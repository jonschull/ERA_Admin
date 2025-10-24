#!/usr/bin/env python3
"""
Preview what probe_assistant will show for probe cases.
Shows Town Hall context without interactive prompts.
"""

import sqlite3
from town_hall_search import TownHallSearch

DB_PATH = '../FathomInventory/fathom_emails.db'

def preview_case(name):
    """Preview context available for this person."""
    
    print(f"\n{'='*80}")
    print(f"PROBE CASE: {name}")
    print('='*80)
    
    # Get meeting info from DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT source_call_title, analyzed_at, COUNT(*) as appearances
        FROM participants
        WHERE name = ?
        GROUP BY source_call_title
    """, (name,))
    
    meetings = cursor.fetchall()
    if meetings:
        print(f"\nFathom Meetings ({len(meetings)} different):")
        for title, date, count in meetings:
            print(f"  • {title} ({date}) - {count}x")
    
    # Search Town Hall
    searcher = TownHallSearch(use_local_db=True)
    results = searcher.search_agendas_for_name(name, max_results=3)
    
    if results:
        print(f"\n📚 Town Hall Context ({len(results)} agendas):")
        for r in results:
            print(f"\n  📄 {r['title']} ({r['date']})")
            snippet = r['snippet'].replace('\n', ' ')
            if len(snippet) > 200:
                snippet = snippet[:200] + '...'
            print(f"     {snippet}")
    else:
        print(f"\n❌ Not found in Town Hall agendas")
    
    # Check Airtable
    cursor.execute("""
        SELECT COUNT(*) FROM participants 
        WHERE name = ? AND validated_by_airtable = 1
    """, (name,))
    in_airtable = cursor.fetchone()[0] > 0
    
    print(f"\n💡 Status: {'✅ Already in Airtable' if in_airtable else '❌ Not in Airtable'}")
    
    conn.close()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # Preview specific names
        for name in sys.argv[1:]:
            preview_case(name)
    else:
        # Preview test cases
        names = ["Mike Lynn", "Victoria Zelin-Cloud", "sustainavistas"]
        for name in names:
            preview_case(name)
        
        print(f"\n{'='*80}")
        print("To preview other names: python3 preview_probe_cases.py 'Name 1' 'Name 2'")
        print('='*80)
