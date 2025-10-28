#!/usr/bin/env python3
"""
Set era_member=True for all Town Hall attendees (non-Africa).

PRINCIPLE: ERA Member = Attended Town Hall
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'FathomInventory' / 'fathom_emails.db'

def main():
    print("=" * 80)
    print("SETTING era_member=True FOR ALL TOWN HALL ATTENDEES")
    print("=" * 80)
    print()
    print("PRINCIPLE: ERA Member = Attended Town Hall (non-Africa)")
    print()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all Town Hall attendees who are NOT flagged (excluding ERA Africa)
    cursor.execute("""
        SELECT DISTINCT p.name
        FROM participants p
        JOIN calls c ON p.call_hyperlink = c.hyperlink
        WHERE c.title LIKE '%Town Hall%'
          AND (p.era_member IS NULL OR p.era_member = 0)
          AND (p.era_africa IS NULL OR p.era_africa = 0)
        ORDER BY p.name
    """)
    
    to_flag = [row[0] for row in cursor.fetchall()]
    
    print(f"Found {len(to_flag)} Town Hall attendees not flagged as ERA members:")
    print()
    
    for i, name in enumerate(to_flag, 1):
        print(f"  {i}. {name}")
    
    print()
    input("Press Enter to proceed with flagging these people as ERA members...")
    print()
    
    # Update database
    print("Updating database...")
    
    updated = 0
    for name in to_flag:
        cursor.execute("""
            UPDATE participants 
            SET era_member = 1 
            WHERE name = ?
        """, (name,))
        updated += cursor.rowcount
    
    conn.commit()
    
    print(f"✅ Updated {updated} records")
    print()
    
    # Verify
    print("Verifying...")
    cursor.execute("""
        SELECT COUNT(DISTINCT p.name)
        FROM participants p
        JOIN calls c ON p.call_hyperlink = c.hyperlink
        WHERE c.title LIKE '%Town Hall%'
          AND (p.era_africa IS NULL OR p.era_africa = 0)
          AND (p.era_member IS NULL OR p.era_member = 0)
    """)
    
    remaining = cursor.fetchone()[0]
    
    if remaining == 0:
        print("✅ All Town Hall attendees now flagged as ERA members")
    else:
        print(f"⚠️  {remaining} Town Hall attendees still not flagged")
    
    conn.close()
    
    print()
    print("=" * 80)
    print("✅ SYNC COMPLETE")
    print("=" * 80)
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
