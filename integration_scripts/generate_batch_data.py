#!/usr/bin/env python3
"""
Generate phase4b2_test_data.json from database with next 50 unenriched people.
"""

import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "FathomInventory" / "fathom_emails.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get top 50 unenriched people with their videos and affiliations
cursor.execute("""
    SELECT 
        name,
        source_call_url,
        source_call_title,
        affiliation
    FROM participants
    WHERE validated_by_airtable = 0
    ORDER BY name
""")

# Group by name and collect videos
people_data = {}
for name, url, title, affiliation in cursor.fetchall():
    if name not in people_data:
        people_data[name] = {
            'name': name,
            'videos': [],
            'record_count': 0,
            'affiliation': affiliation or 'Unknown'
        }
    
    people_data[name]['record_count'] += 1
    
    # Update affiliation if this one is better (not Unknown or generic)
    if affiliation and affiliation not in ['Unknown', 'This participant\'s company is not listed in the calendar event']:
        people_data[name]['affiliation'] = affiliation
    
    if url and url not in [v['url'] for v in people_data[name]['videos']]:
        people_data[name]['videos'].append({
            'url': url,
            'title': title or 'Untitled'
        })

# Sort by record count and take top 50
sorted_people = sorted(people_data.values(), key=lambda x: (-x['record_count'], x['name']))
top_50 = sorted_people[:50]

# Save to file
with open('/tmp/phase4b2_test_data.json', 'w') as f:
    json.dump(top_50, f, indent=2)

print(f"✅ Generated batch data for {len(top_50)} people")
for i, p in enumerate(top_50, 1):
    print(f"{i:2}. {p['name']} ({p['record_count']} records, {len(p['videos'])} videos)")

conn.close()
