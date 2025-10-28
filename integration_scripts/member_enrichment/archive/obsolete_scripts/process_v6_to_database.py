#!/usr/bin/env python3
"""
Process APPROVED V6 enriched bios to SQL database.

Extracts APPROVED entries from ERA_MEMBERS_LACKING_BIOS_V6.md and updates
the SQL database with enriched bio text.
"""

import re
import sqlite3
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
ERA_ADMIN = SCRIPT_DIR.parent.parent
DB_PATH = ERA_ADMIN / 'FathomInventory' / 'fathom_emails.db'
V6_FILE = SCRIPT_DIR / 'ERA_MEMBERS_LACKING_BIOS_V6.md'

def extract_approved_entries(v6_content):
    """Extract all APPROVED entries from V6 markdown file."""
    entries = []
    
    # Split by member headers
    pattern = r'## \d+\. (.+?) APPROVED\s*\n\*\*Bio:\*\*\s*\n\n(.+?)(?=\n\*\*Fields:|$)'
    matches = re.finditer(pattern, v6_content, re.DOTALL)
    
    for match in matches:
        name = match.group(1).strip()
        bio_section = match.group(2).strip()
        
        # Extract bio text (remove markdown formatting like * for italics)
        # Keep the text but remove the * markers
        bio_text = bio_section.replace('*', '').strip()
        
        # Also handle case where bio might not be italicized
        if not bio_text or bio_text == '_[No bio draft yet]_':
            continue
            
        entries.append({
            'name': name,
            'bio': bio_text
        })
    
    return entries

def update_database(entries):
    """Update SQL database with approved bios."""
    print("=" * 80)
    print("PROCESSING V6 APPROVED ENTRIES → SQL DATABASE")
    print("=" * 80)
    print()
    
    # Connect to database
    print(f"Connecting to database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Ensure bio column exists
    try:
        cursor.execute("ALTER TABLE participants ADD COLUMN bio TEXT")
        print("✅ Added 'bio' column to participants table")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("✓  'bio' column already exists")
        else:
            print(f"❌ Error with bio column: {e}")
            return
    
    print()
    print(f"Processing {len(entries)} APPROVED entries...")
    print()
    
    updated = []
    not_found = []
    errors = []
    
    for entry in entries:
        name = entry['name']
        bio = entry['bio']
        
        try:
            # Check if person exists in database (case-insensitive)
            cursor.execute("SELECT id, bio FROM participants WHERE name = ? COLLATE NOCASE", (name,))
            result = cursor.fetchone()
            
            if result:
                person_id, old_bio = result
                
                # Update bio
                cursor.execute("UPDATE participants SET bio = ? WHERE id = ?", (bio, person_id))
                updated.append({
                    'name': name,
                    'old_len': len(old_bio) if old_bio else 0,
                    'new_len': len(bio)
                })
                print(f"✅ {name}")
                print(f"   Old bio: {len(old_bio) if old_bio else 0} chars")
                print(f"   New bio: {len(bio)} chars")
                print()
            else:
                not_found.append(name)
                print(f"⚠️  {name} - NOT FOUND in database")
                print()
        
        except Exception as e:
            errors.append(f"{name}: {e}")
            print(f"❌ {name} - Error: {e}")
            print()
    
    # Commit changes
    conn.commit()
    conn.close()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Bios updated in database: {len(updated)}")
    
    if not_found:
        print(f"\n⚠️  Not found in database ({len(not_found)}):")
        for name in not_found:
            print(f"   - {name}")
    
    if errors:
        print(f"\n❌ Errors ({len(errors)}):")
        for err in errors:
            print(f"   - {err}")
    
    print()
    print("=" * 80)
    print("✅ V6 PROCESSING COMPLETE")
    print("=" * 80)
    
    return updated, not_found, errors

def main():
    # Read V6 file
    print(f"Reading V6 file: {V6_FILE}")
    with open(V6_FILE, 'r') as f:
        v6_content = f.read()
    
    # Extract APPROVED entries
    entries = extract_approved_entries(v6_content)
    
    print(f"Found {len(entries)} APPROVED entries in V6")
    print()
    
    if not entries:
        print("No APPROVED entries found. Exiting.")
        return 0
    
    print("APPROVED members:")
    for entry in entries:
        print(f"  - {entry['name']} ({len(entry['bio'])} chars)")
    print()
    
    # Auto-proceed (user already confirmed)
    print("Proceeding with database update (user confirmed)...")
    print()
    
    # Update database
    updated, not_found, errors = update_database(entries)
    
    # Return results for further processing
    return {
        'updated': updated,
        'not_found': not_found,
        'errors': errors,
        'entries': entries
    }

if __name__ == '__main__':
    result = main()
