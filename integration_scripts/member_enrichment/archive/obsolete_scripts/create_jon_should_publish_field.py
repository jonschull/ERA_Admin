#!/usr/bin/env python3
"""Create 'Jon Should publish' checkbox field in Airtable People table."""

import sys
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'airtable'))

from config import AIRTABLE_CONFIG

# Airtable Metadata API
BASE_ID = AIRTABLE_CONFIG['base_id']
API_KEY = AIRTABLE_CONFIG['api_key']
TABLE_NAME = AIRTABLE_CONFIG['tables']['people']  # "People"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("=" * 80)
print("CREATING 'Jon Should publish' FIELD")
print("=" * 80)
print()
print(f"Base: {BASE_ID}")
print(f"Table: {TABLE_NAME}")
print()

# First, get the table ID
print("1. Getting table ID...")
url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"❌ Error getting tables: {response.status_code}")
    print(response.text)
    sys.exit(1)

data = response.json()
table_id = None

for table in data.get('tables', []):
    if table['name'] == TABLE_NAME:
        table_id = table['id']
        print(f"   ✅ Found table ID: {table_id}")
        break

if not table_id:
    print(f"❌ Could not find table '{TABLE_NAME}'")
    sys.exit(1)

print()

# Check if field already exists
print("2. Checking if field already exists...")
for table in data.get('tables', []):
    if table['id'] == table_id:
        for field in table.get('fields', []):
            if field['name'] == 'Jon Should publish':
                print(f"   ⚠️  Field 'Jon Should publish' already exists!")
                print(f"   Field ID: {field['id']}")
                print(f"   Type: {field['type']}")
                print()
                print("✅ No need to create - field exists")
                sys.exit(0)

print("   Field doesn't exist yet")
print()

# Create the field
print("3. Creating 'Jon Should publish' checkbox field...")
url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{table_id}/fields"

field_config = {
    "name": "Jon Should publish",
    "type": "checkbox",
    "description": "Flag for Jon to review and publish member bio",
    "options": {
        "icon": "check",
        "color": "greenBright"
    }
}

response = requests.post(url, headers=headers, json=field_config)

if response.status_code in [200, 201]:
    result = response.json()
    print(f"   ✅ Field created successfully!")
    print(f"   Field ID: {result.get('id')}")
    print(f"   Name: {result.get('name')}")
    print(f"   Type: {result.get('type')}")
else:
    print(f"   ❌ Error creating field: {response.status_code}")
    print(f"   {response.text}")
    sys.exit(1)

print()
print("=" * 80)
print("✅ READY - Can now set 'Jon Should publish' flags via API")
print("=" * 80)
