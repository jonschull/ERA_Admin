#!/usr/bin/env python3
"""
Download and aggregate Fathom transcripts for ERA Town Hall meetings.

Conservative approach:
- Sequential processing only (no parallel)
- Wait for confirmation before next request
- 3-second minimum delay between successful requests
- Exponential backoff on errors
- Detailed failure logging for mop-up

Usage:
    python download_transcripts.py --test      # First 3 meetings only
    python download_transcripts.py --all       # All 66 ERA Town Halls
    python download_transcripts.py --resume    # Resume from interruption
"""

import sys
import sqlite3
import requests
import json
import time
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# Paths
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent / "FathomInventory" / "fathom_emails.db"
OUTPUT_FILE = SCRIPT_DIR / "output" / "era_townhalls_complete.md"
PROGRESS_FILE = SCRIPT_DIR / "progress.json"
FAILURES_LOG = SCRIPT_DIR / "failures.log"

# Fathom API Configuration (from test_api2.py)
API_KEY = "sF9gLOLjqXECcReINyHCYw.C5u2TizRtq8kvaf7kL6XjkQ6KaAuhvrksUHGvIvlenY"
API_BASE = "https://api.fathom.ai/external/v1"

# Rate limiting configuration
MIN_DELAY_SECONDS = 3  # Minimum delay between successful requests
BACKOFF_MULTIPLIER = 2  # Multiply delay on errors
MAX_CONSECUTIVE_FAILURES = 5  # Abort after this many consecutive failures


