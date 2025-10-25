#!/usr/bin/env python3
"""
STANDARD BATCH GENERATOR - Use this for all future batches

⚠️  CLAUDE: This script will STOP and FORCE you to confirm you've read PAST_LEARNINGS.md
Scripts are dumb. YOU are smart. ACT LIKE IT.
"""
import sys

print("="*80)
print("🚨 MANDATORY PRE-FLIGHT CHECKLIST FOR CLAUDE 🚨")
print("="*80)
print()
print("STOP! Before this script generates anything, you MUST:")
print()
print("1. READ /Users/admin/ERA_Admin/integration_scripts/PAST_LEARNINGS.md")
print("   📖 ACTUALLY READ IT - don't just load it in code")
print("   🧠 INTERNALIZE the patterns in YOUR HEAD")
print()
print("2. Examples of what YOU need to recognize (script can't):")
print("   • 'bk' = Brian Krawitz (initials pattern)")
print("   • 'Agri-Tech Producers LLC, Joe James' → extract Joe James")
print("   • 'ana - Panama Restoration Lab' → Ana Calderon")
print("   • 'Alnoor IP 14P' → Alnoor Sharif")
print()
print("3. The script can only match EXACT strings.")
print("   YOU can recognize VARIATIONS and PATTERNS.")
print()
print("="*80)
response = input("Have you READ and INTERNALIZED PAST_LEARNINGS.md? (yes/no): ").strip().lower()

if response != 'yes':
    print("\n❌ STOPPED: Go read PAST_LEARNINGS.md first.")
    print("   Your intelligence > Script's pattern matching")
    sys.exit(1)

print("\n✅ Good. Now generating batch with YOUR intelligence applied...")
print()

import csv, sqlite3
from pathlib import Path
from datetime import datetime

conn = sqlite3.connect('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')
cur = conn.cursor()

# Load Airtable for fuzzy matching
airtable_lookup = {}
with open('/Users/admin/ERA_Admin/airtable/people_export.csv', 'r') as f:
    for row in csv.DictReader(f):
        name = row.get('Name', '').strip()
        if name: airtable_lookup[name.lower()] = name

print(f"📖 Loaded {len(airtable_lookup)} people from Airtable")

# Get next 50 unprocessed
cur.execute("SELECT DISTINCT name FROM participants WHERE validated_by_airtable = 0 ORDER BY name LIMIT 50")
names = [row[0] for row in cur.fetchall()]

print(f"📋 Processing {len(names)} participants")
print()
print("⚠️  REMINDER: Apply the patterns YOU learned from PAST_LEARNINGS.md")
print("   Don't just rely on exact string matching!")
print()

# Now YOU (Claude) will make intelligent decisions based on what you read
# The script just gathers evidence and formats HTML

decisions = {}
for name in names:
    # Get evidence
    cur.execute("SELECT DISTINCT source_call_url FROM participants WHERE name = ? LIMIT 5", (name,))
    fathom_urls = [row[0] for row in cur.fetchall()]
    fathom_links = ' '.join([f'<a href="{url}" target="_blank" class="evidence-link">🎥</a>' 
                             for url in fathom_urls]) if fathom_urls else "❌"
    
    gmail_link = f'<a href="https://mail.google.com/mail/u/0/#search/{name.replace(" ", "%20")}" target="_blank" class="evidence-link">📧</a>'
    
    # Town Hall links (proper join)
    cur.execute('''
        SELECT DISTINCT t.agenda_id, t.meeting_date
        FROM participants p
        JOIN calls c ON p.source_call_url = c.hyperlink
        JOIN town_hall_agendas t ON c.date = t.meeting_date
        WHERE p.name = ?
        ORDER BY t.meeting_date DESC
        LIMIT 3
    ''', (name,))
    
    agendas = cur.fetchall()
    if agendas:
        th_links = []
        for agenda_id, date in agendas:
            doc_url = f"https://docs.google.com/document/d/{agenda_id}/edit"
            th_links.append(f'<a href="{doc_url}" target="_blank" class="evidence-link">📅 {date}</a>')
        townhall = '<br>'.join(th_links)
    else:
        townhall = "❌"
    
    decisions[name] = {
        'fathom': fathom_links,
        'gmail': gmail_link,
        'townhall': townhall
    }

conn.close()

# Save data for Claude to analyze
import json
output_data = Path('/tmp/batch_next_data.json')
with open(output_data, 'w') as f:
    json.dump({
        'names': names,
        'evidence': decisions,
        'airtable_people': list(airtable_lookup.values())[:100]  # Sample
    }, f, indent=2)

print(f"\n✅ Evidence gathered for {len(names)} participants")
print(f"📄 Data saved to: {output_data}")
print()
print("="*80)
print("NOW: Claude makes intelligent decisions using PAST_LEARNINGS")
print("="*80)
print()
print("REMINDER after generating HTML:")
print("  1. User reviews and gives feedback")
print("  2. YOU update PAST_LEARNINGS.md with new patterns")
print("  3. Process approved actions")
print()
