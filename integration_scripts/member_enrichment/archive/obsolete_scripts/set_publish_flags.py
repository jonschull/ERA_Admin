#!/usr/bin/env python3
"""
Set Publish flag for ERA members who attended Town Halls.

Members to flag:
- Abby Karparis, Ben Rubin, Brendan McNamara, Brian Krawitz
- Chris pieper, Eduard Muller, Emmanuelle Chiche, Mahangi Munanse
- Christina Engelsgaard, David maher (just added to first TH)
"""

import sys
import csv
from pathlib import Path

# Add airtable module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'airtable'))

try:
    from pyairtable import Api
    from config import AIRTABLE_CONFIG
    AIRTABLE_AVAILABLE = True
except ImportError:
    AIRTABLE_AVAILABLE = False
    print("⚠️  WARNING: pyairtable or config not available")
    sys.exit(1)

# Names to flag for publishing
NAMES_TO_PUBLISH = [
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
                'publish': row.get('Publish', ''),
                'era_member': row.get('era Member', ''),
                'bio': row.get('Bio', '').strip()
            }
    return records

def main():
    print("=" * 80)
    print("SETTING PUBLISH FLAGS FOR TOWN HALL ATTENDEES")
    print("=" * 80)
    print()
    
    if not AIRTABLE_AVAILABLE:
        print("❌ Cannot proceed without Airtable configuration")
        return 1
    
    # Initialize Airtable API
    api = Api(AIRTABLE_CONFIG['api_key'])
    table = api.table(AIRTABLE_CONFIG['base_id'], AIRTABLE_CONFIG['tables']['people'])
    
    # Load current state
    print("📥 Loading current Airtable state...")
    records = load_airtable_records()
    print()
    
    success_count = 0
    error_count = 0
    already_published = 0
    not_found = []
    
    for name in NAMES_TO_PUBLISH:
        if name not in records:
            print(f"⚠️  {name} - not found in Airtable")
            not_found.append(name)
            continue
        
        rec = records[name]
        record_id = rec['id']
        
        if not record_id:
            print(f"⚠️  {name} - no Airtable ID")
            continue
        
        # Check if already published
        if rec['publish'] == 'True':
            print(f"✓  {name} - already published")
            already_published += 1
            continue
        
        # Set Publish flag
        try:
            table.update(record_id, {'Publish': True})
            print(f"✅ {name} - set Publish=True")
            success_count += 1
        except Exception as e:
            print(f"❌ {name}: {e}")
            error_count += 1
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Publish flag set: {success_count}")
    print(f"✓  Already published: {already_published}")
    
    if error_count > 0:
        print(f"❌ Errors: {error_count}")
    
    if not_found:
        print(f"\n⚠️  Not found: {len(not_found)}")
        for name in not_found:
            print(f"   - {name}")
    
    print()
    print("=" * 80)
    print("NOTE: Mahangi Munanse / Muhangi Musinga duplicate detected")
    print("=" * 80)
    print("These appear to be the same person:")
    print("  - Mahangi Munanse (recjmTo1C7JGqdZYs) - iptowncrush@gmail.com")
    print("  - Muhangi Musinga (reckJ82HydeOio4eV) - mmusinga32@gmail.com")
    print("Muhangi Musinga already has bio and is published.")
    print("Recommend merging these records.")
    
    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
