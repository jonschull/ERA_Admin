#!/usr/bin/env python3
"""
Process Batch 1 with user corrections.
"""

import json

# Actions to process with corrections
actions = [
    # HIGH confidence - approved as-is
    {'action': 'merge', 'fathom_name': 'JP', 'airtable_name': 'John Perlin'},
    {'action': 'merge', 'fathom_name': 'Jon Schull (Enabling The Future)', 'airtable_name': 'Jon Schull'},
    {'action': 'merge', 'fathom_name': 'Jon Schull, EcoRestoration Alliance', 'airtable_name': 'Jon Schull'},
    {'action': 'merge', 'fathom_name': 'Jon Schull, EcoRestoration Alliance (2)', 'airtable_name': 'Jon Schull'},
    {'action': 'merge', 'fathom_name': 'Jon Schull, EcoRestoration Alliance (7)', 'airtable_name': 'Jon Schull'},
    {'action': 'add', 'fathom_name': 'Joshua Konkankoh', 'full_name': 'Joshua Konkankoh', 'era_member': True},
    {'action': 'add', 'fathom_name': 'Joshua Laizer', 'full_name': 'Joshua Laizer'},
    {'action': 'merge', 'fathom_name': 'Joshua Laizer (4)', 'airtable_name': 'Joshua Laizer'},
    {'action': 'merge', 'fathom_name': 'Joshua Laizer (7)', 'airtable_name': 'Joshua Laizer'},
    {'action': 'merge', 'fathom_name': 'Judith D. Schwartz', 'airtable_name': 'Judith Schwartz', 'note': 'User confirmed already in Airtable'},
    {'action': 'add', 'fathom_name': 'Julia', 'full_name': 'Julia Lindley'},
    {'action': 'merge', 'fathom_name': 'Justin Ritchie (3)', 'airtable_name': 'Justin Ritchie'},
    {'action': 'merge', 'fathom_name': 'KALOMBO-MBILIZI', 'airtable_name': 'Kalombo Mbilizi'},
    {'action': 'add', 'fathom_name': 'Kaluki Paul Mutuku', 'full_name': 'Kaluki Paul Mutuku'},
    {'action': 'merge', 'fathom_name': 'Kaluki Paul Mutuku (2)', 'airtable_name': 'Kaluki Paul Mutuku'},
    {'action': 'merge', 'fathom_name': 'Kaluki Paul Mutuku (4)', 'airtable_name': 'Kaluki Paul Mutuku'},
    {'action': 'add', 'fathom_name': 'Karim', 'full_name': 'Karim Camara'},
    {'action': 'merge', 'fathom_name': 'Katrina Jeffries (5)', 'airtable_name': 'Katrina Jeffries'},
    {'action': 'merge', 'fathom_name': 'Kethia', 'airtable_name': 'Kethia Calixte'},
    {'action': 'add', 'fathom_name': 'Kevin A.', 'full_name': 'Kevin A.', 'note': 'Need full last name - add for now'},
    {'action': 'add', 'fathom_name': 'Kevin Li', 'full_name': 'Kevin Li'},
    {'action': 'merge', 'fathom_name': 'Leonard', 'airtable_name': 'Leonard Iyamuremye'},
    {'action': 'merge', 'fathom_name': 'Leonard IYAMUREME', 'airtable_name': 'Leonard Iyamuremye'},
    
    # MEDIUM - with corrections
    {'action': 'add', 'fathom_name': 'Jeremy - Open Forest Protocol', 'full_name': 'Jeremy Epstein'},
    {'action': 'add', 'fathom_name': 'Juan José Pimento', 'full_name': 'Juan José Pimento'},
    {'action': 'merge', 'fathom_name': 'Juan from Panama', 'airtable_name': 'Juan Carlos Monterrey'},
    {'action': 'merge', 'fathom_name': 'Justin R-Söndergaard', 'airtable_name': 'Justin Roborg-Sondergaard'},
    {'action': 'add', 'fathom_name': 'Justin Ritchie', 'full_name': 'Justin Ritchie'},
    {'action': 'add', 'fathom_name': 'Katharine King', 'full_name': 'Katharine King'},
    {'action': 'add', 'fathom_name': 'Kathleen Groppe', 'full_name': 'Kathleen Groppe'},
    {'action': 'add', 'fathom_name': 'Kathryn Alexander, MA', 'full_name': 'Kathryn Alexander'},
    {'action': 'merge', 'fathom_name': 'Kim Chapple', 'airtable_name': 'Kimberly Chapple'},
    {'action': 'add', 'fathom_name': 'Kwaxala / Pete', 'full_name': 'Pete Corke'},
    {'action': 'add', 'fathom_name': 'Larry Kopald', 'full_name': 'Larry Kopald'},
    {'action': 'add', 'fathom_name': "Lastborn's Galaxy A11 (3)", 'full_name': 'Ilarion Merculief'},
    {'action': 'add', 'fathom_name': 'Lee G', 'full_name': 'Lee G', 'note': 'Need full last name - add for now'},
    
    # LOW - corrections
    {'action': 'merge', 'fathom_name': 'Belizey', 'airtable_name': 'Mbilizi Kalombo'},
    {'action': 'add', 'fathom_name': "Lastborn's Galaxy A11", 'full_name': 'Ilarion Merculief', 'note': 'Claude missed this'},
    
    # LOW - approved drops (except Jules)
    {'action': 'drop', 'fathom_name': 'John K Carroll'},
    {'action': 'drop', 'fathom_name': "John's iPhone"},
    {'action': 'drop', 'fathom_name': "Josean's iPhone"},
    {'action': 'drop', 'fathom_name': "Josean's iPhone (11)"},
    {'action': 'drop', 'fathom_name': 'Joseph Manning'},
    {'action': 'drop', 'fathom_name': 'Joshua Price'},
    {'action': 'drop', 'fathom_name': 'Joshua Shepard'},
    {'action': 'drop', 'fathom_name': 'Judith Rosen'},
    # Jules - SKIP for next round
    {'action': 'drop', 'fathom_name': 'Kaitlin Sullivan'},
    {'action': 'drop', 'fathom_name': 'Kathia Burillo'},
    {'action': 'drop', 'fathom_name': 'Kinari Webb'},
]

