#!/usr/bin/env python3
"""
Import NEW participants from CSV to database (incremental import)
Skips already-imported participants based on (name, source_call_url) combination
"""
import csv
import sqlite3

DB_FILE = '../fathom_emails.db'
CSV_FILE = 'participants.csv'

def get_existing_participants(conn):
    """Get set of existing (name, source_url) tuples"""
    cursor = conn.cursor()
    cursor.execute("SELECT name, source_call_url FROM participants")
    return set((row[0], row[1]) for row in cursor.fetchall())

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
    """Import only NEW participants"""
    
    print("🔌 Connecting to database...")
    conn = sqlite3.connect(DB_FILE)
    
    print("📖 Reading existing participants from database...")
    existing = get_existing_participants(conn)
    print(f"   Found {len(existing)} existing participant records")
    
    print("📖 Reading participants from CSV...")
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_participants = list(reader)
    print(f"   Found {len(all_participants)} total records in CSV")
    
    # Filter to NEW participants only
    new_participants = []
    for p in all_participants:
        key = (p['Name'], p['Source_Call_URL'])
        if key not in existing:
            new_participants.append(p)
    
    print(f"\n📊 New participants to import: {len(new_participants)}")
    
    if len(new_participants) == 0:
        print("✅ No new participants - database is up to date!")
        conn.close()
        return 0, 0
    
    cursor = conn.cursor()
    imported = 0
    linked = 0
    
    print("💾 Importing new participants...")
    for i, p in enumerate(new_participants, 1):
        call_hyperlink = get_call_hyperlink(conn, p['Source_Call_URL'])
        if call_hyperlink:
            linked += 1
        
        cursor.execute("""
            INSERT INTO participants (
                name, location, affiliation,
                collaborating_people, collaborating_organizations,
                source_call_url, source_call_title,
                call_hyperlink
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p['Name'],
            p['Location'],
            p['Affiliation'],
            p['Collaborating_People'],
            p['Collaborating_Organizations'],
            p['Source_Call_URL'],
            p['Source_Call_Title'],
            call_hyperlink
        ))
        
        imported += 1
        
        if i % 50 == 0:
            print(f"  Progress: {i}/{len(new_participants)}")
            conn.commit()
    
    conn.commit()
    
    print(f"\n✅ Imported {imported} new participant records")
    print(f"🔗 Linked {linked} to calls table ({linked/imported*100:.1f}%)")
    
    # Final count
    cursor.execute("SELECT COUNT(*) FROM participants")
    total = cursor.fetchone()[0]
    print(f"📊 Total participants in database: {total}")
    
    conn.close()
    return imported, linked

if __name__ == '__main__':
    try:
        imported, linked = import_new_participants()
        print(f"\n{'='*60}")
        print(f"✅ IMPORT COMPLETE")
        print(f"{'='*60}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
