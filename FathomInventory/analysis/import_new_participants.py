#!/usr/bin/env python3
"""
Import NEW participants from CSV to database (FIXED for UNIQUE constraint)

CHANGED: Now handles the UNIQUE constraint on participant names
- If person already exists: UPDATE to append new source_call_url
- If person is new: INSERT new record

This prevents UNIQUE constraint errors while preserving attendance history.
"""
import csv
import sqlite3

DB_FILE = '../fathom_emails.db'
CSV_FILE = 'participants.csv'

def get_existing_participant_by_name(conn, name):
    """Check if participant with this name (case-insensitive) already exists"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, source_call_url 
        FROM participants 
        WHERE LOWER(TRIM(name)) = LOWER(TRIM(?))
    """, (name,))
    return cursor.fetchone()

def get_call_hyperlink(conn, source_url):
    """Find matching call hyperlink"""
    cursor = conn.cursor()
    
    # Direct match
    cursor.execute("SELECT hyperlink FROM calls WHERE hyperlink = ?", (source_url,))
    result = cursor.fetchone()
    if result:
        return result[0]
    
    # Extract call ID and match
    if '/calls/' in source_url:
        call_id = source_url.split('/calls/')[-1].split('?')[0]
        cursor.execute("SELECT hyperlink FROM calls WHERE hyperlink LIKE ?", (f'%/calls/{call_id}%',))
        result = cursor.fetchone()
        if result:
            return result[0]
    
    return None

def import_new_participants():
    """Import participants with UNIQUE constraint awareness"""
    
    print("🔌 Connecting to database...")
    conn = sqlite3.connect(DB_FILE)
    
    print("📖 Reading participants from CSV...")
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_participants = list(reader)
    print(f"   Found {len(all_participants)} total records in CSV")
    
    cursor = conn.cursor()
    inserted = 0
    updated = 0
    skipped = 0
    
    print("💾 Processing participants...")
    for i, p in enumerate(all_participants, 1):
        name = p['Name']
        source_url = p['Source_Call_URL']
        
        # Check if person already exists (by name, not name+url combo)
        existing = get_existing_participant_by_name(conn, name)
        
        if existing:
            existing_id, existing_urls = existing
            
            # Check if this specific meeting URL already recorded
            if source_url in existing_urls:
                skipped += 1
                continue
            
            # Append new meeting URL to existing record
            new_urls = existing_urls + ', ' + source_url
            cursor.execute("""
                UPDATE participants
                SET source_call_url = ?,
                    analyzed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_urls, existing_id))
            
            updated += 1
            print(f"  ✓ Updated '{name}' with new meeting")
            
        else:
            # New person - insert
            call_hyperlink = get_call_hyperlink(conn, source_url)
            
            cursor.execute("""
                INSERT INTO participants (
                    name, location, affiliation,
                    collaborating_people, collaborating_organizations,
                    source_call_url, source_call_title,
                    call_hyperlink
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name,
                p['Location'],
                p['Affiliation'],
                p['Collaborating_People'],
                p['Collaborating_Organizations'],
                source_url,
                p['Source_Call_Title'],
                call_hyperlink
            ))
            
            inserted += 1
        
        if i % 50 == 0:
            print(f"  Progress: {i}/{len(all_participants)}")
            conn.commit()
    
    conn.commit()
    
    print(f"\n✅ Import complete:")
    print(f"   Inserted: {inserted} new people")
    print(f"   Updated: {updated} existing people with new meetings")
    print(f"   Skipped: {skipped} (already recorded)")
    
    # Final count
    cursor.execute("SELECT COUNT(*) FROM participants")
    total = cursor.fetchone()[0]
    print(f"📊 Total unique participants in database: {total}")
    
    conn.close()
    return inserted, updated, skipped

if __name__ == '__main__':
    try:
        inserted, updated, skipped = import_new_participants()
        print(f"\n{'='*60}")
        print(f"✅ IMPORT COMPLETE")
        print(f"{'='*60}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
