#!/usr/bin/env python3
"""
Download and aggregate Fathom transcripts for ERA Africa meetings.

Based on download_transcripts.py approach for Town Halls.
Queries the local database for ERA Africa meetings and compiles transcripts.

Usage:
    python download_africa_transcripts.py --test      # First 3 meetings only
    python download_africa_transcripts.py --all       # All ERA Africa meetings
"""

import sys
import sqlite3
import requests
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Paths
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent / "FathomInventory" / "fathom_emails.db"
OUTPUT_FILE = SCRIPT_DIR / "output" / "era_africa_complete.md"
PROGRESS_FILE = SCRIPT_DIR / "africa_progress.json"
FAILURES_LOG = SCRIPT_DIR / "africa_failures.log"

# Fathom API Configuration
API_KEY = "sF9gLOLjqXECcReINyHCYw.C5u2TizRtq8kvaf7kL6XjkQ6KaAuhvrksUHGvIvlenY"
API_BASE = "https://api.fathom.ai/external/v1"

# Rate limiting
MIN_DELAY_SECONDS = 3
BACKOFF_MULTIPLIER = 2
MAX_CONSECUTIVE_FAILURES = 5


class AfricaTranscriptDownloader:
    """Download ERA Africa meeting transcripts from Fathom API."""
    
    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        self.progress = self._load_progress()
        self.consecutive_failures = 0
        self.current_delay = MIN_DELAY_SECONDS
        
    def _load_progress(self) -> Dict:
        if PROGRESS_FILE.exists():
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        return {
            "completed": [],
            "failed": {},
            "last_processed_date": None
        }
    
    def _save_progress(self):
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(self.progress, indent=2, fp=f)
    
    def _log_failure(self, meeting_info: str, reason: str, details: str = ""):
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {meeting_info}: {reason}"
        if details:
            log_entry += f"\n  Details: {details}"
        log_entry += "\n"
        
        with open(FAILURES_LOG, 'a') as f:
            f.write(log_entry)
    
    def get_africa_meetings(self) -> List[Tuple]:
        """Get ERA Africa meetings from local database."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Filter out very short meetings (< 15 mins) - likely technical issues
        cursor.execute("""
            SELECT hyperlink, title, date, duration
            FROM calls
            WHERE title LIKE '%ERA Africa%'
              AND CAST(REPLACE(duration, ' mins', '') AS INTEGER) >= 15
            ORDER BY date
        """)
        
        meetings = cursor.fetchall()
        conn.close()
        
        if self.test_mode:
            return meetings[:3]
        return meetings
    
    def extract_call_id_from_url(self, url: str) -> Optional[str]:
        """Extract Fathom call ID from share URL."""
        # URL format: https://fathom.video/share/CALL_ID
        parts = url.rstrip('/').split('/')
        return parts[-1] if parts else None
    
    def fetch_transcript(self, meeting_date: str, meeting_title: str) -> Optional[List[Dict]]:
        """
        Fetch transcript from Fathom API using date range query.
        This is the CORRECT way to get historical meeting transcripts.
        """
        headers = {'X-Api-Key': API_KEY}
        
        try:
            # Query by date range (±1 day to catch timezone issues)
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
            
            # Search for ERA Africa in results
            for meeting in data.get('items', []):
                title = meeting.get('meeting_title', '')
                if 'ERA Africa' in title:
                    transcript = meeting.get('transcript')
                    if transcript:
                        print(f"  ✅ Got transcript ({len(transcript)} entries)")
                        self.consecutive_failures = 0
                        self.current_delay = MIN_DELAY_SECONDS
                        return transcript
            
            # No ERA Africa meeting found in date range
            print(f"  ⚠️  No ERA Africa meeting found in date range")
            return None
                
        except Exception as e:
            print(f"  ❌ Request failed: {e}")
            return None
    
    def format_transcript_section(self, meeting: Tuple, transcript_data: Optional[List[Dict]]) -> str:
        """Format meeting section for markdown output."""
        hyperlink, title, date, duration = meeting
        
        section = f"## 📅 {title}\n\n"
        section += f"**Date:** {date}\n"
        section += f"**Duration:** {duration}\n"
        section += f"**Link:** {hyperlink}\n\n"
        section += "## 💬 Transcript\n\n"
        
        if transcript_data and isinstance(transcript_data, list):
            # Transcript is a list of entries with speaker and text
            for entry in transcript_data:
                speaker = entry.get('speaker', 'Unknown')
                text = entry.get('text', '').strip()
                if text:
                    section += f"**{speaker}:** {text}\n\n"
        else:
            section += "*Transcript not available*\n\n"
        
        section += "---\n\n"
        return section
    
    def download_all(self):
        """Download transcripts for all ERA Africa meetings."""
        meetings = self.get_africa_meetings()
        
        print(f"Found {len(meetings)} ERA Africa meetings (≥15 mins)")
        if self.test_mode:
            print("TEST MODE: Processing first 3 only")
        print()
        
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        # Header
        header = f"""# ERA Africa Meetings - Complete Transcript Archive

