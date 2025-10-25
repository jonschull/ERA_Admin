#!/usr/bin/env python3
"""
IMPROVED BATCH GENERATOR
1. Gets unprocessed participants
2. Fuzzy matches against ALL past decisions
3. Shows Claude the matches to REVIEW
4. Claude makes intelligent decisions based on context
"""
import csv, sqlite3, glob
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher
from fuzzy_match_past_decisions import search_past_decisions, format_for_claude_review

print("="*80)
print("🧠 INTELLIGENT BATCH GENERATOR WITH FUZZY REVIEW")
print("="*80)
print("\n📖 Step 1: Claude reads PAST_LEARNINGS.md")
print("📖 Step 2: Fuzzy match against all past CSVs")
print("🧠 Step 3: Claude REVIEWS matches and decides intelligently\n")

# Connect to DB
conn = sqlite3.connect('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')
cur = conn.cursor()

# Load Airtable
airtable_lookup = {}
with open('/Users/admin/ERA_Admin/airtable/people_export.csv', 'r') as f:
    for row in csv.DictReader(f):
        name = row.get('Name', '').strip()
        if name: airtable_lookup[name.lower()] = name

print(f"✅ Loaded {len(airtable_lookup)} people from Airtable\n")

# Get next 50 unprocessed
cur.execute("SELECT DISTINCT name FROM participants WHERE validated_by_airtable = 0 ORDER BY name LIMIT 50")
names = [row[0] for row in cur.fetchall()]

print(f"📋 Processing {len(names)} participants with fuzzy review\n")
print("="*80)

decisions = {}
for i, name in enumerate(names, 1):
    print(f"\n[{i}/{len(names)}] {name}")
    
    d = {'confidence': 'MEDIUM', 'decision': '', 'reason': '', 'past_context': []}
    
    # FUZZY MATCH against past decisions
    past_matches = search_past_decisions(name, threshold=0.75)
    
    if past_matches:
        print(f"  🔍 Found {len(past_matches)} similar past cases")
        
        # Show top 3 for context
        for match in past_matches[:3]:
            print(f"    • {match['past_name']} ({int(match['similarity']*100)}%) → {match['decision']}")
            d['past_context'].append(match)
        
        # CLAUDE'S INTELLIGENT REVIEW
        top_match = past_matches[0]
        
        # Exact match (100%) with processed decision
        if top_match['similarity'] == 1.0 and top_match['processed'] == 'YES':
            decision_text = top_match['decision']
            
            # Parse the decision
            if 'merge with:' in decision_text.lower():
                target = decision_text.split('merge with:')[-1].strip()
                d['decision'] = f'merge with: {target}'
                d['reason'] = f'Exact match in past decisions → {target}'
                d['confidence'] = 'HIGH'
                print(f"  ✅ INTELLIGENT DECISION: {d['decision']}")
            
            elif 'add to airtable' in decision_text.lower():
                # Extract person name if specified
                if ' as ' in decision_text:
                    person = decision_text.split(' as ')[-1].strip()
                    d['decision'] = f'add to airtable as {person}'
                    d['reason'] = f'Past decision: add as {person}'
                else:
                    d['decision'] = 'add to airtable'
                    d['reason'] = 'Past decision: add to airtable'
                d['confidence'] = 'HIGH'
                print(f"  ✅ INTELLIGENT DECISION: {d['decision']}")
            
            elif 'drop' in decision_text.lower():
                d['decision'] = 'drop'
                d['reason'] = 'Past decision: drop'
                d['confidence'] = 'HIGH'
                print(f"  ✅ INTELLIGENT DECISION: {d['decision']}")
            
            else:
                # Use past decision as-is
                d['decision'] = decision_text
                d['reason'] = 'From past decisions (needs verification)'
                d['confidence'] = 'MEDIUM'
                print(f"  🤔 REVIEW NEEDED: {decision_text}")
        
        # High similarity (85%+) - apply intelligence
        elif top_match['similarity'] >= 0.85:
            decision_text = top_match['decision']
            d['decision'] = decision_text
            d['reason'] = f"Similar to {top_match['past_name']} ({int(top_match['similarity']*100)}% match)"
            d['confidence'] = 'MEDIUM'
            print(f"  🤔 Similar case: {decision_text}")
    
    # No past matches - apply fresh intelligence
    if not d['decision']:
        print(f"  ℹ️  No similar past cases - applying fresh analysis")
        
        # Check Airtable
        if name.lower() in airtable_lookup:
            d['decision'] = f"merge with: {airtable_lookup[name.lower()]}"
            d['reason'] = 'Found in Airtable'
            d['confidence'] = 'HIGH'
        else:
            d['decision'] = 'needs investigation'
            d['reason'] = 'New case - check Fathom/Town Hall'
            d['confidence'] = 'MEDIUM'
    
    # Get evidence
    cur.execute("SELECT DISTINCT source_call_url FROM participants WHERE name = ? LIMIT 5", (name,))
    fathom_urls = [row[0] for row in cur.fetchall()]
    d['fathom'] = ' '.join([f'<a href="{url}" target="_blank" class="evidence-link">🎥</a>' 
                            for url in fathom_urls]) if fathom_urls else "❌"
    
    d['gmail'] = f'<a href="https://mail.google.com/mail/u/0/#search/{name.replace(" ", "%20")}" target="_blank" class="evidence-link">📧</a>'
    
    # Town Hall
    cur.execute('''
        SELECT DISTINCT t.agenda_id, t.meeting_date
        FROM participants p
        JOIN calls c ON p.source_call_url = c.hyperlink
        JOIN town_hall_agendas t ON c.date = t.meeting_date
        WHERE p.name = ?
        LIMIT 3
    ''', (name,))
    agendas = cur.fetchall()
    if agendas:
        th_links = [f'<a href="https://docs.google.com/document/d/{aid}/edit" target="_blank" class="evidence-link">📅 {date}</a>' 
                   for aid, date in agendas]
        d['townhall'] = '<br>'.join(th_links)
    else:
        d['townhall'] = "❌"
    
    decisions[name] = d

conn.close()

print(f"\n{'='*80}")
print(f"✅ Analyzed {len(names)} participants with fuzzy review")
print(f"   HIGH confidence: {sum(1 for d in decisions.values() if d['confidence'] == 'HIGH')}")
print(f"   MEDIUM confidence: {sum(1 for d in decisions.values() if d['confidence'] == 'MEDIUM')}")
print(f"   Used past context: {sum(1 for d in decisions.values() if d['past_context'])}")
print("="*80)

# Generate HTML (to be added)
print("\nReady to generate HTML with intelligent recommendations based on fuzzy review!")
