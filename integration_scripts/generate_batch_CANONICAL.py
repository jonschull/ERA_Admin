#!/usr/bin/env python3
"""
🔒 CANONICAL BATCH GENERATOR - THE ONLY ONE TO USE
Do not bypass this script. All safeguards are built in.

Safeguards:
1. Forces Claude to read PAST_LEARNINGS.md
2. Strips number variants before fuzzy matching
3. Filters already-processed items (no repeats)
4. Checks Airtable with base names
5. Outputs decisions for Claude's intelligent review
6. Generates HTML only after review
"""
import sys
import csv, sqlite3, glob, re
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher

print("="*80)
print("🔒 CANONICAL BATCH GENERATOR")
print("="*80)
print("\n⚠️  MANDATORY PRE-FLIGHT CHECKLIST FOR CLAUDE ⚠️\n")
print("Before this script runs, you (Claude) MUST:")
print()
print("1. READ /Users/admin/ERA_Admin/integration_scripts/PAST_LEARNINGS.md")
print("   📖 ACTUALLY READ IT - internalize patterns in your HEAD")
print()
print("2. Key patterns you need to know:")
print("   • Organizations → people (Flip Town = Muhange Musinga)")
print("   • Name variants (Climbien = Climbien Babungire)")
print("   • Phone numbers → people")
print("   • Username patterns (georgeorbelian = George Orbelian)")
print("   • Single names (jon = Jon Schull, juliet = ?)")
print()
print("3. You will REVIEW items before HTML generation, not bypass to HTML")
print()
print("="*80)
response = input("\n🔒 Have you READ and INTERNALIZED PAST_LEARNINGS.md? (yes/no): ").strip().lower()

if response != 'yes':
    print("\n❌ STOPPED: Go read PAST_LEARNINGS.md first.")
    print("   Context: integration_scripts/PAST_LEARNINGS.md")
    sys.exit(1)

print("\n✅ Proceeding with safeguards enabled...\n")

# Helper functions
def strip_number_suffix(name):
    """Remove (2), (3), (14), etc. from names"""
    return re.sub(r'\s*\(\d+\)$', '', name)

def get_processed_names():
    """Get all names already processed (ProcessThis=YES)"""
    processed = set()
    csv_pattern = '/Users/admin/ERA_Admin/integration_scripts/**/phase4b2_approvals*.csv'
    for csv_file in glob.glob(csv_pattern, recursive=True):
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    name = row.get('Fathom_Name') or row.get('Name', '')
                    process = row.get('ProcessThis', '')
                    if name and process == 'YES':
                        processed.add(name)
                        # Also add base name (without number suffix)
                        processed.add(strip_number_suffix(name))
        except:
            continue
    return processed

def search_past_decisions(name, threshold=0.70):
    """Fuzzy search with STRIPPED base names"""
    base_name = strip_number_suffix(name)
    
    csv_pattern = '/Users/admin/ERA_Admin/integration_scripts/**/phase4b2_approvals*.csv'
    matches = []
    
    for csv_file in glob.glob(csv_pattern, recursive=True):
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    past_name = row.get('Fathom_Name') or row.get('Name', '')
                    if not past_name:
                        continue
                    
                    past_base = strip_number_suffix(past_name)
                    
                    # Compare base names (without number suffixes)
                    similarity = SequenceMatcher(None, base_name.lower(), past_base.lower()).ratio()
                    
                    if similarity >= threshold:
                        matches.append({
                            'similarity': similarity,
                            'past_name': past_name,
                            'past_base': past_base,
                            'decision': row.get('Comments', ''),
                            'processed': row.get('ProcessThis', 'unknown')
                        })
        except:
            continue
    
    matches.sort(key=lambda x: x['similarity'], reverse=True)
    return matches

# Connect
conn = sqlite3.connect('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')
cur = conn.cursor()

# Load Airtable
airtable_lookup = {}
with open('/Users/admin/ERA_Admin/airtable/people_export.csv', 'r') as f:
    for row in csv.DictReader(f):
        name = row.get('Name', '').strip()
        if name:
            airtable_lookup[name.lower()] = name
            # Also index base names (without suffixes)
            base = strip_number_suffix(name)
            if base.lower() not in airtable_lookup:
                airtable_lookup[base.lower()] = name

print(f"✅ Loaded {len(airtable_lookup)} people from Airtable")

# Get already processed
already_processed = get_processed_names()
print(f"✅ Loaded {len(already_processed)} already-processed names from past CSVs")

# Get unprocessed from DB (all of them, no LIMIT)
cur.execute("SELECT DISTINCT name FROM participants WHERE validated_by_airtable = 0 ORDER BY name")
all_unprocessed = [row[0] for row in cur.fetchall()]

# Filter repeats
names = [n for n in all_unprocessed if n not in already_processed and strip_number_suffix(n) not in already_processed][:50]

print(f"📋 {len(names)} truly new participants (filtered {len(all_unprocessed) - len(names)} repeats)")

if len(names) == 0:
    print("\n✅ No new participants to process!")
    sys.exit(0)

print("\n" + "="*80)
print("🧠 APPLYING FUZZY MATCHING WITH INTELLIGENT REVIEW")
print("="*80)

decisions = {}
needs_review = []

