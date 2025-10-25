#!/usr/bin/env python3
"""
Step 1: Process DROP decisions.

Simplest case - just delete records completely.
Run on small sample first for verification.
"""

import sqlite3
import csv
from pathlib import Path
from datetime import datetime
import shutil

DB_PATH = Path('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')
BACKUP_DIR = Path('/Users/admin/ERA_Admin/FathomInventory/backups')
PAST_DECISIONS_DIR = Path('/Users/admin/ERA_Admin/integration_scripts/past_decisions')

def load_drop_decisions():
    """Load all DROP decisions from past CSVs."""
    drops = []
    
    for csv_file in sorted(PAST_DECISIONS_DIR.glob('phase4b2_approvals_batch*.csv')):
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                fathom_name = row.get('Fathom_Name', '').strip().split('🔁')[0].strip()
                comment = row.get('Comments', '').strip().lower()
                process_this = row.get('ProcessThis', '').upper() == 'YES'
                
                if process_this and comment in ['drop', 'drop it', 'duplicate']:
                    drops.append({
                        'name': fathom_name,
                        'csv_file': csv_file.name
                    })
    
    return drops

def backup_database():
    """Create backup before changes."""
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = BACKUP_DIR / f"fathom_emails.backup_step1_drops_{timestamp}.db"
    shutil.copy2(DB_PATH, backup_path)
    print(f"💾 Backup: {backup_path.name}")
    return backup_path

def check_existence(conn, names):
    """Check which names actually exist in database."""
    cursor = conn.cursor()
    existing = []
    
    for name in names:
        cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (name,))
        if cursor.fetchone()[0] > 0:
            existing.append(name)
    
    return existing

def main():
    import sys
    
    # Load decisions
    print("=" * 70)
    print("STEP 1: Process DROP Decisions")
    print("=" * 70)
    
    all_drops = load_drop_decisions()
    print(f"\n📋 Found {len(all_drops)} DROP decisions")
    
    # Check which exist
    conn = sqlite3.connect(DB_PATH)
    existing_names = check_existence(conn, [d['name'] for d in all_drops])
    print(f"   {len(existing_names)} still exist in database")
    
    if not existing_names:
        print("\n✅ Nothing to do - all already dropped!")
        conn.close()
        return
    
    # Determine mode
    test_mode = '--test' in sys.argv
    limit = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else None
    
    if test_mode:
        limit = limit or 5
        print(f"\n🧪 TEST MODE: Processing first {limit} items")
    else:
        if limit:
            print(f"\n⚙️  Processing up to {limit} items")
        else:
            print(f"\n⚙️  Processing ALL {len(existing_names)} items")
    
    # Select items to process
    to_process = existing_names[:limit] if limit else existing_names
    
    print(f"\n📝 Will drop {len(to_process)} items:")
    for name in to_process[:10]:
        print(f"   - {name}")
    if len(to_process) > 10:
        print(f"   ... and {len(to_process) - 10} more")
    
    # Confirm
    print(f"\n⚠️  This will DELETE these {len(to_process)} records from the database.")
    response = input("Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Aborted")
        conn.close()
        return
    
    # Backup
    backup_path = backup_database()
    
    # Execute drops
    print(f"\n🗑️  Dropping records...")
    cursor = conn.cursor()
    deleted_count = 0
    
    for name in to_process:
        cursor.execute("DELETE FROM participants WHERE name = ?", (name,))
        count = cursor.rowcount
        if count > 0:
            print(f"   ✅ Deleted '{name}' ({count} records)")
            deleted_count += count
    
    conn.commit()
    print(f"\n✅ Deleted {deleted_count} total records")
    
    # Verification
    print(f"\n🔍 Verifying...")
    still_exist = check_existence(conn, to_process)
    
    if still_exist:
        print(f"⚠️  {len(still_exist)} items still exist:")
        for name in still_exist:
            print(f"   - {name}")
    else:
        print("✅ All items successfully deleted")
    
    conn.close()
    
    # Summary
    print(f"\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Processed: {len(to_process)}")
    print(f"Deleted: {deleted_count} records")
    print(f"Backup: {backup_path}")
    
    if test_mode:
        print(f"\n💡 Test successful! To process remaining items:")
        print(f"   python3 {Path(__file__).name} --limit 25")
        print(f"   python3 {Path(__file__).name}  # (process all)")

if __name__ == '__main__':
    main()
