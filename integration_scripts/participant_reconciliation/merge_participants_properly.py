#!/usr/bin/env python3
"""
Properly merge participant variants while preserving attendance records.

Key logic:
- If target already has record for same meeting → DELETE variant (true duplicate)
- If target doesn't have record for that meeting → UPDATE variant name (preserve attendance)
"""

import sqlite3
import csv
from pathlib import Path
from fuzzywuzzy import fuzz

DB_PATH = Path(__file__).parent.parent / 'FathomInventory' / 'fathom_emails.db'
PAST_DECISIONS_DIR = Path(__file__).parent / 'past_decisions'

def load_airtable_names():
    """Load validated names from Airtable."""
    airtable_csv = Path(__file__).parent.parent / 'airtable' / 'people_export.csv'
    names = set()
    with open(airtable_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            if name:
                names.add(name)
    return names

def find_target_in_db(target_name, cursor):
    """Find actual target name in database (handles typos/variations)."""
    # Try exact match first
    cursor.execute("SELECT DISTINCT name FROM participants WHERE name = ?", (target_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    
    # Try fuzzy match >90%
    cursor.execute("SELECT DISTINCT name FROM participants WHERE validated_by_airtable = 1")
    validated_names = [row[0] for row in cursor.fetchall()]
    
    best_match = None
    best_score = 0
    for valid_name in validated_names:
        score = fuzz.ratio(target_name.lower(), valid_name.lower())
        if score > best_score:
            best_score = score
            best_match = valid_name
    
    if best_score > 90:
        return best_match
    
    return None

def merge_participant(conn, variant_name, target_name):
    """
    Merge variant → target preserving attendance records.
    
    Returns: (updated_count, deleted_count)
    """
    cursor = conn.cursor()
    
    # Find actual target name in DB
    actual_target = find_target_in_db(target_name, cursor)
    if not actual_target:
        print(f"   ⚠️  Target '{target_name}' not found in DB - skipping {variant_name}")
        return (0, 0)
    
    # Get all variant records
    cursor.execute("""
        SELECT id, source_call_url, source_call_title, call_hyperlink
        FROM participants
        WHERE name = ?
    """, (variant_name,))
    
    variant_records = cursor.fetchall()
    if not variant_records:
        return (0, 0)
    
    updated = 0
    deleted = 0
    
    # Process each variant record individually
    for variant_id, call_url, call_title, call_hyperlink in variant_records:
        # Check if target already has a record for THIS SPECIFIC meeting
        # Match by hyperlink (most unique identifier)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM participants 
            WHERE name = ? 
              AND call_hyperlink = ?
        """, (actual_target, call_hyperlink))
        
        target_has_this_meeting = cursor.fetchone()[0] > 0
        
        if target_has_this_meeting:
            # Target already has this meeting - delete variant record (true duplicate)
            cursor.execute("DELETE FROM participants WHERE id = ?", (variant_id,))
            deleted += 1
        else:
            # Target doesn't have this meeting - update variant to target name (preserves attendance)
            # First check if target name exists at all
            cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (actual_target,))
            if cursor.fetchone()[0] == 0:
                # Target doesn't exist - safe to update
                cursor.execute("""
                    UPDATE participants 
                    SET name = ?,
                        validated_by_airtable = 1
                    WHERE id = ?
                """, (actual_target, variant_id))
                updated += 1
            else:
                # Target exists but doesn't have THIS meeting
                # Update this specific record (UNIQUE constraint won't fire because we're updating single record)
                try:
                    cursor.execute("""
                        UPDATE participants 
                        SET name = ?,
                            validated_by_airtable = 1
                        WHERE id = ?
                    """, (actual_target, variant_id))
                    updated += 1
                except sqlite3.IntegrityError:
                    # Shouldn't happen, but if it does, delete
                    cursor.execute("DELETE FROM participants WHERE id = ?", (variant_id,))
                    deleted += 1
    
    action = f"Updated: {updated}, Deleted: {deleted}" if updated + deleted > 0 else "No changes"
    print(f"   ✅ {variant_name} → {actual_target}: {action}")
    
    return (updated, deleted)

def main():
    print("=" * 80)
    print("PROPER MERGE: Preserving Attendance Records")
    print("=" * 80)
    
    # Load past decisions
    print("\n📖 Loading past decisions...")
    merges = []
    drops = []
    
    for csv_file in sorted(PAST_DECISIONS_DIR.glob('phase4b2_approvals_batch*.csv')):
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                fathom_name = row.get('Fathom_Name', '').strip().split('🔁')[0].strip()
                if not fathom_name:
                    continue
                    
                process_this = row.get('ProcessThis', '').upper() == 'YES'
                if not process_this:
                    continue
                
                comment = row.get('Comments', '').strip()
                
                if comment.startswith('merge with:'):
                    target = comment[len('merge with:'):].strip()
                    merges.append((fathom_name, target))
                elif comment.lower() in ['drop', 'drop it', 'duplicate']:
                    drops.append(fathom_name)
    
    print(f"   Found {len(merges)} merges, {len(drops)} drops")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Process merges
        print(f"\n🔀 Processing {len(merges)} merges...")
        total_updated = 0
        total_deleted = 0
        
        for variant_name, target_name in merges:
            updated, deleted = merge_participant(conn, variant_name, target_name)
            total_updated += updated
            total_deleted += deleted
        
        print(f"\n   Total: {total_updated} records updated, {total_deleted} duplicates deleted")
        
        # Process drops
        print(f"\n🗑️  Processing {len(drops)} drops...")
        cursor = conn.cursor()
        drop_count = 0
        
        for drop_name in drops:
            cursor.execute("DELETE FROM participants WHERE name = ?", (drop_name,))
            if cursor.rowcount > 0:
                print(f"   ✅ Dropped: {drop_name} ({cursor.rowcount} records)")
                drop_count += cursor.rowcount
        
        print(f"\n   Total: {drop_count} records dropped")
        
        # Commit
        conn.commit()
        print("\n✅ All changes committed")
        
        # Final stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN source_call_title LIKE '%Town Hall%' THEN 1 ELSE 0 END) as th_participants,
                SUM(CASE WHEN validated_by_airtable = 1 THEN 1 ELSE 0 END) as validated
            FROM participants
        """)
        
        total, th_participants, validated = cursor.fetchone()
        
        print("\n" + "=" * 80)
        print("📊 FINAL STATUS")
        print("=" * 80)
        print(f"   Total participants: {total}")
        print(f"   TH participants: {th_participants}")
        print(f"   Validated: {validated}")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == '__main__':
    main()
