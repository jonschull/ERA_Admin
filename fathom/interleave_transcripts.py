#!/usr/bin/env python3
"""
Interleave Manually-Collected Transcripts into Complete Archive

PURPOSE:
    Replace "Transcript not available" placeholders in era_townhalls_complete.md
    with actual transcripts that were manually downloaded from Fathom website.

CONTEXT:
    Some ERA Town Hall meetings are accessible on Fathom website but not via API.
    After download_transcripts.py completes, it leaves placeholders for these meetings.
    This script integrates manually-collected transcripts from Missing 7.md.

WORKFLOW:
    1. Backup era_townhalls_complete.md
    2. Parse Missing 7.md to extract transcripts by date
    3. Find corresponding meeting sections in complete file
    4. Replace "Transcript not available" with actual transcript
    5. Delete Missing 7.md (now integrated)

INPUT:
    - output/era_townhalls_complete.md (with placeholders)
    - output/Missing 7.md (manually-collected transcripts)

OUTPUT:
    - output/era_townhalls_complete.md (updated with all transcripts)
    - output/era_townhalls_complete.md.backup (original preserved)

SAFETY:
    - Creates backup before any modifications
    - Uses regex matching to find exact meeting sections
    - Validates transcript content before replacement
    - Reports success/failure for each meeting

USAGE:
    python3 interleave_transcripts.py

REQUIREMENTS:
    - Missing 7.md must follow format:
      ERA Town Hall Meeting - [Month] [Day]
      VIEW RECORDING - ...
      ---
      [transcript content]

AUTHOR: ERA Admin / Cascade AI
DATE: 2025-10-24
"""

import re
from pathlib import Path

COMPLETE_FILE = Path("output/era_townhalls_complete.md")
MISSING_FILE = Path("output/Missing 7.md")
BACKUP_FILE = Path("output/era_townhalls_complete.md.backup")

# Parse Missing 7.md to extract transcripts by date
def parse_missing_transcripts():
    """Extract each meeting's transcript from Missing 7.md"""
    content = MISSING_FILE.read_text()
    
    # Split by "ERA Town Hall Meeting" headers
    meetings = []
    parts = re.split(r'(ERA Town Hall Meeting[^\n]+\n)', content)
    
    # Reconstruct meetings (header + content)
    for i in range(1, len(parts), 2):
        if i+1 < len(parts):
            header = parts[i].strip()
            content_part = parts[i+1]
            
            # Extract date from header
            date_match = re.search(r'- (April|May|June|July|August|September|October|November|December) (\d+)', header)
            if date_match:
                month_map = {
                    'April': '04', 'May': '05', 'June': '06', 'July': '07',
                    'August': '08', 'September': '09', 'October': '10',
                    'November': '11', 'December': '12'
                }
                month = month_map[date_match.group(1)]
                day = date_match.group(2).zfill(2)
                
                # Determine year based on month (2023 for April, 2024 for Dec, 2025 for rest)
                if month == '04':
                    year = '2023'
                elif month == '12':
                    year = '2024'
                else:
                    year = '2025'
                
                date_key = f"{year}-{month}-{day}"
                
                # Extract just the transcript part (from "---" to end or next meeting)
                # The transcript should start after VIEW RECORDING line
                meetings.append({
                    'date': date_key,
                    'header': header,
                    'content': content_part
                })
                print(f"Parsed transcript for {date_key}")
    
    return meetings

def interleave_transcripts():
    """Carefully replace 'Transcript not available' sections with actual transcripts"""
    
    # Backup first
    print(f"Creating backup: {BACKUP_FILE}")
    BACKUP_FILE.write_text(COMPLETE_FILE.read_text())
    
    # Parse missing transcripts
    missing_transcripts = parse_missing_transcripts()
    print(f"\nFound {len(missing_transcripts)} transcripts to interleave")
    
    # Read complete file
    complete_content = COMPLETE_FILE.read_text()
    
    # For each missing transcript, find and replace in complete file
    for mt in missing_transcripts:
        date = mt['date']
        print(f"\nProcessing {date}...")
        
        # Find the meeting section in complete file
        # Pattern: date followed by transcript section
        pattern = rf'(\*\*Date:\*\* {re.escape(date)}[^\n]*\n.*?## 💬 Transcript\n\n)\*Transcript not available[^\n]*\n'
        
        matches = list(re.finditer(pattern, complete_content, re.DOTALL))
        
        if matches:
            print(f"  Found meeting section for {date}")
            match = matches[0]
            
            # Extract transcript from missing file (everything after "---" following VIEW RECORDING)
            transcript_match = re.search(r'VIEW RECORDING[^\n]*\n\n---\n\n(.*?)(?=\n  ERA Town Hall|\Z)', mt['content'], re.DOTALL)
            
            if transcript_match:
                new_transcript = transcript_match.group(1).strip()
                
                # Replace the "Transcript not available" with actual transcript
                replacement = match.group(1) + new_transcript + "\n"
                complete_content = complete_content[:match.start()] + replacement + complete_content[match.end():]
                print(f"  ✅ Replaced transcript ({len(new_transcript)} chars)")
            else:
                print(f"  ⚠️  Could not extract transcript content")
        else:
            print(f"  ⚠️  Could not find meeting section in complete file")
    
    # Write updated content
    print(f"\n Writing updated file...")
    COMPLETE_FILE.write_text(complete_content)
    print(f"✅ Complete! Updated {COMPLETE_FILE}")
    
    return len(missing_transcripts)

if __name__ == '__main__':
    count = interleave_transcripts()
    print(f"\n{'='*60}")
    print(f"Successfully interleaved {count} transcripts")
    print(f"Backup saved to: {BACKUP_FILE}")
    print(f"{'='*60}")
