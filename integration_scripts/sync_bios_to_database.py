#!/usr/bin/env python3
"""
Synchronize bios from Airtable to Fathom database.

Steps:
1. Add bio column to participants table (if doesn't exist)
2. Copy all bios from Airtable to database
3. Report sync status
"""

import csv
import sqlite3
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
ERA_ADMIN = SCRIPT_DIR.parent
DB_PATH = ERA_ADMIN / 'FathomInventory' / 'fathom_emails.db'
AIRTABLE_CSV = ERA_ADMIN / 'airtable' / 'people_export.csv'

def main():
    print("=" * 80)
    print("SYNCHRONIZING BIOS: Airtable → Database")
    print("=" * 80)
    print()
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Step 1: Add bio column if doesn't exist
    print("1. Adding 'bio' column to participants table...")
    try:
        cursor.execute("ALTER TABLE participants ADD COLUMN bio TEXT")
        print("   ✅ Column added")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("   ✓  Column already exists")
        else:
            print(f"   ❌ Error: {e}")
            return 1
    
    print()
    
    # Step 2: Load bios from Airtable
    print("2. Loading bios from Airtable...")
    airtable_bios = {}
    
    with open(AIRTABLE_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            bio = row.get('Bio', '').strip()
            if bio:  # Only store non-empty bios
                airtable_bios[name] = bio
    
    print(f"   Found {len(airtable_bios)} bios in Airtable")
    print()
    
    # Step 3: Sync to database
    print("3. Syncing bios to database...")
    
    synced = 0
    not_found = []
    errors = []
    
    for name, bio in airtable_bios.items():
        try:
            # Check if person exists in database
            cursor.execute("SELECT id FROM participants WHERE name = ? COLLATE NOCASE", (name,))
            result = cursor.fetchone()
            
            if result:
                person_id = result[0]
                cursor.execute("UPDATE participants SET bio = ? WHERE id = ?", (bio, person_id))
                synced += 1
                if synced <= 10:  # Show first 10
                    print(f"   ✅ {name} ({len(bio)} chars)")
            else:
                not_found.append(name)
        
        except Exception as e:
            errors.append(f"{name}: {e}")
    
    if synced > 10:
        print(f"   ... and {synced - 10} more")
    
    conn.commit()
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Bios synced to database: {synced}")
    
    if not_found:
        print(f"\n⚠️  People in Airtable not found in database: {len(not_found)}")
        if len(not_found) <= 20:
            for name in not_found:
                print(f"   - {name}")
        else:
            for name in not_found[:10]:
                print(f"   - {name}")
            print(f"   ... and {len(not_found) - 10} more")
    
    if errors:
        print(f"\n❌ Errors: {len(errors)}")
        for err in errors[:5]:
            print(f"   - {err}")
    
    # Step 4: Verify sync
    print()
    print("4. Verifying sync...")
    cursor.execute("SELECT COUNT(*) FROM participants WHERE bio IS NOT NULL AND bio != ''")
    db_bio_count = cursor.fetchone()[0]
    print(f"   Database now has {db_bio_count} bios")
    
    conn.close()
    
    print()
    print("=" * 80)
    print("✅ SYNC COMPLETE - Database is now source of truth for bios")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Perfect bios in database")
    print("2. Later: Push perfected bios back to Airtable")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
