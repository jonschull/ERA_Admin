#!/usr/bin/env python3
"""
Execute Round 2 actions - all 25 items from CSV + probe resolutions.
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

print("\n" + "=" * 80)
print("PHASE 4B-2 ROUND 2: EXECUTE ALL ACTIONS")
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
# PART 1: ADD TO AIRTABLE (2 people)
# ============================================================================

print("\n" + "=" * 80)
print("➕ ADDING PEOPLE TO AIRTABLE")
print("=" * 80)

people_to_add = [
    {'name': 'Mtokani Saleh', 'is_member': True, 'notes': 'ERA Africa member'},
    {'name': 'Karim Camara', 'is_member': True, 'notes': 'ERA Africa member'},
]

added, skipped = add_people_to_airtable(people_to_add, conn)
if added:
    update_fathom_validated(added, conn)
    # Reload Airtable to get new people
    with open(AIRTABLE_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        airtable_people = {row['Name']: row for row in reader if row.get('Name')}

print(f"\n✅ Added {len(added)} people to Airtable")

# ============================================================================
# PART 2: MERGE FATHOM RECORDS (4 custom + 18 from CSV = 22 merges)
# ============================================================================

print("\n" + "=" * 80)
print("🔀 EXECUTING MERGES")
print("=" * 80)

# Custom merges from probe resolutions
custom_merges = [
    ('Ed', 'Ed Huling'),
    ('Mtokani', 'Mtokani Saleh'),
    ('Charles', 'Charles Upton'),
]

# Standard merges from CSV
csv_merges = [
    ('Philip Bogdonoff, Bio4Climate.org', 'Philip Bogdonoff'),
    ('Eliza Herald (3)', 'Eliza Herald'),
    ('Leonard IYAMUREME', 'Leonard Iyamuremye'),
    ('Folorunsho Dayo Oluwafemi', 'Folorunso Dayo Oluwafemi'),
    ('mbilizi Kalombo', 'Mbilizi Kalombo'),
    ('Dr Brian von Herzen', 'Brian Von Herzen'),
    ('Benamara Elhabib', 'Elhabib Benamara'),
    ('Leonard', 'Leonard Iyamuremye'),
    ('Rob de Laet', 'Rob de Laet'),
    ('William Wildcat', 'William Wildcat'),
    ('Daniel Langfitt', 'Daniel Langfitt'),
    ('MARIUS IRAGI', 'Marius Iragi'),
    ('MUTASA BRIAN', 'Brian Mutasa'),
    ('Rodger', 'Rodger Payne'),
    ('Ansiima Casinga Rolande', 'Ansiima Rolande'),
    ('Cole', 'Cole Davis'),
    ('George Karwani-Tanzania', 'George Karwani'),
    ('Joshua Konkankoh', 'Konkankoh Joshua'),
]

all_merges = custom_merges + csv_merges

merge_count = 0
for fathom_name, target_name in all_merges:
    # Check if target exists in Airtable
    if target_name not in airtable_people:
        print(f"   ⚠️  '{target_name}' not in Airtable - skipping '{fathom_name}'")
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

print(f"\n✅ Merged: {merge_count}/{len(all_merges)}")

# ============================================================================
# PART 3: DROP ORGANIZATIONS & LINK TO PEOPLE (2 drops)
# ============================================================================

print("\n" + "=" * 80)
print("🗑️  DROPPING ORGANIZATIONS (linking to people)")
print("=" * 80)

# 1. Global Earth Repair → Michael Pilarski
cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", ('Global Earth Repair',))
ger_count = cursor.fetchone()[0]

if ger_count > 0:
    cursor.execute("""
        DELETE FROM participants
        WHERE name = 'Global Earth Repair'
    """)
    print(f"   ✅ Dropped 'Global Earth Repair' ({ger_count} records)")
    print(f"      Note: Organization belongs to Michael Pilarski (already in Airtable)")
else:
    print(f"   ⏭️  'Global Earth Repair' - Already processed")

# 2. sustainavistas → Grant Holton
cursor.execute("SELECT COUNT(*) FROM participants WHERE name LIKE 'sustainavistas%'")
sv_count = cursor.fetchone()[0]

if sv_count > 0:
    cursor.execute("""
        DELETE FROM participants
        WHERE name LIKE 'sustainavistas%'
    """)
    print(f"   ✅ Dropped 'sustainavistas' variants ({sv_count} records)")
    print(f"      Note: Organization belongs to Grant Holton (already in Airtable)")
else:
    print(f"   ⏭️  'sustainavistas' - Already processed")

# ============================================================================
# COMMIT ALL CHANGES
# ============================================================================

conn.commit()
print("\n" + "=" * 80)
print("✅ ALL ACTIONS COMMITTED TO DATABASE")
print("=" * 80)

# ============================================================================
# FINAL STATS
# ============================================================================

print("\n" + "=" * 80)
print("📊 FINAL DATABASE STATUS")
print("=" * 80)

cursor.execute("""
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN validated_by_airtable = 1 THEN 1 ELSE 0 END) as validated,
        SUM(CASE WHEN validated_by_airtable = 0 THEN 1 ELSE 0 END) as remaining
    FROM participants
""")
total, validated, remaining = cursor.fetchone()

print(f"   Total participants: {total}")
print(f"   Validated: {validated}")
print(f"   Remaining: {remaining}")

conn.close()

print("\n" + "=" * 80)
print("✅ ROUND 2 COMPLETE")
print("=" * 80)
print(f"\nSummary:")
print(f"   ➕ Added to Airtable: {len(added)}")
print(f"   🔀 Merged: {merge_count}")
print(f"   🗑️  Dropped: 2 organizations")
print(f"   📊 Total actions: {len(added) + merge_count + 2}")