class TranscriptDownloader:
    """Conservative transcript downloader with failure tracking."""
    
    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        self.progress = self._load_progress()
        self.consecutive_failures = 0
        self.current_delay = MIN_DELAY_SECONDS
        
    def _load_progress(self) -> Dict:
        """Load progress from file for resumability."""
        if PROGRESS_FILE.exists():
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        return {
            "completed": [],
            "failed": {},
            "last_processed_date": None
        }
    
    def _save_progress(self):
        """Save progress for resumability."""
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(self.progress, indent=2, fp=f)
    
    def _log_failure(self, meeting_id: str, reason: str, details: str = ""):
        """Log failure with timestamp for mop-up."""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {meeting_id}: {reason}"
        if details:
            log_entry += f"\n  Details: {details}"
        log_entry += "\n"
        
        with open(FAILURES_LOG, 'a') as f:
            f.write(log_entry)
        
        self.progress["failed"][meeting_id] = {
            "reason": reason,
            "timestamp": timestamp,
            "details": details
        }
    
    def get_era_town_halls(self) -> List[Dict]:
        """Get all ERA Town Hall meetings from database, chronologically."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        query = """
            SELECT 
                c.hyperlink,
                c.title,
                c.date,
                c.duration,
                t.agenda_text,
                t.meeting_title as agenda_title,
                e.body_md as summary
            FROM calls c
            LEFT JOIN town_hall_agendas t ON DATE(c.date) = DATE(t.meeting_date)
            LEFT JOIN (
                SELECT meeting_date, body_md 
                FROM emails 
                WHERE subject LIKE '%Summary%ERA%'
            ) e ON DATE(c.date) = DATE(e.meeting_date)
            WHERE c.title LIKE '%ERA Town Hall%'
            ORDER BY c.date
        """
        
        if self.test_mode:
            query += " LIMIT 3"
        
        cursor.execute(query)
        
        meetings = []
        for row in cursor.fetchall():
            meeting_id = row[0].split('/calls/')[-1] if '/calls/' in row[0] else None
            meetings.append({
                'url': row[0],
                'id': meeting_id,
                'title': row[1],
                'date': row[2],
                'duration': row[3],
                'agenda': row[4],
                'agenda_title': row[5],
                'summary': row[6]
            })
        
        conn.close()
        return meetings
    
    def fetch_transcript(self, meeting_date: str, meeting_title: str) -> Optional[List[Dict]]:
        """
        Fetch transcript from Fathom API using date range query.
        Returns transcript data or None on failure.
        Implements conservative rate limiting and error handling.
        Uses date-based search to find historical meetings.
        """
        headers = {'X-Api-Key': API_KEY}
        
        try:
            print(f"  🔍 Querying API for {meeting_date}...", end=' ', flush=True)
            
            # Query by date range (meeting date ±1 day to catch timezone issues)
            from datetime import datetime, timedelta
            meeting_dt = datetime.strptime(meeting_date, '%Y-%m-%d')
            start_date = (meeting_dt - timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z')
            end_date = (meeting_dt + timedelta(days=1)).strftime('%Y-%m-%dT23:59:59Z')
            
            params = {
                'created_after': start_date,
                'created_before': end_date,
                'limit': 100,
                'include_transcript': 'true'
            }
            
            response = requests.get(
                f'{API_BASE}/meetings',
                headers=headers,
                params=params,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Search for ERA Town Hall in results
            for meeting in data.get('items', []):
                title = meeting.get('meeting_title', '')
                if 'ERA Town Hall' in title or meeting_title in title:
                    transcript = meeting.get('transcript')
                    if transcript:
                        print(f"✅ ({len(transcript)} entries)")
                        self.consecutive_failures = 0
                        self.current_delay = MIN_DELAY_SECONDS
                        return transcript
                    else:
                        print(f"⚠️  Found but no transcript")
                        return None
            
            # ERA Town Hall not found in this date range
            print(f"⚠️  Not found in date range")
            return None
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"🚫 Rate limited")
            else:
                print(f"❌ HTTP error {e.response.status_code}")
            self.consecutive_failures += 1
            self.current_delay *= BACKOFF_MULTIPLIER
            return None
            
        except requests.exceptions.Timeout:
            print("❌ Timeout")
            self.consecutive_failures += 1
            self.current_delay *= BACKOFF_MULTIPLIER
            return None
            
        except Exception as e:
            print(f"❌ Error: {str(e)[:100]}")
            self.consecutive_failures += 1
            self.current_delay *= BACKOFF_MULTIPLIER
            return None
    
    def strip_images(self, text: str) -> str:
        """Remove base64 encoded images from markdown text."""
        if not text:
            return text
        
        import re
        # Remove markdown image references like [image1]: <data:image/...>
        text = re.sub(r'\[image\d+\]:\s*<data:image/[^>]+>', '', text, flags=re.IGNORECASE)
        # Remove inline images like ![alt](data:image/...)
        text = re.sub(r'!\[([^\]]*)\]\(data:image/[^)]+\)', '', text, flags=re.IGNORECASE)
        # Remove any remaining ![][imageN] references
        text = re.sub(r'!\[\]\[image\d+\]', '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def format_transcript(self, transcript_data: List[Dict]) -> str:
        """Format transcript data as markdown."""
        if not transcript_data:
            return "*Transcript data unavailable*\n"
        
        lines = []
        for entry in transcript_data:
            speaker = entry.get('speaker', {})
            speaker_name = speaker.get('display_name', 'Unknown Speaker')
            speaker_email = speaker.get('matched_calendar_invitee_email', '')
            
            # Handle timestamp - can be string (HH:MM:SS) or number (seconds)
            timestamp = entry.get('timestamp', '00:00:00')
            if isinstance(timestamp, str):
                time_str = timestamp
            else:
                # Convert seconds to HH:MM:SS
                hours = int(timestamp // 3600)
                minutes = int((timestamp % 3600) // 60)
                seconds = int(timestamp % 60)
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            text = entry.get('text', '').strip()
            
            # Format: **[HH:MM:SS] Speaker Name** (email)
            if speaker_email:
                lines.append(f"**[{time_str}] {speaker_name}** ({speaker_email})")
            else:
                lines.append(f"**[{time_str}] {speaker_name}**")
            lines.append(f"> {text}")
            lines.append("")  # Blank line between entries
        
        return "\n".join(lines)
    
    def generate_meeting_section(self, meeting: Dict, transcript: Optional[List[Dict]]) -> str:
        """Generate complete markdown section for one meeting."""
        lines = [
            "---",
            f"# {meeting['title']}",
            f"**Date:** {meeting['date']} | **Duration:** {meeting['duration'] or 'Unknown'}",
            f"**Fathom URL:** {meeting['url']}",
            "",
            "---",
            ""
        ]
        
        # Add agenda if available (strip images)
        if meeting['agenda']:
            clean_agenda = self.strip_images(meeting['agenda'])
            if clean_agenda:  # Only include if there's content after stripping
                lines.extend([
                    "## 📋 Town Hall Agenda & Notes",
                    "",
                    clean_agenda,
                    "",
                    "---",
                    ""
                ])
        
        # Add Fathom summary if available
        if meeting['summary']:
            lines.extend([
                "## 🤖 Fathom AI Summary",
                "",
                meeting['summary'].strip(),
                "",
                "---",
                ""
            ])
        
        # Add transcript
        lines.extend([
            "## 💬 Transcript",
            ""
        ])
        
        if transcript:
            lines.append(self.format_transcript(transcript))
        else:
            lines.append("*Transcript not available via API (meeting may be too old or not yet processed)*")
            lines.append("")
        
        lines.extend([
            "---",
            "---",
            ""
        ])
        
        return "\n".join(lines)
    
    def process_all_meetings(self):
        """Main processing loop with conservative rate limiting."""
        meetings = self.get_era_town_halls()
        
        mode_str = "TEST MODE (first 3 meetings)" if self.test_mode else f"ALL {len(meetings)} ERA Town Halls"
        print(f"\n{'='*80}")
        print(f"FATHOM TRANSCRIPT DOWNLOADER - {mode_str}")
        print(f"{'='*80}\n")
        print(f"Output: {OUTPUT_FILE}")
        print(f"Progress: {PROGRESS_FILE}")
        print(f"Failures: {FAILURES_LOG}")
        print(f"\nRate limiting: {MIN_DELAY_SECONDS}s between requests, exponential backoff on errors")
        print(f"Abort threshold: {MAX_CONSECUTIVE_FAILURES} consecutive failures\n")
        
        # Initialize output file (only if starting fresh)
        if not OUTPUT_FILE.exists() or len(self.progress['completed']) == 0:
            print("📝 Creating new output file...")
            with open(OUTPUT_FILE, 'w') as f:
                f.write(f"# ERA Town Hall Meetings - Complete Archive\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Total Meetings:** {len(meetings)}\n\n")
                f.write(f"This document aggregates meeting agendas, AI summaries, and full transcripts ")
                f.write(f"for all ERA Town Hall meetings, in chronological order.\n\n")
        else:
            print(f"📝 Resuming - appending to existing file ({len(self.progress['completed'])} already completed)...")
        
        # Process each meeting sequentially
        for i, meeting in enumerate(meetings, 1):
            meeting_id = meeting['id']
            
            # Skip if already completed
            if meeting_id in self.progress['completed']:
                print(f"[{i}/{len(meetings)}] ⏭️  Skipping {meeting['date']} (already completed)")
                continue
            
            print(f"\n[{i}/{len(meetings)}] Processing {meeting['date']} - {meeting['title']}")
            print(f"  ID: {meeting_id}")
            
            # Check for consecutive failures threshold
            if self.consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                print(f"\n❌ ABORTING: {MAX_CONSECUTIVE_FAILURES} consecutive failures")
                print(f"   Check {FAILURES_LOG} for details")
                print(f"   Progress saved - resume with:")
                if self.test_mode:
                    print(f"   python download_transcripts.py --test")
                else:
                    print(f"   python download_transcripts.py --all")
                self._save_progress()
                break
            
            # Fetch transcript (with rate limiting built in)
            transcript = self.fetch_transcript(meeting['date'], meeting['title'])
            
            # Generate and append section
            section = self.generate_meeting_section(meeting, transcript)
            with open(OUTPUT_FILE, 'a') as f:
                f.write(section)
            
            # Track completion
            if transcript:
                self.progress['completed'].append(meeting_id)
                print(f"  ✅ Completed with transcript")
            else:
                self.progress['completed'].append(meeting_id)
                self._log_failure(meeting_id, "No transcript available", "API returned no transcript data")
                print(f"  ⚠️  Completed without transcript (logged)")
            
            self.progress['last_processed_date'] = meeting['date']
            self._save_progress()
            
            # Conservative delay before next request
            if i < len(meetings):  # Don't delay after last meeting
                print(f"  ⏳ Waiting {self.current_delay}s before next request...")
                time.sleep(self.current_delay)
        
        # Final summary
        print(f"\n{'='*80}")
        print(f"PROCESSING COMPLETE")
        print(f"{'='*80}")
        print(f"✅ Completed: {len(self.progress['completed'])} meetings")
        print(f"❌ Failed: {len(self.progress['failed'])} meetings")
        print(f"\nOutput: {OUTPUT_FILE}")
        if self.progress['failed']:
            print(f"Failures logged in: {FAILURES_LOG}")
            print(f"\nFailed meetings can be manually reviewed for mop-up.")
        print()


def main():
    parser = argparse.ArgumentParser(description="Download ERA Town Hall transcripts from Fathom API")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--test', action='store_true', help='Test mode: first 3 meetings only')
    group.add_argument('--all', action='store_true', help='Process all 66 ERA Town Hall meetings')
    group.add_argument('--resume', action='store_true', help='Resume from previous interruption')
    
    args = parser.parse_args()
    
    test_mode = args.test or args.resume
    downloader = TranscriptDownloader(test_mode=test_mode)
    
    try:
        downloader.process_all_meetings()
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Interrupted by user (Ctrl+C)")
        print(f"   Saving progress...")
        downloader._save_progress()
        print(f"   ✅ Progress saved to {PROGRESS_FILE}")
        print(f"   Resume with: python download_transcripts.py --{'test' if test_mode else 'all'}")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        print(f"   Saving progress...")
        downloader._save_progress()
        print(f"   ✅ Progress saved to {PROGRESS_FILE}")
        print(f"   Resume with: python download_transcripts.py --{'test' if test_mode else 'all'}")
        raise


if __name__ == '__main__':
    main()
