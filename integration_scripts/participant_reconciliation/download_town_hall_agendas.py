#!/usr/bin/env python3
"""
One-time download of all Town Hall agendas into local database.

This eliminates repeated Google Drive API calls when searching.
After initial download, all searches are local and instant.

Usage:
    python3 download_town_hall_agendas.py
"""

import json
import sqlite3
import sys
from datetime import datetime
from town_hall_search import TownHallSearch

DB_PATH = '../FathomInventory/fathom_emails.db'
INDEX_PATH = 'town_hall_agenda_index.json'

def load_agenda_index():
    """Load the agenda index."""
    with open(INDEX_PATH, 'r') as f:
        return json.load(f)

def download_all_agendas():
    """Download all agenda texts and store in database."""
    
    # Load index
    print("📂 Loading agenda index...")
    agendas = load_agenda_index()
    print(f"   Found {len(agendas)} agendas")
    
    # Initialize search (has download capabilities)
    print("\n🔑 Initializing Google Drive connection...")
    searcher = TownHallSearch(use_local_db=False)  # Need Google Drive mode for downloading
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check what we already have
    cursor.execute("SELECT COUNT(*) FROM town_hall_agendas")
    existing_count = cursor.fetchone()[0]
    print(f"   Database has {existing_count} agendas already")
    
    if existing_count > 0:
        response = input("\n⚠️  Database already has agendas. Re-download all? (yes/no): ").strip().lower()
        if response != 'yes':
            print("Cancelled.")
            return
        print("\n🗑️  Clearing existing data...")
        cursor.execute("DELETE FROM town_hall_agendas")
        conn.commit()
    
    # Download each agenda
    print(f"\n📥 Downloading {len(agendas)} agendas...")
    print("=" * 80)
    
    success_count = 0
    error_count = 0
    
    for i, agenda in enumerate(agendas, 1):
        agenda_id = agenda['id']
        title = agenda['name']  # field is 'name' not 'title'
        date = agenda.get('date', 'Unknown')
        
        print(f"\n[{i}/{len(agendas)}] {title}")
        print(f"   Date: {date}")
        print(f"   ID: {agenda_id}")
        
        # Check if already downloaded in this session
        cursor.execute("SELECT agenda_id FROM town_hall_agendas WHERE agenda_id = ?", (agenda_id,))
        if cursor.fetchone():
            print("   ⏭️  Already downloaded")
            continue
        
        # Download text as Markdown
        try:
            text = searcher.download_agenda_text(agenda_id, as_markdown=True)
            
            if text and len(text) > 100:  # Sanity check
                # Store in database
                cursor.execute("""
                    INSERT INTO town_hall_agendas (agenda_id, meeting_date, meeting_title, agenda_text, format)
                    VALUES (?, ?, ?, ?, 'markdown')
                """, (agenda_id, date, title, text))
                conn.commit()
                
                print(f"   ✅ Downloaded ({len(text):,} characters)")
                success_count += 1
            else:
                print(f"   ⚠️  Downloaded but text too short ({len(text) if text else 0} chars)")
                error_count += 1
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            error_count += 1
            continue
    
    print("\n" + "=" * 80)
    print(f"\n✅ Download complete!")
    print(f"   Success: {success_count}")
    print(f"   Errors: {error_count}")
    print(f"   Total in database: {success_count}")
    
    # Test full-text search
    print("\n🔍 Testing full-text search...")
    cursor.execute("""
        SELECT agenda_id, meeting_title, snippet(agenda_search, 2, '**', '**', '...', 40)
        FROM agenda_search
        WHERE agenda_search MATCH 'regenerative'
        LIMIT 3
    """)
    
    results = cursor.fetchall()
    if results:
        print(f"   Found {len(results)} mentions of 'regenerative':")
        for agenda_id, title, snippet in results:
            print(f"\n   📄 {title}")
            print(f"      {snippet}")
    else:
        print("   No results (may need to rebuild FTS index)")
    
    conn.close()
    
    print("\n✅ All agendas cached locally!")
    print(f"   Database: {DB_PATH}")
    print(f"   Use: town_hall_search.py (now searches local DB)")

if __name__ == '__main__':
    try:
        download_all_agendas()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
