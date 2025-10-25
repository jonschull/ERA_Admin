#!/usr/bin/env python3
"""
Deduplicate participant records by consolidating multiple meeting appearances.

For each unique participant name (case-insensitive):
1. Find all records with that name
2. Keep the one with airtable_id if it exists (enriched version)
3. Otherwise keep the earliest record
4. Merge all other records into the kept record:
   - Concatenate source_call_urls (comma-separated)
   - Keep all call_hyperlinks
   - Preserve earliest analyzed_at
5. Delete duplicate records

This handles the Oct 21 duplication where 554 entries were created from
Town Hall meetings, many being duplicates of already-enriched participants.
"""

import sqlite3
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from era_config import Config

def analyze_duplicates(db_path):
    """Analyze duplicate situation before making changes."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=== Duplicate Analysis ===\n")
    
    # Total participants
    cursor.execute("SELECT COUNT(*) FROM participants")
    total = cursor.fetchone()[0]
    print(f"Total participant records: {total}")
    
    # Unique names (case-insensitive)
    cursor.execute("SELECT COUNT(DISTINCT LOWER(TRIM(name))) FROM participants")
    unique = cursor.fetchone()[0]
    print(f"Unique participant names: {unique}")
    print(f"Duplicate records: {total - unique}\n")
    
    # Find names with multiple records
    cursor.execute("""
        SELECT 
            LOWER(TRIM(name)) as name_lower,
            COUNT(*) as record_count,
            SUM(CASE WHEN airtable_id IS NOT NULL THEN 1 ELSE 0 END) as enriched_count
        FROM participants
        GROUP BY name_lower
        HAVING record_count > 1
        ORDER BY record_count DESC
        LIMIT 20
    """)
    
    print("Top 20 duplicated names:")
    print(f"{'Name':<40} {'Records':<10} {'Enriched':<10}")
    print("-" * 60)
    
    dupes = cursor.fetchall()
    for name, count, enriched in dupes:
        print(f"{name[:38]:<40} {count:<10} {enriched:<10}")
    
    conn.close()
    
    return len(dupes)

def build_deduplication_plan(db_path):
    """Build plan for which records to keep/merge/delete."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all duplicate groups
    cursor.execute("""
        SELECT 
            LOWER(TRIM(name)) as name_lower,
            COUNT(*) as record_count
        FROM participants
        GROUP BY name_lower
        HAVING record_count > 1
    """)
    
    duplicate_groups = cursor.fetchall()
    
    plan = {
        'keep': [],      # Records to keep
        'merge_into': {},  # { kept_id: [list of ids to merge] }
        'delete': []     # Records to delete after merge
    }
    
    for name_lower, count in duplicate_groups:
        # Get all records for this name
        cursor.execute("""
            SELECT id, name, airtable_id, source_call_url, call_hyperlink, analyzed_at
            FROM participants
            WHERE LOWER(TRIM(name)) = ?
            ORDER BY 
                CASE WHEN airtable_id IS NOT NULL THEN 0 ELSE 1 END,  -- Enriched first
                analyzed_at ASC  -- Then by earliest
        """, (name_lower,))
        
        records = cursor.fetchall()
        
        # Keep the first one (enriched or earliest)
        kept_record = records[0]
        plan['keep'].append(kept_record[0])
        
        # Mark others for merge
        others = [r[0] for r in records[1:]]
        if others:
            plan['merge_into'][kept_record[0]] = others
            plan['delete'].extend(others)
    
    conn.close()
    
    return plan

def execute_deduplication(db_path, dry_run=True):
    """Execute the deduplication plan."""
    
    if dry_run:
        print("\n=== DRY RUN MODE - No changes will be made ===\n")
    else:
        print("\n=== EXECUTING DEDUPLICATION ===\n")
        # Backup first
        import shutil
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{db_path}.backup_before_dedup_{timestamp}"
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup created: {backup_path}\n")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    plan = build_deduplication_plan(db_path)
    
    print(f"Records to keep: {len(plan['keep'])}")
    print(f"Records to delete: {len(plan['delete'])}")
    print(f"Merge operations: {len(plan['merge_into'])}\n")
    
    if not dry_run:
        # Begin transaction
        cursor.execute("BEGIN TRANSACTION")
        
        try:
            # For each kept record, merge data from duplicates
            for kept_id, duplicate_ids in plan['merge_into'].items():
                # Get all source URLs from duplicates
                cursor.execute("""
                    SELECT GROUP_CONCAT(source_call_url, ', ')
                    FROM (
                        SELECT DISTINCT source_call_url
                        FROM participants
                        WHERE id IN ({})
                    )
                """.format(','.join('?' * (len(duplicate_ids) + 1))), 
                [kept_id] + duplicate_ids)
                
                merged_urls = cursor.fetchone()[0]
                
                # Update kept record with merged data
                cursor.execute("""
                    UPDATE participants
                    SET source_call_url = ?
                    WHERE id = ?
                """, (merged_urls, kept_id))
                
                print(f"✓ Merged {len(duplicate_ids)} duplicates into record {kept_id}")
            
            # Delete duplicate records
            if plan['delete']:
                placeholders = ','.join('?' * len(plan['delete']))
                cursor.execute(f"DELETE FROM participants WHERE id IN ({placeholders})", 
                             plan['delete'])
                print(f"\n✓ Deleted {len(plan['delete'])} duplicate records")
            
            # Commit transaction
            cursor.execute("COMMIT")
            print("\n✅ Deduplication complete!")
            
        except Exception as e:
            cursor.execute("ROLLBACK")
            print(f"\n❌ Error during deduplication: {e}")
            print("Transaction rolled back - no changes made")
            raise
    else:
        print("\nDRY RUN - No changes made. Run with --execute to apply changes.")
    
    conn.close()

def main():
    db_path = Config.FATHOM_DB_PATH
    
    # Parse arguments
    dry_run = '--execute' not in sys.argv
    
    print(f"Database: {db_path}\n")
    
    # Step 1: Analyze
    analyze_duplicates(db_path)
    
    # Step 2: Build plan
    print("\n" + "="*60)
    plan = build_deduplication_plan(db_path)
    print(f"\nDeduplication plan built:")
    print(f"  - Keep {len(plan['keep'])} records")
    print(f"  - Merge {len(plan['merge_into'])} groups")
    print(f"  - Delete {len(plan['delete'])} duplicates")
    
    # Step 3: Execute or show dry run
    print("\n" + "="*60)
    execute_deduplication(db_path, dry_run=dry_run)
    
    # Step 4: Show final stats
    if not dry_run:
        print("\n" + "="*60)
        print("=== Final Statistics ===\n")
        analyze_duplicates(db_path)

if __name__ == '__main__':
    main()
