#!/usr/bin/env python3
"""
Import participant data from participants.csv into fathom_emails.db

This script:
1. Creates participants table if it doesn't exist
2. Imports participant records from CSV
3. Links to existing calls in the database
4. Handles duplicates gracefully (same person in multiple calls)
"""

import csv
import sqlite3
import sys
from pathlib import Path

# Configuration
DB_FILE = '../fathom_emails.db'
CSV_FILE = 'participants.csv'
SCHEMA_FILE = 'schema_participants.sql'

def create_schema(conn):
    """Create participants table and indexes"""
    print("📋 Creating database schema...")
    
    with open(SCHEMA_FILE, 'r') as f:
        schema_sql = f.read()
    
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    print("✅ Schema created")

def get_call_hyperlink(conn, source_url):
    """
    Try to find matching call hyperlink in calls table.
    The source_url from analysis might not exactly match.
    """
    cursor = conn.cursor()
    
    # Direct match
    cursor.execute("SELECT hyperlink FROM calls WHERE hyperlink = ?", (source_url,))
    result = cursor.fetchone()
    if result:
        return result[0]
    
    # Try extracting call ID and matching
    if '/calls/' in source_url:
        call_id = source_url.split('/calls/')[-1].split('?')[0]
        cursor.execute("SELECT hyperlink FROM calls WHERE hyperlink LIKE ?", (f'%/calls/{call_id}%',))
        result = cursor.fetchone()
        if result:
            return result[0]
    
    return None

def import_participants(conn):
    """Import participants from CSV"""
    print(f"📖 Reading {CSV_FILE}...")
    
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        participants = list(reader)
    
    print(f"📊 Found {len(participants)} participant records")
    
    cursor = conn.cursor()
    imported = 0
    linked = 0
    
    print("💾 Importing to database...")
    
    for i, p in enumerate(participants, 1):
        # Find matching call hyperlink
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
        
        if i % 100 == 0:
            print(f"  Progress: {i}/{len(participants)} ({i/len(participants)*100:.1f}%)")
            conn.commit()
    
    conn.commit()
    
    print(f"\n✅ Imported {imported} participant records")
    print(f"🔗 Linked {linked} to calls table ({linked/imported*100:.1f}%)")
    
    return imported, linked

def validate_import(conn):
    """Validate the import with some quick queries"""
    print("\n🔍 Validating import...")
    
    cursor = conn.cursor()
    
    # Count total participants
    cursor.execute("SELECT COUNT(*) FROM participants")
    total = cursor.fetchone()[0]
    print(f"  Total participants: {total}")
    
    # Count unique names
    cursor.execute("SELECT COUNT(DISTINCT name) FROM participants")
    unique_names = cursor.fetchone()[0]
    print(f"  Unique names: {unique_names}")
    
    # Count linked to calls
    cursor.execute("SELECT COUNT(*) FROM participants WHERE call_hyperlink IS NOT NULL")
    linked = cursor.fetchone()[0]
    print(f"  Linked to calls: {linked}")
    
    # Sample enriched view
    cursor.execute("""
        SELECT name, call_title, call_date 
        FROM participants_enriched 
        WHERE call_hyperlink IS NOT NULL
        LIMIT 5
    """)
    print("\n  Sample enriched data:")
    for name, title, date in cursor.fetchall():
        print(f"    - {name} from '{title[:40]}...' ({date})")
    
    print("\n✅ Validation complete")

def main():
    """Main import process"""
    print("="*60)
    print("PARTICIPANT DATA IMPORT")
    print("="*60)
    print()
    
    # Check files exist
    if not Path(CSV_FILE).exists():
        print(f"❌ Error: {CSV_FILE} not found")
        sys.exit(1)
    
    if not Path(SCHEMA_FILE).exists():
        print(f"❌ Error: {SCHEMA_FILE} not found")
        sys.exit(1)
    
    if not Path(DB_FILE).exists():
        print(f"❌ Error: {DB_FILE} not found")
        sys.exit(1)
    
    # Connect to database
    print(f"🔌 Connecting to {DB_FILE}...")
    conn = sqlite3.connect(DB_FILE)
    
    try:
        # Create schema
        create_schema(conn)
        
        # Import data
        imported, linked = import_participants(conn)
        
        # Validate
        validate_import(conn)
        
        print("\n" + "="*60)
        print("✅ IMPORT COMPLETE")
        print("="*60)
        print(f"Imported: {imported} participants")
        print(f"Linked: {linked} to existing calls")
        print(f"Database: {DB_FILE}")
        
    except Exception as e:
        print(f"\n❌ Error during import: {e}")
        conn.rollback()
        sys.exit(1)
    
    finally:
        conn.close()

if __name__ == '__main__':
    main()
