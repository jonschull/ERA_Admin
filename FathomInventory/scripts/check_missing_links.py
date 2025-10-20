#!/usr/bin/env python3
"""Check if database has URLs for TSV entries missing hyperlinks."""

import csv
import sqlite3
from datetime import datetime

TSV_FILE = "all_fathom_calls.tsv"
DB_FILE = "fathom_emails.db"

def normalize_date(date_str):
    """Normalize date formats for matching."""
    # TSV format: "Sep 3, 2025" -> "September 03, 2025"
    # Database format: "September 03, 2025"
    try:
        dt = datetime.strptime(date_str, "%b %d, %Y")
        return dt.strftime("%B %d, %Y")
    except:
        return date_str

# Read TSV entries without hyperlinks
missing_links = []
with open(TSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        if not row.get('Hyperlink', '').strip():
            missing_links.append(row)

print(f"Found {len(missing_links)} TSV entries without hyperlinks\n")

# Connect to database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

matches_found = 0
matches_with_diff_duration = 0

for entry in missing_links[:10]:  # Check first 10
    title = entry['Title']
    date = normalize_date(entry['Date'])
    duration_str = entry.get('Duration', '')
    
    cursor.execute("""
        SELECT meeting_title, meeting_date, meeting_duration_mins, meeting_url 
        FROM emails 
        WHERE meeting_title = ? AND meeting_date = ?
    """, (title, date))
    
    result = cursor.fetchone()
    if result:
        db_title, db_date, db_duration, db_url = result
        matches_found += 1
        
        tsv_duration = duration_str.split()[0] if duration_str else "?"
        duration_match = str(db_duration) == tsv_duration
        
        if not duration_match:
            matches_with_diff_duration += 1
        
        print(f"✓ MATCH: {title}")
        print(f"  TSV:  {date} | {duration_str}")
        print(f"  DB:   {db_date} | {db_duration} mins")
        print(f"  URL:  {db_url[:80]}...")
        print(f"  Duration match: {duration_match}\n")

conn.close()

print(f"\n=== SUMMARY ===")
print(f"Checked: {min(10, len(missing_links))} entries")
print(f"Matches found: {matches_found}")
print(f"With different duration: {matches_with_diff_duration}")
