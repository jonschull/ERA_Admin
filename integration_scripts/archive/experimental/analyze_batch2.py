#!/usr/bin/env python3
"""
Batch 2 Analysis with Airtable Cross-Check and Past Learnings
"""

import csv
import sqlite3
from pathlib import Path

# Batch 2 participants
batch2_names = [
    '16319034965', '18022588598', 'Abigail Castle', 'Aditi', 'admin', 'afmiller09',
    'Agri-Tech Producers LLC, Joe James', 'Aimee Samara (Krouskop)', 'Allison Wu',
    'Alnoor IP 14P', 'Ana', 'ana - Panama Restoration Lab', 'Ana C',
    'Ananda Fitzsimmons (4)', 'Andrea Manrique', 'andreaseke', "Andres's iPhone (2)",
    'Angelique', 'aniqa', 'aniqa Locations: Bangladesh, Egypt, Sikkim',
    'Anna Calderon', 'Ansiima Casinga Rolande', 'BasHam (Ecoist)', 'Beck Bio4Climate',
    'Benamara Elhabib', 'Betty Bitengo', 'Billimarie', 'Billimarie (3)',
    'Bio4Climate1 (Beck Mordini)', 'BioIntegrity', 'bk', 'Brendah',
    'Brendan McNamara (ORQAS)', 'Brian', 'Bru Pearce (4)', 'C. Petruzzi-McHale',
    'CBiradar', 'Charles', 'Charlie Shore', 'Charlie Shore, Gaithersburg, MD',
    'charlotte', 'Chris Pilley', 'CHRISTOPHER - Tanzania', 'Christopher Danch',
    'Climbien', 'Climbien (3)', 'Coakee Wildcat', 'Cole',
    'Cosmic Labyrinth (Indy Boyle-Rhymes)', 'Cosmic Labyrinth (Indy)'
]

# Load Airtable people
airtable_csv = Path('/Users/admin/ERA_Admin/airtable/people_export.csv')
airtable_people = set()

print("📖 Loading Airtable people...")
with open(airtable_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('Name', '').strip()
        if name:
            airtable_people.add(name.lower())

print(f"   ✅ Loaded {len(airtable_people)} people from Airtable")

# Connect to Fathom DB for Town Hall/recording data
fathom_db = '/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db'

# Analyze each participant
decisions = {}

for name in batch2_names:
    decision = {'name': name, 'confidence': 'MEDIUM', 'decision': '', 'reason': '', 'in_airtable': False}
    
    # Check if in Airtable
    name_lower = name.lower()
    if name_lower in airtable_people:
        decision['in_airtable'] = True
    
    # Pattern matching
    if name.isdigit():
        decision['decision'] = 'drop'
        decision['reason'] = 'Phone number'
        decision['confidence'] = 'HIGH'
    
    elif name in ['admin', 'bk', 'afmiller09', 'andreaseke']:
        decision['decision'] = 'drop'
        decision['reason'] = 'System account or username'
        decision['confidence'] = 'HIGH'
    
    elif "iPhone" in name:
        decision['decision'] = 'drop'
        decision['reason'] = 'Device name'
        decision['confidence'] = 'HIGH'
    
    # Organization patterns (past learnings)
    elif name == 'Agri-Tech Producers LLC, Joe James':
        if 'joe james' in airtable_people:
            decision['decision'] = 'merge with: Joe James'
            decision['in_airtable'] = True
        else:
            decision['decision'] = 'add to airtable as Joe James'
        decision['reason'] = 'Organization + person pattern (past learning)'
        decision['confidence'] = 'HIGH'
    
    elif name == 'BioIntegrity':
        decision['decision'] = 'merge with: Chris Searles'
        decision['reason'] = 'Organization = Chris Searles (past learning: Oct 22)'
        decision['confidence'] = 'HIGH'
        decision['in_airtable'] = True
    
    # Number variants
    elif '(' in name and ')' in name and any(c.isdigit() for c in name):
        base_name = name.split('(')[0].strip()
        if base_name.lower() in airtable_people:
            decision['decision'] = f'merge with: {base_name}'
            decision['reason'] = f'Number variant of {base_name}'
            decision['confidence'] = 'HIGH'
        else:
            decision['decision'] = f'merge with: {base_name}'
            decision['reason'] = f'Number variant - base name may need adding'
            decision['confidence'] = 'MEDIUM'
    
    # Past learnings
    elif name == 'CBiradar':
        decision['decision'] = 'merge with: Chandrashekhar Biradar'
        decision['reason'] = 'Past learning: CBiradar = Chandrashekhar Biradar'
        decision['confidence'] = 'HIGH'
    
    elif name == 'Brendah':
        decision['decision'] = 'merge with: Mbilizi Kalombo'
        decision['reason'] = 'Past learning from earlier rounds'
        decision['confidence'] = 'MEDIUM'
    
    elif name == 'charlotte':
        decision['decision'] = 'merge with: Charlotte Anthony'
        decision['reason'] = 'Past learning: charlotte = Charlotte Anthony'
        decision['confidence'] = 'HIGH'
    
    elif name in ['Climbien', 'Climbien (3)']:
        decision['decision'] = 'merge with: Climbien Babungire'
        decision['reason'] = 'Past learning + number variant'
        decision['confidence'] = 'HIGH'
    
    # Organization + person patterns
    elif ' - ' in name or '(' in name:
        # Extract person name
        if '(' in name:
            person = name.split('(')[1].rstrip(')')
            if person and not person.isdigit():
                decision['decision'] = f'add to airtable as {person}'
                decision['reason'] = f'Person name from context: {name}'
                decision['confidence'] = 'MEDIUM'
    
    # Already in Airtable
    elif decision['in_airtable']:
        decision['decision'] = f'merge with: {name}'
        decision['reason'] = 'Already in Airtable'
        decision['confidence'] = 'HIGH'
    
    # Default: investigate
    else:
        decision['decision'] = 'add to airtable' if len(name.split()) > 1 else 'investigate'
        decision['reason'] = 'Full name - check Town Hall context' if len(name.split()) > 1 else 'Single name - needs context'
        decision['confidence'] = 'MEDIUM'
    
    decisions[name] = decision

# Print summary
print("\n" + "="*80)
print("BATCH 2 ANALYSIS SUMMARY")
print("="*80)

high = [d for d in decisions.values() if d['confidence'] == 'HIGH']
medium = [d for d in decisions.values() if d['confidence'] == 'MEDIUM']
low = [d for d in decisions.values() if d['confidence'] == 'LOW']

print(f"\n✅ HIGH Confidence: {len(high)}")
print(f"🤔 MEDIUM Confidence: {len(medium)}")
print(f"⚠️  LOW Confidence: {len(low)}")

print(f"\n📊 Already in Airtable: {sum(1 for d in decisions.values() if d['in_airtable'])}")
print(f"➕ To Add: {sum(1 for d in decisions.values() if 'add to airtable' in d['decision'])}")
print(f"🔗 To Merge: {sum(1 for d in decisions.values() if 'merge with' in d['decision'])}")
print(f"❌ To Drop: {sum(1 for d in decisions.values() if d['decision'] == 'drop')}")

# Save for HTML generation
import json
with open('/tmp/batch2_decisions.json', 'w') as f:
    json.dump(decisions, f, indent=2)

print(f"\n📄 Saved decisions to: /tmp/batch2_decisions.json")
print("✅ Ready for HTML generation")
