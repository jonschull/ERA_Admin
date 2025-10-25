#!/usr/bin/env python3
"""
Execute Round 3 actions from CSV.
"""

import sqlite3
import csv
from pathlib import Path
from datetime import datetime
import shutil

# Paths
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent / "FathomInventory" / "fathom_emails.db"
BACKUP_DIR = SCRIPT_DIR.parent / "FathomInventory" / "backups"
AIRTABLE_CSV = SCRIPT_DIR.parent / "airtable" / "people_export.csv"
CSV_PATH = SCRIPT_DIR / "phase4b2_approvals_20251020172426.csv"

print("\n" + "=" * 80)
print("PHASE 4B-2 ROUND 3: EXECUTE ACTIONS")
print("=" * 80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Backup database
BACKUP_DIR.mkdir(exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M')
backup_path = BACKUP_DIR / f"fathom_emails.backup_{timestamp}.db"
shutil.copy2(DB_PATH, backup_path)
print(f"\n💾 Database backup: {backup_path.name}")

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Load Airtable people
airtable_people = {}
with open(AIRTABLE_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('Name'):
            airtable_people[row['Name']] = row

print(f"✅ Loaded {len(airtable_people)} people from Airtable")

# Parse CSV for merges
merges = []
with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('ProcessThis', '').upper() != 'YES':
            continue
        
        comment = row.get('Comments', '').strip()
        if 'merge with:' in comment.lower():
            fathom_name = row['Fathom_Name']
            target_name = comment.split('merge with:', 1)[1].strip()
            merges.append((fathom_name, target_name))

print(f"\n📋 Found {len(merges)} merges to execute")

# Execute merges
print("\n" + "=" * 80)
print("🔀 EXECUTING MERGES")
print("=" * 80)

merge_count = 0
skipped = []

for fathom_name, target_name in merges:
    # Check if target exists in Airtable
    if target_name not in airtable_people:
        print(f"   ⚠️  '{target_name}' not in Airtable - skipping '{fathom_name}'")
        skipped.append((fathom_name, target_name))
        continue
    
    # Get record count
    cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (fathom_name,))
    count = cursor.fetchone()[0]
    
    if count == 0:
        print(f"   ⏭️  '{fathom_name}' - Already processed or doesn't exist")
        continue
    
    # Execute merge: rename to target and mark validated
    cursor.execute("""
        UPDATE participants
        SET name = ?,
            validated_by_airtable = 1,
            era_member = 1
        WHERE name = ?
    """, (target_name, fathom_name))
    
    merge_count += 1
    print(f"   ✅ Merged '{fathom_name}' → '{target_name}' ({count} records)")

print(f"\n✅ Merged: {merge_count}/{len(merges)}")

if skipped:
    print(f"\n⚠️  Skipped {len(skipped)} merges (targets not in Airtable):")
    for fathom, target in skipped:
        print(f"   • {fathom} → {target}")

# Commit changes
conn.commit()
print("\n" + "=" * 80)
print("✅ ALL CHANGES COMMITTED")
print("=" * 80)

# Final stats
cursor.execute("""
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN validated_by_airtable = 1 THEN 1 ELSE 0 END) as validated,
        SUM(CASE WHEN validated_by_airtable = 0 THEN 1 ELSE 0 END) as remaining
    FROM participants
""")
total, validated, remaining = cursor.fetchone()

print(f"\n📊 DATABASE STATUS:")
print(f"   Total: {total}")
print(f"   Validated: {validated}")
print(f"   Remaining: {remaining}")

conn.close()

print("\n" + "=" * 80)
print("✅ ROUND 3 COMPLETE")
print("=" * 80)
