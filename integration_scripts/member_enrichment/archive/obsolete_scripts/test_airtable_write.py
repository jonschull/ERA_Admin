#!/usr/bin/env python3
"""
Quick test: Does our ERA_Admin Airtable key have write permissions?
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'airtable'))

from pyairtable import Api
from config import AIRTABLE_CONFIG

# Test with a safe field update on a test record
api = Api(AIRTABLE_CONFIG['api_key'])
table = api.table(AIRTABLE_CONFIG['base_id'], AIRTABLE_CONFIG['tables']['people'])

print("Testing write permissions...")
print(f"Base ID: {AIRTABLE_CONFIG['base_id']}")
print()

# Use the Abby Karparsi record for test
TEST_ID = 'recp6cA4v3QZm3R6A'

try:
    # Read current
    record = table.get(TEST_ID)
    current_name = record['fields'].get('Name', '')
    print(f"✅ Read successful: {current_name}")
    
    # Try a no-op update (update to same value)
    print(f"Testing write with no-op update...")
    table.update(TEST_ID, {'Name': current_name})
    print("✅ WRITE SUCCESSFUL! Key has write permissions!")
    print()
    print("Ready to proceed with fixes.")
    
except Exception as e:
    print(f"❌ Write failed: {e}")
    print()
    if "403" in str(e):
        print("Key still read-only. Need write-enabled PAT.")
    else:
        print("Different error - investigate.")
