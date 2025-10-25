#!/usr/bin/env python3
"""
Execute Round 4 actions from CSV.
"""

import sqlite3
import csv
import sys
from pathlib import Path
from datetime import datetime
import shutil

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from add_to_airtable import add_people_to_airtable, update_fathom_validated

# Paths
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent / "FathomInventory" / "fathom_emails.db"
BACKUP_DIR = SCRIPT_DIR.parent / "FathomInventory" / "backups"
AIRTABLE_CSV = SCRIPT_DIR.parent / "airtable" / "people_export.csv"
CSV_PATH = SCRIPT_DIR / "phase4b2_approvals_20251020181148.csv"

print("\n" + "=" * 80)
print("PHASE 4B-2 ROUND 4: EXECUTE ACTIONS")
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

# ============================================================================
# PART 1: EXECUTE STANDARD MERGES + DROP
# ============================================================================

print("\n" + "=" * 80)
print("🔀 EXECUTING STANDARD MERGES")
print("=" * 80)

# Parse CSV for standard merges and drops
standard_merges = []
drops = []

with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('ProcessThis', '').upper() != 'YES':
            continue
        
        comment = row.get('Comments', '').strip()
        fathom_name = row['Fathom_Name']
        
        # Skip custom comments for now
        if not (comment.lower().startswith('merge with:') or 
                comment.lower().startswith('drop')):
            continue
        
        if comment.lower().startswith('merge with:'):
            target_name = comment.split('merge with:', 1)[1].strip()
            standard_merges.append((fathom_name, target_name))
        elif comment.lower().startswith('drop'):
            drops.append(fathom_name)

merge_count = 0
for fathom_name, target_name in standard_merges:
    if target_name not in airtable_people:
        print(f"   ⚠️  '{target_name}' not in Airtable - skipping '{fathom_name}'")
        continue
    
    cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (fathom_name,))
    count = cursor.fetchone()[0]
    
    if count == 0:
        print(f"   ⏭️  '{fathom_name}' - Already processed")
        continue
    
    cursor.execute("""
        UPDATE participants
        SET name = ?,
            validated_by_airtable = 1,
            era_member = 1
        WHERE name = ?
    """, (target_name, fathom_name))
    
    merge_count += 1
    print(f"   ✅ {fathom_name} → {target_name} ({count} records)")

print(f"\n✅ Standard merges: {merge_count}/{len(standard_merges)}")

# Execute drops
print("\n" + "=" * 80)
print("🗑️  EXECUTING DROPS")
print("=" * 80)

for name in drops:
    cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (name,))
    count = cursor.fetchone()[0]
    
    if count > 0:
        cursor.execute("DELETE FROM participants WHERE name = ?", (name,))
        print(f"   ✅ Dropped '{name}' ({count} records)")

# ============================================================================
# PART 2: ADD NEW PEOPLE TO AIRTABLE
# ============================================================================

print("\n" + "=" * 80)
print("➕ ADDING NEW PEOPLE TO AIRTABLE")
print("=" * 80)

people_to_add = [
    {'name': 'Frank van Schoubroeck', 'is_member': True, 'notes': 'From Round 4 custom comment'},
    {'name': 'Haley Kraczek', 'is_member': True, 'email': 'hnkraczek@gmail.com', 'notes': 'From Round 4 custom comment'},
    {'name': 'Muhange Musinga', 'is_member': True, 'notes': 'Maps to Flip Town and Fliptown Ubuntu DAO'},
    {'name': 'Joshua Shephard', 'is_member': True, 'notes': 'Maps to JS initials'},
]

added, skipped = add_people_to_airtable(people_to_add, conn)
if added:
    update_fathom_validated(added, conn)
    # Reload Airtable
    with open(AIRTABLE_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        airtable_people = {row['Name']: row for row in reader if row.get('Name')}

print(f"\n✅ Added {len(added)} people to Airtable")

# ============================================================================
# PART 3: MERGE CUSTOM COMMENT ITEMS
# ============================================================================

print("\n" + "=" * 80)
print("🔀 EXECUTING CUSTOM COMMENT MERGES")
print("=" * 80)

custom_merges = [
    ('Ana C', 'Ana Calderon'),
    ('Flip Town', 'Muhange Musinga'),
    ('Fliptown Ubuntu DAO', 'Muhange Musinga'),
    ('JS', 'Joshua Shephard'),
]

custom_count = 0
for fathom_name, target_name in custom_merges:
    cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (fathom_name,))
    count = cursor.fetchone()[0]
    
    if count == 0:
        print(f"   ⏭️  '{fathom_name}' - Already processed")
        continue
    
    cursor.execute("""
        UPDATE participants
        SET name = ?,
            validated_by_airtable = 1,
            era_member = 1
        WHERE name = ?
    """, (target_name, fathom_name))
    
    custom_count += 1
    print(f"   ✅ {fathom_name} → {target_name} ({count} records)")

print(f"\n✅ Custom merges: {custom_count}/{len(custom_merges)}")

# ============================================================================
# COMMIT AND FINAL STATS
# ============================================================================

conn.commit()
print("\n" + "=" * 80)
print("✅ ALL CHANGES COMMITTED")
print("=" * 80)

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
print("✅ ROUND 4 COMPLETE")
print("=" * 80)
print(f"\nSummary:")
print(f"   🔀 Standard merges: {merge_count}")
print(f"   🔀 Custom merges: {custom_count}")
print(f"   🗑️  Drops: {len(drops)}")
print(f"   ➕ Added to Airtable: {len(added)}")
print(f"   📊 Total actions: {merge_count + custom_count + len(drops) + len(added)}")
