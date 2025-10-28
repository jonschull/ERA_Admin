#!/usr/bin/env python3
"""
Restore lost Town Hall attendance records.

Adds call attendance from deleted duplicate names to their canonical versions.
This repairs the data loss from today's reckless merges.
"""

import csv
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'FathomInventory' / 'fathom_emails.db'
CSV_PATH = Path(__file__).parent / 'LOST_ATTENDANCE_RECORDS.csv'

def main():
    print("=" * 80)
    print("RESTORING LOST ATTENDANCE RECORDS")
    print("=" * 80)
    print()
    
    # Load lost records from CSV
    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        lost_records = list(reader)
    
    print(f"Found {len(lost_records)} lost attendance records")
    print()
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    added = 0
    already_exists = 0
    errors = 0
    
    for record in lost_records:
        canonical_name = record['canonical_name']
        call_hyperlink = record['call_hyperlink']
        source_call_title = record['source_call_title']
        
        print(f"Processing: {record['deleted_name']} → {canonical_name}")
        print(f"  Call: {source_call_title}")
        print(f"  Link: {call_hyperlink}")
        
        # Get current source_call_url for canonical name
        cursor.execute("""
            SELECT source_call_url FROM participants WHERE name = ?
        """, (canonical_name,))
        
        result = cursor.fetchone()
        
        if not result:
            print(f"  ⚠️  {canonical_name} not found in database - skipping")
            errors += 1
            continue
        
        current_urls = result[0] or ""
        source_call_url = record['source_call_url']
        
        # Check if this call is already in the comma-separated list
        url_list = [u.strip() for u in current_urls.split(',') if u.strip()]
        
        if source_call_url in url_list or call_hyperlink in current_urls:
            print(f"  ✓  Call already in attendance list - skipping")
            already_exists += 1
        else:
            # Add the call URL to the comma-separated list
            try:
                if current_urls:
                    new_urls = current_urls + ', ' + source_call_url
                else:
                    new_urls = source_call_url
                
                cursor.execute("""
                    UPDATE participants
                    SET source_call_url = ?
                    WHERE name = ?
                """, (new_urls, canonical_name))
                
                print(f"  ✅ Added call to attendance list")
                added += 1
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                errors += 1
        
        print()
    
    # Commit changes
    conn.commit()
    
    # Verify
    print("=" * 80)
    print("VERIFICATION")
    print("=" * 80)
    
    for canonical in set(r['canonical_name'] for r in lost_records):
        cursor.execute("""
            SELECT COUNT(DISTINCT call_hyperlink) 
            FROM participants 
            WHERE name = ?
        """, (canonical,))
        count = cursor.fetchone()[0]
        print(f"{canonical}: {count} unique call(s)")
    
    conn.close()
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Added: {added}")
    print(f"✓  Already existed: {already_exists}")
    print(f"❌ Errors: {errors}")
    print()
    
    if added > 0:
        print("✅ Successfully restored lost Town Hall attendance data")
    else:
        print("⚠️  No new records added")
    
    return 0 if errors == 0 else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
