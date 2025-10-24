#!/usr/bin/env python3
"""
Process approved matches from exported CSV.
Executes user-approved actions:
1. Delete "drop" entries from Fathom
2. Add manual matches
3. Enrich approved matches
"""

import sys
import csv
import sqlite3
from pathlib import Path
from datetime import datetime

# Import from main script
sys.path.insert(0, str(Path(__file__).parent))
from phase4b1_enrich_from_airtable import (
    get_db_connection,
    verify_database_integrity,
    load_airtable_data,
    require_backup,
    add_enrichment_columns,
    delete_fathom_participants,
    enrich_participants
)

# Configuration
CSV_PATH = Path("/Users/admin/Downloads/phase4b1_approvals_2025-10-19 (2).csv")
DB_PATH = Path("/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db")

# Names to delete (from "drop" comments)
DROP_NAMES = [
    "Abdulganiyu Jimoh",
    "Abdulganiyu Jimoh (2)",
    "Abdulganiyu Jimoh (3)",
    "Abdulganiyu Jimoh (4)",
    "Nikko",
    "admin",
    "Brendah",
    "Bianca",
    "Julia"
]

# Manual match: Rolanda → Ansima Casinga Rolande
MANUAL_MATCHES = {
    "Rolanda": "Ansima Casinga Rolande"
}


def parse_csv_approvals(csv_path, airtable_people):
    """Parse CSV and return approved matches."""
    print(f"\n📖 Parsing CSV approvals: {csv_path}")
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    approved = []
    rejected = []
    
    for row in rows:
        if row['APPROVED'].upper() == 'YES':
            approved.append(row)
        else:
            rejected.append(row)
    
    print(f"✅ Parsed CSV")
    print(f"   - Total rows: {len(rows)}")
    print(f"   - Approved: {len(approved)}")
    print(f"   - Rejected: {len(rejected)}")
    
    # Build matches dict
    matches = {}
    for row in approved:
        fathom_name = row['Fathom_Name']
        airtable_name = row['Airtable_Name']
        
        # Find airtable person
        airtable_person = next((p for p in airtable_people if p['name'] == airtable_name), None)
        
        if airtable_person:
            matches[fathom_name] = {
                'airtable_person': airtable_person,
                'fathom_data': {
                    'name': fathom_name,
                    'video_urls': row['Video_URLs'].split(' | ') if row['Video_URLs'] else []
                },
                'score': int(row['Score'].replace('%', ''))
            }
    
    return matches


def add_manual_matches(matches, manual_dict, airtable_people):
    """Add manual matches to the approved set."""
    print(f"\n➕ Adding {len(manual_dict)} manual matches...")
    
    for fathom_name, airtable_name in manual_dict.items():
        # Find airtable person
        airtable_person = next((p for p in airtable_people if p['name'] == airtable_name), None)
        
        if airtable_person:
            matches[fathom_name] = {
                'airtable_person': airtable_person,
                'fathom_data': {
                    'name': fathom_name,
                    'video_urls': []
                },
                'score': 100  # Manual match = 100%
            }
            print(f"   ✓ {fathom_name} → {airtable_name}")
        else:
            print(f"   ✗ '{airtable_name}' not found in Airtable!")
    
    return matches


def main():
    print()
    print("=" * 60)
    print("PHASE 4B-1: PROCESS APPROVED MATCHES")
    print("=" * 60)
    print()
    print(f"CSV: {CSV_PATH}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # STEP 1: Connect
    conn = get_db_connection()
    verify_database_integrity(conn)
    
    # STEP 2: Load Airtable data
    airtable_people = load_airtable_data()
    
    # STEP 3: Parse CSV approvals
    matches = parse_csv_approvals(CSV_PATH, airtable_people)
    
    # STEP 4: Add manual matches
    matches = add_manual_matches(matches, MANUAL_MATCHES, airtable_people)
    
    print()
    print(f"📊 Total approved matches: {len(matches)}")
    print()
    
    # STEP 5: Create backup
    require_backup()
    
    # STEP 6: DELETE drop entries
    try:
        conn.execute("BEGIN TRANSACTION")
        delete_fathom_participants(conn, DROP_NAMES)
        conn.commit()
        print("✅ Deletions committed")
    except Exception as e:
        conn.rollback()
        print(f"❌ ERROR deleting entries: {e}")
        conn.close()
        sys.exit(1)
    
    # STEP 7: Add enrichment columns
    try:
        conn.execute("BEGIN TRANSACTION")
        add_enrichment_columns(conn)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"❌ ERROR adding columns: {e}")
        conn.close()
        sys.exit(1)
    
    # STEP 8: Enrich approved matches
    try:
        conn.execute("BEGIN TRANSACTION")
        stats, corrections = enrich_participants(conn, matches)
        conn.commit()
        print("\n✅ Database modifications committed successfully")
    except Exception as e:
        conn.rollback()
        print(f"\n❌ ERROR during enrichment: {e}")
        print("Transaction rolled back - database unchanged")
        conn.close()
        sys.exit(1)
    finally:
        conn.close()
    
    print()
    print("=" * 60)
    print("COMPLETE!")
    print("=" * 60)
    print(f"✅ Deleted: {len(DROP_NAMES)} participants")
    print(f"✅ Enriched: {len(matches)} participants")
    print(f"   - Name corrections: {stats['name_corrections']}")
    print(f"   - Members identified: {stats['members_identified']}")
    print(f"   - Donors identified: {stats['donors_identified']}")
    print()


if __name__ == "__main__":
    main()
