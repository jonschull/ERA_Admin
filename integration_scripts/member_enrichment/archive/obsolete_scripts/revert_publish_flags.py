#!/usr/bin/env python3
"""Revert the 9 Publish flags I just set by mistake."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'airtable'))

from pyairtable import Api
from config import AIRTABLE_CONFIG

api = Api(AIRTABLE_CONFIG['api_key'])
table = api.table(AIRTABLE_CONFIG['base_id'], AIRTABLE_CONFIG['tables']['people'])

names_to_revert = [
    ('Abby Karparis', 'recp6cA4v3QZm3R6A'),
    ('Ben Rubin', 'rectb5bvnxf3KRCee'),
    ('Brendan McNamara', 'recRsz61TznaNVvB3'),
    ('Brian Krawitz', 'recuLLZtlrJkkVy6N'),
    ('Chris pieper', 'recVPFOyDjpMpm1T4'),
    ('Emmanuelle Chiche', 'recu2VRrMGyz3zVB8'),
    ('Mahangi Munanse', 'recjmTo1C7JGqdZYs'),
    ('Christina Engelsgaard', 'recsS2wW3VUWb4444'),
    ('David maher', 'rec66aVpCukqpYans')
]

print("REVERTING Publish flags...")
print("=" * 80)

for name, record_id in names_to_revert:
    try:
        table.update(record_id, {'Publish': False})
        print(f"✅ {name} - reverted to Publish=False")
    except Exception as e:
        print(f"❌ {name}: {e}")

print()
print("✅ Reverted 9 Publish flags")
print()
print("ISSUE: 'Jon Should publish' field doesn't exist in Airtable")
print("Need to create it first or use different approach")
