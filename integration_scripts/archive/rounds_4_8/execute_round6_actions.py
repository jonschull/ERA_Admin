#!/usr/bin/env python3
"""
Execute Round 6 actions from CSV.
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
CSV_PATH = SCRIPT_DIR / "phase4b2_approvals_20251020185853.csv"

print("\n" + "=" * 80)
print("PHASE 4B-2 ROUND 6: EXECUTE ACTIONS")
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
# PART 0: FIX PAULO'S NAME IN AIRTABLE (Remove "(FTA)")
# ============================================================================

print("\n" + "=" * 80)
print("🔧 FIXING AIRTABLE NAME: Paulo Carvalho")
print("=" * 80)

# Read Airtable
with open(AIRTABLE_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

# Find and fix Paulo's name
paulo_fixed = False
for row in rows:
    if row.get('Name') == 'Paulo Carvalho (FTA)':
        row['Name'] = 'Paulo Carvalho'
        row['last_modified'] = datetime.now().isoformat() + 'Z'
        paulo_fixed = True
        print(f"   ✅ Renamed: 'Paulo Carvalho (FTA)' → 'Paulo Carvalho'")
        break

if paulo_fixed:
    # Write back
    with open(AIRTABLE_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("   ✅ Airtable CSV updated")
    
    # Reload
    airtable_people = {}
    for row in rows:
        if row.get('Name'):
            airtable_people[row['Name']] = row
else:
    print("   ⏭️  Paulo already fixed or not found")

# ============================================================================
# PART 1: EXECUTE STANDARD MERGES
# ============================================================================

print("\n" + "=" * 80)
print("🔀 EXECUTING STANDARD MERGES")
print("=" * 80)

# Standard merges from CSV (including the Paulo one now with fixed name)
standard_merges = [
    ('Rob De Laet (7)', 'Rob De Laet'),
    ('Rob Lewis, northwest Washington, Salish Sea', 'Rob Lewis'),
    ('Russ Speer (9)', 'Russ Speer'),
    ('Nabil Chaibdraa', 'Nabil Chaib Draa'),
    ('Paolo Nardi', 'Paolo Nardi Fernandez'),
    ('Paulo Magalhães', 'Paulo Magalhaes'),
    ('Paulo de Carvalho', 'Paulo Carvalho'),  # Now matches fixed name
    ('Peter / Erica', 'Erica Geies'),
    ('Peter Gubbels Groundswell-West Africa', 'Peter Gubbels'),
    ('Samuel Ombeni', 'Samuell Ombeni'),  # Double L in Airtable
    ('SteveApfelbaum', 'Steve Apfelbaum'),
    ('Victoria Zelin & Jonathan Cloud', 'Victoria Zelin Cloud'),
    ('Yuri Herzfeld', 'Iuri Herzfled'),
    ('Nyaguthii', 'Nyaguthii Chege'),
    ('Patrick', 'Patrick Campbell'),
    ('Poyom', 'Poyom Boydell'),
    ('Rochelle', 'Rochelle Bell'),
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
    'Jason Theunissen',  # Not ERA-related
    'Zoom user',  # Generic name
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
    {'name': 'Nathalie Ríos', 'is_member': True, 'notes': 'ERA member from Round 6'},
    {'name': 'Niko Bertulis', 'is_member': True, 'notes': 'From "Nikko"'},
    {'name': 'Cassandra Kiki', 'is_member': True, 'notes': 'From "Sandra"'},
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
    ('ana - Panama Restoration Lab', 'Ana Calderon'),
    ('Nikko', 'Niko Bertulis'),
    ('Samuel', 'Samuell Ombeni'),  # Double L
    ('Sandra', 'Cassandra Kiki'),
    ('Thilo', 'Thilo Herbst'),
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
print("✅ ROUND 6 COMPLETE")
print("=" * 80)
print(f"\nSummary:")
print(f"   🔧 Fixed: Paulo Carvalho name (removed FTA)")
print(f"   🔀 Standard merges: {merge_count}")
print(f"   🔀 Custom merges: {custom_count}")
print(f"   🗑️  Drops: {len(drops)}")
print(f"   ➕ Added to Airtable: {len(added)}")
print(f"   📊 Total actions: {merge_count + custom_count + len(drops) + len(added) + 1}")