for name in names:
    base_name = strip_number_suffix(name)
    d = {'name': name, 'base_name': base_name, 'decision': '', 'reason': '', 'confidence': 'MEDIUM'}
    
    # 1. Fuzzy match with STRIPPED base names
    past = search_past_decisions(name, threshold=0.70)
    
    if past and past[0]['similarity'] >= 0.95 and past[0]['processed'] == 'YES':
        # High similarity match with processed decision
        dec = past[0]['decision']
        
        if 'merge with:' in dec.lower():
            target = dec.split('merge with:')[-1].strip()
            d['decision'] = f'merge with: {target}'
            d['reason'] = f"Past decision (base match: {past[0]['past_base']})"
            d['confidence'] = 'HIGH'
        elif 'add to airtable' in dec.lower():
            d['decision'] = dec
            d['reason'] = f"Past decision (base match: {past[0]['past_base']})"
            d['confidence'] = 'HIGH'
        elif 'drop' in dec.lower():
            d['decision'] = 'drop'
            d['reason'] = f"Past decision (base match: {past[0]['past_base']})"
            d['confidence'] = 'HIGH'
    
    # 2. Check Airtable with BASE name (stripped)
    if not d['decision'] and base_name.lower() in airtable_lookup:
        d['decision'] = f"merge with: {airtable_lookup[base_name.lower()]}"
        d['reason'] = 'Found in Airtable (base name match)'
        d['confidence'] = 'HIGH'
    
    # 3. Still nothing - needs Claude's review
    if not d['decision']:
        d['decision'] = 'NEEDS_CLAUDE_REVIEW'
        d['reason'] = 'No past match, not in Airtable'
        d['confidence'] = 'NEEDS_REVIEW'
        needs_review.append(name)
    
    decisions[name] = d
    
    # Show progress
    status = "✅ HIGH" if d['confidence'] == 'HIGH' else "🔍 REVIEW"
    print(f"[{len(decisions)}/{len(names)}] {status}: {name} → {d['decision'][:50]}")

conn.close()

print("\n" + "="*80)
print("📊 INITIAL ANALYSIS COMPLETE")
print("="*80)
print(f"✅ HIGH confidence: {sum(1 for d in decisions.values() if d['confidence'] == 'HIGH')}")
print(f"🔍 NEEDS REVIEW: {len(needs_review)}")

# Save intermediate results
intermediate = Path('/tmp/batch_intermediate.json')
import json
with open(intermediate, 'w') as f:
    json.dump({
        'names': names,
        'decisions': decisions,
        'needs_review': needs_review
    }, f, indent=2)

print(f"\n💾 Intermediate results saved: {intermediate}")

if needs_review:
    print("\n" + "="*80)
    print("🛑 STOP - CLAUDE MUST REVIEW THESE ITEMS")
    print("="*80)
    print(f"\n{len(needs_review)} items need your intelligent review:")
    print()
    for name in needs_review[:20]:  # Show first 20
        base = strip_number_suffix(name)
        print(f"  • {name}")
        if name != base:
            print(f"    (base: {base})")
    
    if len(needs_review) > 20:
        print(f"\n  ... and {len(needs_review) - 20} more")
    
    print("\n" + "="*80)
    print("🧠 NEXT STEP: Claude MUST DO THE INVESTIGATION")
    print("="*80)
    print("⚠️  'NEEDS_REVIEW' = TODO FOR CLAUDE, NOT FINAL OUTPUT!")
    print()
    print("FOR EACH ITEM, USE ALL 6 TOOLS (OR UNTIL YOU HAVE A CLEAR ANSWER):")
    print()
    print("  1. ✅ PAST_LEARNINGS.md patterns")
    print("  2. ✅ Town Hall AGENDAS (if they presented → HIGH confidence add)")
    print("  3. ✅ Gmail/emails search for full names/context")
    print("  4. ✅ Past batch CSVs for previous decisions")
    print("  5. ✅ Aggressive fuzzy matching in Airtable")
    print("  6. ✅ Fathom call TITLES for organization context")
    print()
    print("🔴 DON'T STOP after 2-3 tools - USE ALL 6 or until clear answer!")
    print("🔴 NEVER output 'needs investigation' - DO THE INVESTIGATION!")
    print("🔴 NEVER propose single-name additions - find full name or ASK USER!")
    print()
    print("After investigating ALL items, update intermediate file with decisions")
    print("Then call: python3 generate_claude_html_report_v2.py")
    print()
    print("DO NOT generate HTML inline - use the existing tool!")
else:
    print("\n✅ All items matched!")
    print("Next: Call generate_claude_html_report_v2.py with decisions")

print("\n🔒 Safeguards enforced successfully.")
print("\n📋 REMEMBER: Use generate_claude_html_report_v2.py for HTML (never generate inline!)")

print("\n" + "="*80)
print("🔍 CRITICAL: REVIEW YOUR OWN WORK BEFORE PRESENTING TO USER")
print("="*80)
print()
print("After generating HTML, STOP. Do NOT present it yet.")
print()
print("Ask yourself for EACH decision:")
print("  • Did I actually READ the Town Hall agenda (not just check it exists)?")
print("  • Did I EXTRACT organization from Fathom title?")
print("  • Would user complain this is vague or incomplete?")
print("  • Is this a single name I should have found the full name for?")
print()
print("RED FLAGS to fix:")
print("  ❌ 'Town Hall participant' without full name")
print("  ❌ 'add to airtable' without 'as [specific name]'")
print("  ❌ Single lowercase names (sasi, pedro, etc.)")
print("  ❌ Device names not converted to person names")
print("  ❌ Missing org context when available")
print()
print("If you find issues: Fix them, regenerate HTML, review again.")
print("Only when ZERO issues → Present to user.")
print()
print("="*80)