**Generated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
**Total Meetings:** {len(meetings)}
**Source:** Fathom API + Local Database

---

"""
        
        all_sections = [header]
        success_count = 0
        failure_count = 0
        
        for i, meeting in enumerate(meetings, 1):
            hyperlink, title, date, duration = meeting
            call_id = self.extract_call_id_from_url(hyperlink)
            
            print(f"[{i}/{len(meetings)}] {date} - {duration}")
            
            if not call_id:
                print(f"  ⚠️  Could not extract call ID from {hyperlink}")
                self._log_failure(f"{date} - {title}", "No call ID in URL", hyperlink)
                failure_count += 1
                continue
            
            # Check if already processed
            if call_id in self.progress['completed']:
                print(f"  ⏭️  Already processed, skipping")
                continue
            
            # Fetch transcript using date range query
            print(f"  Fetching transcript for {date}...")
            transcript_data = self.fetch_transcript(date, title)
            
            if transcript_data:
                print(f"  ✅ Got transcript")
                success_count += 1
                self.consecutive_failures = 0
                self.current_delay = MIN_DELAY_SECONDS
            else:
                print(f"  ⚠️  No transcript available")
                self._log_failure(f"{date} - {title}", "No transcript from API", call_id)
                failure_count += 1
                self.consecutive_failures += 1
            
            # Format section
            section = self.format_transcript_section(meeting, transcript_data)
            all_sections.append(section)
            
            # Update progress
            self.progress['completed'].append(call_id)
            self.progress['last_processed_date'] = date
            self._save_progress()
            
            # Write incrementally
            OUTPUT_FILE.write_text(''.join(all_sections))
            
            # Rate limiting
            if i < len(meetings):
                time.sleep(self.current_delay)
            
            # Check for too many consecutive failures
            if self.consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                print(f"\n⚠️  {MAX_CONSECUTIVE_FAILURES} consecutive failures. Stopping.")
                break
        
        print(f"\n{'='*80}")
        print(f"✅ Complete!")
        print(f"   Success: {success_count}/{len(meetings)}")
        print(f"   Failures: {failure_count}/{len(meetings)}")
        print(f"   Output: {OUTPUT_FILE}")
        print(f"{'='*80}")


def main():
    parser = argparse.ArgumentParser(description='Download ERA Africa meeting transcripts')
    parser.add_argument('--test', action='store_true', help='Test mode: first 3 meetings only')
    parser.add_argument('--all', action='store_true', help='Download all ERA Africa meetings')
    
    args = parser.parse_args()
    
    if not (args.test or args.all):
        print("Usage: python download_africa_transcripts.py [--test | --all]")
        sys.exit(1)
    
    downloader = AfricaTranscriptDownloader(test_mode=args.test)
    downloader.download_all()


if __name__ == '__main__':
    main()
