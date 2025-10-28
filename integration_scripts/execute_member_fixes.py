#!/usr/bin/env python3
"""
Execute diagnostic fixes based on user decisions.

PRINCIPLE: ERA Member = Attended Town Hall (unless exception made by Jon)

Actions:
1. Fix spelling mismatches (Queue A & B)
2. Remove ERA member flags from priority 0 (44 names)
3. Remove ERA member flags from 4 unrecognized names
4. Flag published non-members for unpublishing
5. Dedupe 8 duplicate records

Then generate fresh diagnostic.
"""

import sys
import csv
from pathlib import Path

# Add airtable module to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'airtable'))

from pyairtable import Api
from config import AIRTABLE_CONFIG

# Initialize Airtable
api = Api(AIRTABLE_CONFIG['api_key'])
table = api.table(AIRTABLE_CONFIG['base_id'], AIRTABLE_CONFIG['tables']['people'])

# Paths
ERA_ADMIN_ROOT = Path(__file__).parent.parent
AIRTABLE_CSV = ERA_ADMIN_ROOT / 'airtable' / 'people_export.csv'

# Queue A & B: Spelling fixes
SPELLING_FIXES = [
    # Queue A: High confidence (100% match) - these are already correct in Airtable
    # Just need to investigate why they were priority 0
    
    # Queue B: Need name corrections
    {'id': 'recp6cA4v3QZm3R6A', 'old_name': 'Abby Karparsi', 'new_name': 'Abby Karparis'},
    {'id': 'recEXcpeaO5Tws4XM', 'old_name': 'Edward Muller', 'new_name': 'Eduard Muller'},
]

# Priority 0 names to remove ERA member flag (44 total)
PRIORITY_0_REMOVE_ERA_FLAG = [
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

# Unrecognized members to remove ERA flag (not in database, user doesn't know them)
UNRECOGNIZED_REMOVE_ERA_FLAG = [
    'Benjamin Bisetsa',
    'Daniel Fleetwood',
    'David Gold',
    'David Harper'
]

# Duplicates to merge (keep first, delete second)
DUPLICATES_TO_MERGE = [
    {'keep': 'recGFs9XTcC2jnIDh', 'delete': 'recLt3XCk52TZwWk4', 'name': 'Ana Beatriz Freitas'},
    {'keep': 'recdnTAG6vu4mMCLX', 'delete': 'recsNjlDwH3PKtlg3', 'name': 'Climbien Babungire'},  # Keep published
    {'keep': 'recXLNG7IZ4a9fQWt', 'delete': 'recRSD92aDqhNH9Y6', 'name': 'Greg Jones'},
    {'keep': 'recQo8zLzTjUjgZx9', 'delete': 'reczbnaxdDvrIyUSX', 'name': 'John Hepworth'},
    {'keep': 'rec8ZOirE8XY3mOFg', 'delete': 'recFOUrSaMCV5Xpbv', 'name': 'Marie Pierre Bilodeau'},
    {'keep': 'reckcK4G2iaCOaSya', 'delete': 'recX1da6YJtWDksqa', 'name': 'Micah Opondo'},
    {'keep': 'recCJLiqFSEsXtcTm', 'delete': 'recBIwdENBslbOPto', 'name': 'Pacifique Ndayishimiye'},
    {'keep': 'recn4KBLBzYkWx7cO', 'delete': 'recmYdaawIXc693As', 'name': 'Philip Bogdonoff'},
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
    print("=" * 80)
    print("EXECUTING DIAGNOSTIC FIXES")
    print("=" * 80)
    print()
    print("PRINCIPLE: ERA Member = Attended Town Hall")
    print()
    
    # Load current state
    records = load_airtable_records()
    
    # Track changes
    stats = {
        'spelling_fixed': 0,
        'era_flags_removed': 0,
        'duplicates_deleted': 0,
        'should_unpublish': [],
        'errors': []
    }
    
    # ========================================================================
    # 1. Fix spelling (Queue B only - Queue A already correct)
    # ========================================================================
    print("=" * 80)
    print("1. FIXING SPELLING MISMATCHES")
    print("=" * 80)
    print()
    
    for fix in SPELLING_FIXES:
        try:
            table.update(fix['id'], {'Name': fix['new_name']})
            print(f"✅ {fix['old_name']} → {fix['new_name']}")
            stats['spelling_fixed'] += 1
        except Exception as e:
            print(f"❌ {fix['old_name']}: {e}")
            stats['errors'].append(f"Spelling fix failed: {fix['old_name']}")
    
    print()
    
    # ========================================================================
    # 2. Remove ERA member flags from priority 0 (44 names)
    # ========================================================================
    print("=" * 80)
    print("2. REMOVING ERA MEMBER FLAGS (Priority 0 - No Town Hall Attendance)")
    print("=" * 80)
    print()
    
    all_remove_era = PRIORITY_0_REMOVE_ERA_FLAG + UNRECOGNIZED_REMOVE_ERA_FLAG
    
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
            print(f"✅ {name} - removed ERA member flag")
            stats['era_flags_removed'] += 1
            
            # Check if published
            if rec['publish'] == 'True':
                stats['should_unpublish'].append({
                    'name': name,
                    'id': record_id,
                    'has_bio': bool(rec['bio'])
                })
                print(f"   ⚠️  PUBLISHED but not member - add to unpublish list")
        
        except Exception as e:
            print(f"❌ {name}: {e}")
            stats['errors'].append(f"Remove ERA flag failed: {name}")
    
    print()
    
    # ========================================================================
    # 3. Delete duplicate records
    # ========================================================================
    print("=" * 80)
    print("3. DELETING DUPLICATE RECORDS")
    print("=" * 80)
    print()
    
    for dup in DUPLICATES_TO_MERGE:
        try:
            table.delete(dup['delete'])
            print(f"✅ {dup['name']} - deleted duplicate {dup['delete']}")
            print(f"   Kept: {dup['keep']}")
            stats['duplicates_deleted'] += 1
        except Exception as e:
            print(f"❌ {dup['name']}: {e}")
            stats['errors'].append(f"Delete duplicate failed: {dup['name']}")
    
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
    
    if stats['errors']:
        print(f"❌ Errors ({len(stats['errors'])}):")
        for err in stats['errors']:
            print(f"   - {err}")
        print()
    
    # Save unpublish list
    output_file = Path(__file__).parent / 'member_enrichment' / 'JON_SHOULD_UNPUBLISH.md'
    with open(output_file, 'w') as f:
        f.write("# Jon Should Unpublish\n\n")
        f.write("**Date:** October 26, 2025\n\n")
        f.write("These people are published but are NOT ERA members (no Town Hall attendance):\n\n")
        for item in stats['should_unpublish']:
            bio_status = "✅ Has bio" if item['has_bio'] else "❌ No bio"
            f.write(f"- **{item['name']}** (`{item['id']}`) - {bio_status}\n")
    
    print(f"✅ Created: {output_file}")
    print()
    
    return 0 if not stats['errors'] else 1

if __name__ == '__main__':
    sys.exit(main())
