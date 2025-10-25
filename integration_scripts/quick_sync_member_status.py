#!/usr/bin/env python3
"""
Quick sync: Update era_member status from Airtable for already-validated participants.

Much faster than full fuzzy matching - just updates existing validated records.
"""

import sqlite3
import csv
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "FathomInventory" / "fathom_emails.db"
AIRTABLE_CSV = Path(__file__).parent.parent / "airtable" / "people_export.csv"

def main():
    print("🔄 Quick Member Status Sync")
    print("=" * 60)
    
    # Load Airtable member status
    print(f"\n📖 Loading Airtable member status...")
    airtable_members = {}
    with open(AIRTABLE_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            if name:
                is_member = row.get('era Member') == 'True'
                airtable_members[name] = is_member
    
    print(f"   ✅ Loaded {len(airtable_members)} people")
    print(f"   - {sum(1 for m in airtable_members.values() if m)} are ERA members")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get validated participants
    cursor.execute("""
        SELECT DISTINCT name
        FROM participants
        WHERE validated_by_airtable = 1
    """)
    
    validated = [row[0] for row in cursor.fetchall()]
    print(f"\n📊 Database has {len(validated)} validated participants")
    
    # Update member status
    print(f"\n🔄 Updating member status...")
    updated = 0
    changed_to_member = 0
    changed_to_non_member = 0
    
    for name in validated:
        if name in airtable_members:
            new_status = 1 if airtable_members[name] else 0
            
            # Check current status
            cursor.execute("SELECT era_member FROM participants WHERE name = ? LIMIT 1", (name,))
            row = cursor.fetchone()
            old_status = row[0] if row and row[0] is not None else 0
            
            # Update all records with this name
            cursor.execute("""
                UPDATE participants
                SET era_member = ?
                WHERE name = ?
            """, (new_status, name))
            
            if cursor.rowcount > 0:
                updated += 1
                if new_status == 1 and old_status == 0:
                    changed_to_member += 1
                elif new_status == 0 and old_status == 1:
                    changed_to_non_member += 1
    
    conn.commit()
    
    print(f"\n✅ Updated {updated} participants")
    print(f"   - Changed to member: {changed_to_member}")
    print(f"   - Changed to non-member: {changed_to_non_member}")
    
    # Final stats
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN era_member = 1 THEN 1 ELSE 0 END) as members
        FROM participants
        WHERE validated_by_airtable = 1
    """)
    
    total, members = cursor.fetchone()
    print(f"\n📊 Final validated participant status:")
    print(f"   Total: {total}")
    print(f"   Members: {members} ({members/total*100:.1f}%)")
    print(f"   Non-members: {total - members} ({(total-members)/total*100:.1f}%)")
    
    conn.close()
    print("\n✅ Sync complete!")

if __name__ == '__main__':
    main()
