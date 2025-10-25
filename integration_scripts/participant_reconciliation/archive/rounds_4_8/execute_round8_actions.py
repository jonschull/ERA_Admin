#!/usr/bin/env python3
"""
Execute Round 8 actions from CSV.
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
CSV_PATH = SCRIPT_DIR / "phase4b2_approvals_20251020200355.csv"

print("\n" + "=" * 80)
print("PHASE 4B-2 ROUND 8: EXECUTE ACTIONS")
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
# PART 1: EXECUTE STANDARD MERGES
# ============================================================================

print("\n" + "=" * 80)
print("🔀 EXECUTING STANDARD MERGES")
print("=" * 80)

# Standard merges from CSV
standard_merges = [
    ('Abbie Dusseldorp (She/her)', 'Abbie Dusseldorp'),
    ('Ananda Fitzsimmons (4)', 'Ananda Fitzsimmons'),
    ('BasHam (Ecoist)', 'Basham Zain'),
    ('Billimarie (3)', 'Billimarie Lubiano Robinson'),
    ('Beck Bio4Climate', 'Beck Mordini'),
    ('Billimarie', 'Billimarie Lubiano Robinson'),
]

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

# ============================================================================
# PART 2: EXECUTE DROPS
# ============================================================================

print("\n" + "=" * 80)
print("🗑️  EXECUTING DROPS")
print("=" * 80)

drops = [
    'Bob',  # Standard drop from CSV
]

for name in drops:
    cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (name,))
    count = cursor.fetchone()[0]
    
    if count > 0:
        cursor.execute("DELETE FROM participants WHERE name = ?", (name,))
        print(f"   ✅ Dropped '{name}' ({count} records)")

# ============================================================================
# PART 3: ADD NEW PEOPLE TO AIRTABLE
# ============================================================================

print("\n" + "=" * 80)
print("➕ ADDING NEW PEOPLE TO AIRTABLE")
print("=" * 80)

people_to_add = [
    {'name': 'Andrew Atencia', 'is_member': True, 'notes': 'Should be ERA Member'},
    {'name': 'Angelique Rodriguez', 'is_member': True, 'notes': 'ERA Member'},
    {'name': 'Anna Akpe', 'is_member': True, 'notes': 'ERA Member'},
    {'name': 'Aviv Green', 'is_member': True, 'notes': 'ERA Member'},
    {'name': 'Apryle Schneeberger', 'is_member': True, 'notes': 'ERA Member'},
    {'name': 'Arun Bangura', 'is_member': True, 'notes': 'ERA Member, link to ERA Africa'},
    {'name': 'Chris Searles', 'is_member': True, 'notes': 'Org: Biointegrity'},
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
# PART 4: MERGE CUSTOM COMMENT ITEMS
# ============================================================================

print("\n" + "=" * 80)
print("🔀 EXECUTING CUSTOM COMMENT MERGES")
print("=" * 80)

custom_merges = [
    ("Andres's iPhone (2)", 'Andres Garcia'),  # Device name
    ('Bio4Climate1 (Beck Mordini)', 'Beck Mordini'),  # Username
    ('Brendan McNamara (ORQAS)', 'Brendan McNamara'),  # Organization suffix
    ('Ana', 'Ana Calderon'),  # Single name
    ('Angelique', 'Angelique Rodriguez'),  # Single name
    ('Belize', 'Mbilizi Kalombo'),  # Nickname
    ('Belizey', 'Mbilizi Kalombo'),  # Nickname variant
    ('BioIntegrity', 'Chris Searles'),  # Organization name
    ('Brendah', 'Mbilizi Kalombo'),  # Name variant
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
# PART 5: HANDLE NEWLY ADDED PEOPLE THAT NEED MERGING
# ============================================================================

print("\n" + "=" * 80)
print("🔀 EXECUTING MERGES FOR NEWLY ADDED PEOPLE")
print("=" * 80)

newly_added_merges = [
    ('Andrew Atencia', 'Andrew Atencia'),
    ('Angelique Rodriguez', 'Angelique Rodriguez'),
    ('Anna Akpe', 'Anna Akpe'),
    ('Aviv Green', 'Aviv Green'),
]

for fathom_name, target_name in newly_added_merges:
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
    
    print(f"   ✅ {fathom_name} → {target_name} ({count} records)")

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
print("✅ ROUND 8 COMPLETE")
print("=" * 80)
print(f"\nSummary:")
print(f"   🔀 Standard merges: {merge_count}")
print(f"   🔀 Custom merges: {custom_count}")
print(f"   🔀 Newly added merges: 4")
print(f"   🗑️  Drops: {len(drops)}")
print(f"   ➕ Added to Airtable: {len(added)}")
print(f"   📊 Total actions: {merge_count + custom_count + 4 + len(drops) + len(added)}")
