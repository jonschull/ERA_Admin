#!/usr/bin/env python3
"""
Execute Round 5 actions from CSV.
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
CSV_PATH = SCRIPT_DIR / "phase4b2_approvals_20251020183634.csv"

print("\n" + "=" * 80)
print("PHASE 4B-2 ROUND 5: EXECUTE ACTIONS")
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

# Standard merges from CSV
standard_merges = [
    ('Katrina Jeffries (5)', 'Katrina Jeffries'),
    ('John Dennis Liu', 'John D. Liu'),
    ('Joshua Shepard', 'Joshua Sheppard'),
    ('Leticia Bernardes - explorer.land by OpenForests', 'Leticia Bernardes'),
    ('MOHAMMED ALKHALID', 'Mohammed Al Khalid'),
    ('Nabil Chaib-draa', 'Nabil Chaib Draa'),
    ('Jimmy', 'Jimmy Pryor'),
    ('Kethia', 'Kethia Calixte'),
    ('Mark', 'Mark Luckenbach'),
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

# Handle drops - Jon Schull variants and Jan Dietrick joint entries
print("\n" + "=" * 80)
print("🗑️  DROPPING DUPLICATES & JOINT ENTRIES")
print("=" * 80)

# Drop Jon Schull variants (he's already in Airtable as "Jon Schull")
jon_variants = [
    'Jon Schull, EcoRestoration Alliance',
    'Jon Schull, EcoRestoration Alliance (7)',
]

for variant in jon_variants:
    cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (variant,))
    count = cursor.fetchone()[0]
    
    if count > 0:
        cursor.execute("DELETE FROM participants WHERE name = ?", (variant,))
        print(f"   ✅ Dropped '{variant}' ({count} records) - Jon Schull already in Airtable")

# Drop Jan Dietrick & Ron Whitehurst joint entries (both already in Airtable separately)
jan_ron_variants = [
    'Jan Dietrick & Ron Whitehurst',
    'Jan Dietrick & Ron Whitehurst, BugFarm, Ventura, CA',
    'Jan Dietrick, W Ventura',
]

for variant in jan_ron_variants:
    cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (variant,))
    count = cursor.fetchone()[0]
    
    if count > 0:
        cursor.execute("DELETE FROM participants WHERE name = ?", (variant,))
        print(f"   ✅ Dropped '{variant}' ({count} records) - Jan/Ron already in Airtable separately")

# Drop Julia (standard drop from CSV)
cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", ('Julia',))
count = cursor.fetchone()[0]
if count > 0:
    cursor.execute("DELETE FROM participants WHERE name = ?", ('Julia',))
    print(f"   ✅ Dropped 'Julia' ({count} records)")

# ============================================================================
# PART 2: ADD NEW PEOPLE TO AIRTABLE
# ============================================================================

print("\n" + "=" * 80)
print("➕ ADDING NEW PEOPLE TO AIRTABLE")
print("=" * 80)

people_to_add = [
    {'name': 'Jerald Katch', 'is_member': True, 'notes': 'From "Jed Katch"'},
    {'name': 'John Magugu', 'is_member': True, 'notes': 'From "John\'s iPhone"'},
    {'name': 'Lauren Miller', 'is_member': True, 'notes': 'From "Loren Miller" (typo)'},
    {'name': 'Luc Lendrum', 'is_member': True, 'email': 'luc.lendrum@nel-i.com', 'notes': 'Organization: NEL-i https://nel-i.com/'},
    {'name': 'Mooyong Han', 'is_member': True, 'notes': 'From "Myhan"'},
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
    ('Jed Katch', 'Jerald Katch'),
    ("John's iPhone", 'John Magugu'),
    ('Juan from Panama', 'Juan Carlos Monterrey'),  # Corrected spelling
    ('Loren Miller', 'Lauren Miller'),
    ('Luc Lendrum', 'Luc Lendrum'),  # Will merge to itself after adding
    ('MC Planning', 'Rochelle Bell'),
    ('18022588598', 'Michael Mayer'),  # Phone number to person
    ('KALOMBO-MBILIZI', 'Mbilizi Kalombo'),
    ('Myhan', 'Mooyong Han'),
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
print("✅ ROUND 5 COMPLETE")
print("=" * 80)
print(f"\nSummary:")
print(f"   🔀 Standard merges: {merge_count}")
print(f"   🔀 Custom merges: {custom_count}")
print(f"   🗑️  Drops: ~10 (Jon Schull variants, Jan/Ron joint entries, Julia)")
print(f"   ➕ Added to Airtable: {len(added)}")
print(f"   📊 Total actions: {merge_count + custom_count + len(added) + 10}")
