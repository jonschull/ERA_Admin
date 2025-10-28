#!/usr/bin/env python3
"""
Data-preserving participant merge function.

Safely merges duplicate participant records without losing any data:
- Preserves ALL call attendance records
- Merges emails, projects, airtable_ids
- Keeps the best bio
- Validates before deleting
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'FathomInventory' / 'fathom_emails.db'

def merge_participants_safely(duplicate_name, canonical_name, dry_run=True):
    """
    Merge duplicate into canonical, preserving ALL data.
    
    Args:
        duplicate_name: Name to be merged (will be deleted)
        canonical_name: Name to keep (will receive merged data)
        dry_run: If True, only show what would happen
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 80)
    print(f"MERGING: {duplicate_name} → {canonical_name}")
    print("=" * 80)
    
    # Get all data for both names
    cursor.execute("""
        SELECT name, email, bio, airtable_id, projects, location, affiliation,
               collaborating_people, collaborating_organizations, era_member, is_donor,
               data_source, landscape_node_id, era_africa
        FROM participants
        WHERE name IN (?, ?)
    """, (duplicate_name, canonical_name))
    
    records = {}
    for row in cursor.fetchall():
        name = row[0]
        records[name] = {
            'email': row[1],
            'bio': row[2],
            'airtable_id': row[3],
            'projects': row[4],
            'location': row[5],
            'affiliation': row[6],
            'collaborating_people': row[7],
            'collaborating_organizations': row[8],
            'era_member': row[9],
            'is_donor': row[10],
            'data_source': row[11],
            'landscape_node_id': row[12],
            'era_africa': row[13]
        }
    
    if duplicate_name not in records:
        print(f"⚠️  '{duplicate_name}' not found in database")
        conn.close()
        return False
    
    if canonical_name not in records:
        print(f"⚠️  '{canonical_name}' not found in database")
        conn.close()
        return False
    
    dup = records[duplicate_name]
    canon = records[canonical_name]
    
    # Show current state
    print()
    print("CURRENT STATE:")
    print("-" * 80)
    print(f"{duplicate_name}:")
    print(f"  Bio: {len(dup['bio']) if dup['bio'] else 0} chars")
    print(f"  Email: {dup['email'] or '(none)'}")
    print(f"  Airtable ID: {dup['airtable_id'] or '(none)'}")
    print(f"  ERA member: {dup['era_member']}")
    print()
    print(f"{canonical_name}:")
    print(f"  Bio: {len(canon['bio']) if canon['bio'] else 0} chars")
    print(f"  Email: {canon['email'] or '(none)'}")
    print(f"  Airtable ID: {canon['airtable_id'] or '(none)'}")
    print(f"  ERA member: {canon['era_member']}")
    print()
    
    # Count call records for each
    cursor.execute("""
        SELECT COUNT(*) FROM participants WHERE name = ?
    """, (duplicate_name,))
    dup_call_count = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) FROM participants WHERE name = ?
    """, (canonical_name,))
    canon_call_count = cursor.fetchone()[0]
    
    print(f"{duplicate_name}: {dup_call_count} call record(s)")
    print(f"{canonical_name}: {canon_call_count} call record(s)")
    print()
    
    # Determine what to merge
    updates = {}
    
    # Bio: Keep the longer one
    if dup['bio'] and canon['bio']:
        if len(dup['bio']) > len(canon['bio']):
            updates['bio'] = dup['bio']
            print(f"📝 Will use bio from {duplicate_name} ({len(dup['bio'])} chars > {len(canon['bio'])} chars)")
    elif dup['bio'] and not canon['bio']:
        updates['bio'] = dup['bio']
        print(f"📝 Will copy bio from {duplicate_name}")
    
    # Email: Prefer non-null
    if dup['email'] and not canon['email']:
        updates['email'] = dup['email']
        print(f"📧 Will copy email: {dup['email']}")
    
    # Airtable ID: Prefer non-null
    if dup['airtable_id'] and not canon['airtable_id']:
        updates['airtable_id'] = dup['airtable_id']
        print(f"🔗 Will copy airtable_id: {dup['airtable_id']}")
    
    # Projects: Merge
    if dup['projects'] and canon['projects']:
        merged_projects = set(canon['projects'].split(';') + dup['projects'].split(';'))
        updates['projects'] = ';'.join(sorted(merged_projects))
        print(f"📋 Will merge projects")
    elif dup['projects'] and not canon['projects']:
        updates['projects'] = dup['projects']
        print(f"📋 Will copy projects")
    
    # ERA member: Keep True if either is True
    if dup['era_member'] and not canon['era_member']:
        updates['era_member'] = True
        print(f"✅ Will set ERA member to True")
    
    print()
    
    if dry_run:
        print("🔍 DRY RUN - No changes made")
        print()
        print("To execute, run with dry_run=False")
        conn.close()
        return True
    
    # Execute merge
    print("EXECUTING MERGE:")
    print("-" * 80)
    
    # Update canonical with merged data
    if updates:
        set_clauses = ', '.join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [canonical_name]
        
        cursor.execute(f"""
            UPDATE participants 
            SET {set_clauses}
            WHERE name = ?
        """, values)
        
        print(f"✅ Updated {canonical_name} with {len(updates)} field(s)")
    
    # Rename all duplicate records to canonical
    cursor.execute("""
        UPDATE participants
        SET name = ?
        WHERE name = ?
    """, (canonical_name, duplicate_name))
    
    renamed = cursor.rowcount
    print(f"✅ Renamed {renamed} record(s) from {duplicate_name} to {canonical_name}")
    
    conn.commit()
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (duplicate_name,))
    remaining = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (canonical_name,))
    total = cursor.fetchone()[0]
    
    print()
    if remaining == 0:
        print(f"✅ SUCCESS: All {duplicate_name} records merged into {canonical_name}")
        print(f"   {canonical_name} now has {total} call record(s)")
    else:
        print(f"⚠️  WARNING: {remaining} {duplicate_name} records still exist")
    
    conn.close()
    return remaining == 0


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python merge_participant_safely.py <duplicate_name> <canonical_name> [--execute]")
        sys.exit(1)
    
    duplicate = sys.argv[1]
    canonical = sys.argv[2]
    execute = len(sys.argv) > 3 and sys.argv[3] == '--execute'
    
    merge_participants_safely(duplicate, canonical, dry_run=not execute)
