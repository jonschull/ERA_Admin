#!/usr/bin/env python3
"""
Apply learned mappings from previous rounds to current batch.
Automatically fills in decisions for known patterns.
"""
import json
import sys
from pathlib import Path

# Load learned mappings
mappings_file = Path(__file__).parent / 'phase4b2_learned_mappings.json'
with open(mappings_file, 'r') as f:
    mappings = json.load(f)

phone_mappings = mappings.get('phone_mappings', {})
device_mappings = mappings.get('device_mappings', {})
name_corrections = mappings.get('name_corrections', {})
org_to_person = mappings.get('org_to_person', {})
drop_patterns = set(mappings.get('drop_patterns', []))

def apply_mappings(batch_data):
    """Apply learned mappings to batch data"""
    
    applied = {
        'phone': 0,
        'device': 0,
        'org': 0,
        'name': 0,
        'drop': 0
    }
    
    for person in batch_data:
        fathom_name = person.get('name', '')
        
        # Already has a decision? Skip
        if person.get('auto_decision'):
            continue
        
        # Check drop patterns
        if fathom_name in drop_patterns:
            person['auto_decision'] = 'drop'
            person['auto_reason'] = f'Previously dropped in earlier round'
            applied['drop'] += 1
            continue
        
        # Check phone mappings
        if fathom_name in phone_mappings:
            target = phone_mappings[fathom_name]
            person['auto_decision'] = f'merge with: {target}'
            person['auto_reason'] = f'Phone number mapping from previous round'
            applied['phone'] += 1
            continue
        
        # Check device mappings  
        if fathom_name in device_mappings:
            target = device_mappings[fathom_name]
            person['auto_decision'] = f'merge with: {target}'
            person['auto_reason'] = f'Device name mapping from previous round'
            applied['device'] += 1
            continue
        
        # Check org mappings
        if fathom_name in org_to_person:
            target = org_to_person[fathom_name]
            person['auto_decision'] = f'merge with: {target}'
            person['auto_reason'] = f'Organization mapping from previous round'
            applied['org'] += 1
            continue
        
        # Check name corrections (less aggressive - only if exact match)
        if fathom_name in name_corrections:
            target = name_corrections[fathom_name]
            # Filter out non-name corrections (instructions, etc.)
            if not any(word in target.lower() for word in ['add', 'era', 'member', 'organization', 'airtable', 'examine', 'gmail']):
                person['auto_decision'] = f'merge with: {target}'
                person['auto_reason'] = f'Name correction from previous round'
                applied['name'] += 1
    
    return batch_data, applied

if __name__ == '__main__':
    # This would be called from generate_phase4b2_table.py
    print(f"Loaded {len(phone_mappings)} phone, {len(device_mappings)} device, "
          f"{len(org_to_person)} org, {len(name_corrections)} name, "
          f"{len(drop_patterns)} drop mappings")
