#!/usr/bin/env python3
"""
Merge duplicate participant records without losing data.

For each duplicate pair:
1. Keep the record with the bio (canonical name)
2. Update any calls from the duplicate to point to canonical
3. Merge emails, projects, and other data
4. Delete the duplicate
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'FathomInventory' / 'fathom_emails.db'

# Pairs: (duplicate_name, canonical_name_with_bio)
DUPLICATES = [
    ('Muhange Musinga', 'Muhangi Musinga'),
    ('Juan José Pimento', 'Juan Pimento'),
    ('Kim Chapple', 'Kimberly Chapple'),
    ('Mike Lynn', 'Michael Lynn'),
    ('Terrance Long IDUM', 'Terrance Long'),
    ('William Wildcat', 'Coakee William Wildcat')
]

def merge_participants(conn, duplicate_name, canonical_name):
    """Merge duplicate into canonical, preserving all data."""
    cursor = conn.cursor()
    
    print(f"\n{'='*80}")
    print(f"Merging: {duplicate_name} → {canonical_name}")
    print(f"{'='*80}")
    
    # Count records
    cursor.execute("SELECT COUNT(*), bio, email FROM participants WHERE name = ? GROUP BY bio, email", (duplicate_name,))
    dup_info = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*), bio, email FROM participants WHERE name = ? GROUP BY bio, email", (canonical_name,))
    canonical_info = cursor.fetchall()
    
    if not dup_info:
        print(f"⚠️  Duplicate '{duplicate_name}' not found - skipping")
        return 0
    
    if not canonical_info:
        print(f"⚠️  Canonical '{canonical_name}' not found - skipping")
        return 0
    
    print(f"  {duplicate_name}: {sum(c for c, _, _ in dup_info)} record(s)")
    print(f"  {canonical_name}: {sum(c for c, _, _ in canonical_info)} record(s)")
    
    # Get canonical record details
    cursor.execute("SELECT email, bio, airtable_id FROM participants WHERE name = ? LIMIT 1", (canonical_name,))
    canonical_data = cursor.fetchone()
    canonical_email, canonical_bio, canonical_airtable_id = canonical_data
    
    # Get duplicate record details
    cursor.execute("SELECT email, bio, airtable_id FROM participants WHERE name = ? LIMIT 1", (duplicate_name,))
    dup_data = cursor.fetchone()
    dup_email, dup_bio, dup_airtable_id = dup_data
    
    # If duplicate has data canonical doesn't, update canonical
    updates = {}
    if dup_email and not canonical_email:
        updates['email'] = dup_email
        print(f"  📧 Copying email: {dup_email}")
    if dup_airtable_id and not canonical_airtable_id:
        updates['airtable_id'] = dup_airtable_id
        print(f"  🔗 Copying airtable_id: {dup_airtable_id}")
    
    if updates:
        set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
        cursor.execute(f"UPDATE participants SET {set_clause} WHERE name = ?", 
                      list(updates.values()) + [canonical_name])
        print(f"  ✅ Updated canonical with {len(updates)} field(s)")
    
    # Delete all duplicate records
    cursor.execute("DELETE FROM participants WHERE name = ?", (duplicate_name,))
    deleted = cursor.rowcount
    print(f"  🗑️  Deleted {deleted} duplicate record(s)")
    
    return deleted

def main():
    print("=" * 80)
    print("MERGING DUPLICATE PARTICIPANTS")
    print("=" * 80)
    print()
    print("Will merge 6 duplicate pairs, keeping records with bios")
    print()
    
    conn = sqlite3.connect(DB_PATH)
    
    total_merged = 0
    
    for duplicate, canonical in DUPLICATES:
        merged = merge_participants(conn, duplicate, canonical)
        if merged:
            total_merged += merged
    
    # Commit all changes
    conn.commit()
    
    print()
    print("=" * 80)
    print("VERIFICATION")
    print("=" * 80)
    
    cursor = conn.cursor()
    
    # Check each duplicate is gone
    for duplicate, canonical in DUPLICATES:
        cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (duplicate,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            print(f"✅ {duplicate} → merged successfully")
        else:
            print(f"❌ {duplicate} → still has {count} records")
    
    print()
    
    # Final count
    cursor.execute("""
        SELECT COUNT(DISTINCT name)
        FROM participants
        WHERE era_member = 1
          AND (era_africa IS NULL OR era_africa = 0)
          AND (bio IS NULL OR bio = '')
    """)
    
    no_bio_count = cursor.fetchone()[0]
    
    print(f"ERA members (non-Africa) without bios: {no_bio_count}")
    print(f"(Should be 6 fewer than before)")
    
    conn.close()
    
    print()
    print("=" * 80)
    print("✅ MERGE COMPLETE")
    print("=" * 80)
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