print("="*80)
print("BATCH 1 PROCESSING - WITH USER CORRECTIONS")
print("="*80)

results = {
    'adds': [],
    'merges': [],
    'drops': [],
    'errors': []
}

for item in actions:
    action = item['action']
    fathom_name = item['fathom_name']
    
    try:
        if action == 'add':
            print(f"\n✅ ADD: {fathom_name} → {item['full_name']}")
            if item.get('note'):
                print(f"   Note: {item['note']}")
            # Would call: add_to_airtable(item['full_name'], fathom_name)
            results['adds'].append(item)
            
        elif action == 'merge':
            print(f"\n🔗 MERGE: {fathom_name} → {item['airtable_name']}")
            if item.get('note'):
                print(f"   Note: {item['note']}")
            # Would call: merge_participants(fathom_name, item['airtable_name'])
            results['merges'].append(item)
            
        elif action == 'drop':
            print(f"\n❌ DROP: {fathom_name}")
            # Would call: remove_participant(fathom_name)
            results['drops'].append(item)
            
    except Exception as e:
        print(f"\n⚠️ ERROR: {fathom_name} - {str(e)}")
        results['errors'].append({'item': item, 'error': str(e)})

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"✅ Adds: {len(results['adds'])}")
print(f"🔗 Merges: {len(results['merges'])}")
print(f"❌ Drops: {len(results['drops'])}")
print(f"⚠️ Errors: {len(results['errors'])}")

# Save results
with open('/tmp/batch1_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n📄 Results saved to: /tmp/batch1_results.json")
print("\n✅ DRY RUN COMPLETE - Review and confirm before executing actual API calls")
