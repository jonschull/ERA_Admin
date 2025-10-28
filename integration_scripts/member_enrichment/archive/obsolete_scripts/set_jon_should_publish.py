#!/usr/bin/env python3
"""
Set 'Jon Should publish' flag for ERA members who attended Town Halls.

These 10 people:
- Abby Karparis, Ben Rubin, Brendan McNamara, Brian Krawitz
- Chris pieper, Eduard Muller, Emmanuelle Chiche, Mahangi Munanse
- Christina Engelsgaard, David maher
"""

import sys
import csv
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'airtable'))

from pyairtable import Api
from config import AIRTABLE_CONFIG

api = Api(AIRTABLE_CONFIG['api_key'])
table = api.table(AIRTABLE_CONFIG['base_id'], AIRTABLE_CONFIG['tables']['people'])

NAMES_TO_FLAG = [
    'Abby Karparis',
    'Ben Rubin',
    'Brendan McNamara',
    'Brian Krawitz',
    'Chris pieper',
    'Eduard Muller',
    'Emmanuelle Chiche',
    'Mahangi Munanse',
    'Christina Engelsgaard',
    'David maher'
]

def load_airtable_records():
    """Load current Airtable state from CSV."""
    records = {}
    csv_path = Path(__file__).parent.parent.parent / 'airtable' / 'people_export.csv'
    
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            records[name] = {
                'id': row.get('airtable_id', ''),
                'bio': row.get('Bio', '').strip()
            }
    return records

def main():
    print("=" * 80)
    print("SETTING 'Jon Should publish' FLAGS")
    print("=" * 80)
    print()
    
    records = load_airtable_records()
    
    success_count = 0
    error_count = 0
    not_found = []
    
    for name in NAMES_TO_FLAG:
        if name not in records:
            print(f"⚠️  {name} - not found in Airtable")
            not_found.append(name)
            continue
        
        rec = records[name]
        record_id = rec['id']
        
        if not record_id:
            print(f"⚠️  {name} - no Airtable ID")
            continue
        
        try:
            table.update(record_id, {'Jon Should publish': True})
            has_bio = "has bio" if rec['bio'] else "no bio yet"
            print(f"✅ {name} - Jon Should publish set ({has_bio})")
            success_count += 1
        except Exception as e:
            print(f"❌ {name}: {e}")
            error_count += 1
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ 'Jon Should publish' flag set: {success_count}")
    
    if error_count > 0:
        print(f"❌ Errors: {error_count}")
    
    if not_found:
        print(f"\n⚠️  Not found: {len(not_found)}")
        for name in not_found:
            print(f"   - {name}")
    
    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
