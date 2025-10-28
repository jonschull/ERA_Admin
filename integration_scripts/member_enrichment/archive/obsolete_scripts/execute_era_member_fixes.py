#!/usr/bin/env python3
"""
Execute ERA member fixes based on Town Hall attendance principle.

PRINCIPLE: ERA Member = Attended Town Hall (unless exception made by Jon)

Actions:
1. Fix spelling mismatches (1 remaining: Edward → Eduard Muller)
2. Remove ERA member flags from 48 names (priority 0 + unrecognized)
3. Delete 8 duplicate records
4. Generate "Jon Should Unpublish" list

Following pattern from update_airtable_bios.py
Test case (Abby Karparsi) already successful.
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

# Paths
ERA_ADMIN_ROOT = Path(__file__).parent.parent.parent
AIRTABLE_CSV = ERA_ADMIN_ROOT / 'airtable' / 'people_export.csv'

# === FIX DATA ===

# Spelling fix (already did Abby Karparsi)
SPELLING_FIX = {
    'id': 'recEXcpeaO5Tws4XM',
    'old_name': 'Edward Muller',
    'new_name': 'Eduard Muller'
}

# Priority 0 names to remove ERA member flag (44 total)
PRIORITY_0_NAMES = [
    'Abby Abrahamson', 'Avery Correia', 'Campbell Webb', 'Candrace Ducheneaux',
    'Ceal Smith', 'Dan Gerry', 'Daniel Robin', 'Daniel Valdiviezo',
    'Derek Wilson', 'Finian Makepeace', 'Gayathri Ilango', 'Ilse Koehler-Rollefson',
    'Jacobus Van Der Bank', 'Jim Laurie', 'Joao Lopes', 'Joe Morris',
    'John Polhaus', 'John Roulac', 'John Wick', 'Karol Mieczkin',
    'Katie Chess', 'Leonie Van Der Steen', 'Lisa Smith', 'Mark Fredericks',
    'Martin Peck', 'Matthijis Bouw', 'Micah Opondo', 'Michael Vermeer',
    'Mick Lorkins', 'Monifa Afina', 'Méthode Dukore', 'Natalie Novoselova',
    'Nathalia Rio Preto', 'Ngwana Henry', 'Norma Carty', 'Pamela Berstler',
    'Patrick Worms,', 'Penny Lewise', 'Tanner Millen', 'Twizeyimana Innocent',
    'Vivian Kanchian', 'Walter Jehne', 'aparna.dasaraju', 'chris.searles'
]

# Unrecognized members (4 total)
UNRECOGNIZED_NAMES = [
    'Benjamin Bisetsa',
    'Daniel Fleetwood',
    'David Gold',
    'David Harper'
]

# Duplicates to delete (keep first, delete second)
DUPLICATES_TO_DELETE = [
    {'name': 'Ana Beatriz Freitas', 'keep': 'recGFs9XTcC2jnIDh', 'delete': 'recLt3XCk52TZwWk4'},
    {'name': 'Climbien Babungire', 'keep': 'recdnTAG6vu4mMCLX', 'delete': 'recsNjlDwH3PKtlg3'},
    {'name': 'Greg Jones', 'keep': 'recXLNG7IZ4a9fQWt', 'delete': 'recRSD92aDqhNH9Y6'},
    {'name': 'John Hepworth', 'keep': 'recQo8zLzTjUjgZx9', 'delete': 'reczbnaxdDvrIyUSX'},
    {'name': 'Marie Pierre Bilodeau', 'keep': 'rec8ZOirE8XY3mOFg', 'delete': 'recFOUrSaMCV5Xpbv'},
    {'name': 'Micah Opondo', 'keep': 'reckcK4G2iaCOaSya', 'delete': 'recX1da6YJtWDksqa'},
    {'name': 'Pacifique Ndayishimiye', 'keep': 'recCJLiqFSEsXtcTm', 'delete': 'recBIwdENBslbOPto'},
    {'name': 'Philip Bogdonoff', 'keep': 'recn4KBLBzYkWx7cO', 'delete': 'recmYdaawIXc693As'},
]

def load_airtable_records():
    """Load current Airtable state from CSV."""
    records = {}
    with open(AIRTABLE_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            records[name] = {
                'id': row.get('airtable_id', ''),
                'email': row.get('Email', ''),
                'era_member': row.get('era Member', ''),
                'publish': row.get('Publish', ''),
                'bio': row.get('Bio', '').strip()
            }
    return records

def main():
    """Execute all fixes."""
    
    print("=" * 80)
    print("EXECUTING ERA MEMBER FIXES - BULK OPERATIONS")
    print("=" * 80)
    print()
    print("PRINCIPLE: ERA Member = Attended Town Hall")
    print()
    print("Test case (Abby Karparsi) already successful ✅")
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
    print(f"   Loaded {len(records)} records")
    print()
    
    # Track changes
    stats = {
        'spelling_fixed': 1,  # Already did Abby
        'era_flags_removed': 0,
        'duplicates_deleted': 0,
        'should_unpublish': [],
        'errors': []
    }
    
    # ========================================================================
    # 1. Fix remaining spelling
    # ========================================================================
    print("=" * 80)
    print("1. FIXING SPELLING (1 remaining)")
    print("=" * 80)
    print()
    
    try:
        current = table.get(SPELLING_FIX['id'])
        current_name = current['fields'].get('Name', '')
        
        if current_name == SPELLING_FIX['old_name']:
            table.update(SPELLING_FIX['id'], {'Name': SPELLING_FIX['new_name']})
            print(f"✅ {SPELLING_FIX['old_name']} → {SPELLING_FIX['new_name']}")
            stats['spelling_fixed'] += 1
        else:
            print(f"⚠️  Skipped: Current name is '{current_name}' (expected '{SPELLING_FIX['old_name']}')")
    except Exception as e:
        print(f"❌ {SPELLING_FIX['old_name']}: {e}")
        stats['errors'].append(f"Spelling fix: {SPELLING_FIX['old_name']}")
    
    print()
    
    # ========================================================================
    # 2. Remove ERA member flags (48 names)
    # ========================================================================
    print("=" * 80)
    print("2. REMOVING ERA MEMBER FLAGS (48 names)")
    print("=" * 80)
    print()
    
    all_remove_era = PRIORITY_0_NAMES + UNRECOGNIZED_NAMES
    
    for name in all_remove_era:
        if name not in records:
            print(f"⚠️  {name} - not found in CSV")
            continue
        
        rec = records[name]
        record_id = rec['id']
        
        if not record_id:
            print(f"⚠️  {name} - no Airtable ID")
            continue
        
        try:
            # Remove ERA member flag
            table.update(record_id, {'era Member': False})
            print(f"✅ {name}")
            stats['era_flags_removed'] += 1
            
            # Check if published
            if rec['publish'] == 'True':
                stats['should_unpublish'].append({
                    'name': name,
                    'id': record_id,
                    'has_bio': bool(rec['bio'])
                })
        
        except Exception as e:
            print(f"❌ {name}: {e}")
            stats['errors'].append(f"Remove flag: {name}")
    
    print()
    
    # ========================================================================
    # 3. Delete duplicate records
    # ========================================================================
    print("=" * 80)
    print("3. DELETING DUPLICATE RECORDS (8 duplicates)")
    print("=" * 80)
    print()
    
    for dup in DUPLICATES_TO_DELETE:
        try:
            table.delete(dup['delete'])
            print(f"✅ {dup['name']} - deleted {dup['delete']}, kept {dup['keep']}")
            stats['duplicates_deleted'] += 1
        except Exception as e:
            print(f"❌ {dup['name']}: {e}")
            stats['errors'].append(f"Delete duplicate: {dup['name']}")
    
    print()
    
    # ========================================================================
    # Summary
    # ========================================================================
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"✅ Spelling fixes: {stats['spelling_fixed']}")
    print(f"✅ ERA flags removed: {stats['era_flags_removed']}")
    print(f"✅ Duplicates deleted: {stats['duplicates_deleted']}")
    print()
    
    if stats['should_unpublish']:
        print(f"⚠️  JON SHOULD UNPUBLISH ({len(stats['should_unpublish'])} records):")
        for item in stats['should_unpublish']:
            bio_status = "has bio" if item['has_bio'] else "no bio"
            print(f"   - {item['name']} ({item['id']}) [{bio_status}]")
        print()
        
        # Save unpublish list
        output_file = Path(__file__).parent / 'JON_SHOULD_UNPUBLISH.md'
        with open(output_file, 'w') as f:
            f.write("# Jon Should Unpublish\n\n")
            f.write("**Date:** October 26, 2025\n\n")
            f.write("These people are published but are NOT ERA members (no Town Hall attendance):\n\n")
            for item in stats['should_unpublish']:
                bio_status = "✅ Has bio" if item['has_bio'] else "❌ No bio"
                f.write(f"- **{item['name']}** (`{item['id']}`) - {bio_status}\n")
        
        print(f"✅ Created: {output_file}")
        print()
    
    if stats['errors']:
        print(f"❌ Errors ({len(stats['errors'])}):")
        for err in stats['errors']:
            print(f"   - {err}")
        print()
    
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print()
    print("1. Refresh Airtable export:")
    print("   cd /Users/admin/ERA_Admin/airtable")
    print("   python3 export_people.py")
    print()
    print("2. Generate fresh diagnostic:")
    print("   Who attended Town Halls but has no bio?")
    print()
    
    return 0 if not stats['errors'] else 1


if __name__ == '__main__':
    sys.exit(main())
