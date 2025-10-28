#!/usr/bin/env python3
"""
Diagnose priority 0 members by finding potential spelling mismatches
between Airtable names and Database names using fuzzy matching.

Does NOT fix anything - only generates diagnostic report.
"""

import csv
import sqlite3
from pathlib import Path
from fuzzywuzzy import fuzz

# Paths
SCRIPT_DIR = Path(__file__).parent
ERA_ADMIN_ROOT = SCRIPT_DIR.parent.parent
AIRTABLE_CSV = ERA_ADMIN_ROOT / "airtable" / "people_export.csv"
FATHOM_DB = ERA_ADMIN_ROOT / "FathomInventory" / "fathom_emails.db"
PRIORITY_LIST = SCRIPT_DIR / "batches" / "batch1_priority_list.csv"

def load_priority_0_members():
    """Load all priority 0 ERA members from the priority list."""
    priority_0 = []
    
    with open(PRIORITY_LIST) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['th_count'] == '0':
                priority_0.append(row['name'])
    
    return priority_0

def load_airtable_era_members():
    """Load ERA members from Airtable."""
    era_members = {}
    
    with open(AIRTABLE_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            era_member = row.get('era Member', '').strip()
            if era_member == 'True':
                era_members[name] = {
                    'id': row.get('airtable_id', ''),
                    'email': row.get('Email', ''),
                }
    
    return era_members

def load_database_members():
    """Load all members from database."""
    conn = sqlite3.connect(FATHOM_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT DISTINCT name, era_member, email
        FROM participants
        WHERE era_member = 1
        ORDER BY name
    ''')
    
    db_members = {}
    for row in cursor.fetchall():
        name = row[0]
        db_members[name] = {
            'era_member': row[1],
            'email': row[2]
        }
    
    conn.close()
    return db_members

def find_potential_matches(airtable_name, db_names, threshold=85):
    """Find potential database name matches for an Airtable name."""
    matches = []
    
    for db_name in db_names:
        # Try different fuzzy matching strategies
        ratio = fuzz.ratio(airtable_name.lower(), db_name.lower())
        partial = fuzz.partial_ratio(airtable_name.lower(), db_name.lower())
        token_sort = fuzz.token_sort_ratio(airtable_name.lower(), db_name.lower())
        
        best_score = max(ratio, partial, token_sort)
        
        if best_score >= threshold:
            matches.append({
                'db_name': db_name,
                'score': best_score,
                'ratio': ratio,
                'partial': partial,
                'token_sort': token_sort
            })
    
    # Sort by best score descending
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches

def main():
    print("=" * 80)
    print("PRIORITY 0 MISMATCH DIAGNOSTIC")
    print("=" * 80)
    print()
    
    # Load data
    print("📥 Loading data...")
    priority_0 = load_priority_0_members()
    airtable_members = load_airtable_era_members()
    db_members = load_database_members()
    
    # Filter to priority 0 ERA members
    priority_0_era = [name for name in priority_0 if name in airtable_members]
    
    print(f"   Priority 0 members: {len(priority_0)}")
    print(f"   Priority 0 ERA members: {len(priority_0_era)}")
    print(f"   Database ERA members: {len(db_members)}")
    print()
    
    # Find potential matches
    print("🔍 Finding potential spelling mismatches...")
    print()
    
    results = {
        'high_confidence': [],  # 95%+
        'likely_match': [],     # 85-94%
        'possible_match': [],   # 70-84%
        'no_match': []          # <70%
    }
    
    for airtable_name in sorted(priority_0_era):
        matches = find_potential_matches(airtable_name, db_members.keys())
        
        if not matches:
            results['no_match'].append({
                'airtable_name': airtable_name,
                'airtable_data': airtable_members[airtable_name]
            })
        else:
            best_match = matches[0]
            category = (
                'high_confidence' if best_match['score'] >= 95 else
                'likely_match' if best_match['score'] >= 85 else
                'possible_match'
            )
            
            results[category].append({
                'airtable_name': airtable_name,
                'airtable_data': airtable_members[airtable_name],
                'db_name': best_match['db_name'],
                'db_data': db_members[best_match['db_name']],
                'score': best_match['score'],
                'all_matches': matches[:3]  # Top 3
            })
    
    # Generate report
    output_file = SCRIPT_DIR / "PRIORITY_0_MATCHES_DIAGNOSTIC.md"
    
    with open(output_file, 'w') as f:
        f.write("# Priority 0 Spelling Mismatch Diagnostic\n\n")
        f.write("**Date:** October 26, 2025\n")
        f.write(f"**Analyzed:** {len(priority_0_era)} priority 0 ERA members\n\n")
        f.write("---\n\n")
        
        # High confidence matches
        f.write("## High Confidence Matches (95%+ similarity)\n\n")
        f.write("**These are almost certainly spelling variations of the same person.**\n\n")
        
        if results['high_confidence']:
            for item in results['high_confidence']:
                f.write(f"### {item['airtable_name']} → {item['db_name']}\n")
                f.write(f"**Score:** {item['score']}%\n\n")
                f.write(f"**Airtable:** {item['airtable_data']['id']}\n")
                f.write(f"- Email: {item['airtable_data']['email']}\n\n")
                f.write(f"**Database:**\n")
                f.write(f"- Email: {item['db_data']['email']}\n\n")
                f.write("**Recommended Action:** Standardize name in Airtable to match database\n\n")
                f.write("---\n\n")
        else:
            f.write("*None found*\n\n")
        
        # Likely matches
        f.write("## Likely Matches (85-94% similarity)\n\n")
        f.write("**These are probably the same person - verify before fixing.**\n\n")
        
        if results['likely_match']:
            for item in results['likely_match']:
                f.write(f"### {item['airtable_name']} → {item['db_name']}\n")
                f.write(f"**Score:** {item['score']}%\n\n")
                f.write(f"**Airtable:** {item['airtable_data']['id']}\n")
                f.write(f"- Email: {item['airtable_data']['email']}\n\n")
                f.write(f"**Database:**\n")
                f.write(f"- Email: {item['db_data']['email']}\n\n")
                f.write("**Recommended Action:** Verify match, then standardize name\n\n")
                f.write("---\n\n")
        else:
            f.write("*None found*\n\n")
        
        # Possible matches
        f.write("## Possible Matches (70-84% similarity)\n\n")
        f.write("**These might be the same person - needs manual review.**\n\n")
        
        if results['possible_match']:
            for item in results['possible_match']:
                f.write(f"### {item['airtable_name']}\n")
                f.write(f"**Top matches:**\n")
                for match in item['all_matches']:
                    f.write(f"- {match['db_name']} ({match['score']}%)\n")
                f.write(f"\n**Airtable:** {item['airtable_data']['id']}\n")
                f.write(f"- Email: {item['airtable_data']['email']}\n\n")
                f.write("**Recommended Action:** Manual review needed\n\n")
                f.write("---\n\n")
        else:
            f.write("*None found*\n\n")
        
        # No matches
        f.write("## No Matches Found (<70% similarity)\n\n")
        f.write("**These may be:**\n")
        f.write("1. Real members who haven't attended Town Halls yet\n")
        f.write("2. Incorrectly marked as ERA members\n")
        f.write("3. Very different name formats (username vs real name)\n\n")
        
        if results['no_match']:
            for item in results['no_match']:
                f.write(f"- **{item['airtable_name']}** ({item['airtable_data']['id']})\n")
                f.write(f"  - Email: {item['airtable_data']['email']}\n")
            f.write("\n**Recommended Action:** Manual verification of membership status\n\n")
        else:
            f.write("*None found*\n\n")
        
        # Summary
        f.write("---\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **High confidence matches:** {len(results['high_confidence'])}\n")
        f.write(f"- **Likely matches:** {len(results['likely_match'])}\n")
        f.write(f"- **Possible matches:** {len(results['possible_match'])}\n")
        f.write(f"- **No matches:** {len(results['no_match'])}\n")
        f.write(f"- **Total analyzed:** {len(priority_0_era)}\n\n")
        f.write("---\n\n")
        f.write("## Next Steps\n\n")
        f.write("1. Review high confidence matches - queue for name standardization\n")
        f.write("2. Verify likely matches manually\n")
        f.write("3. Research possible matches\n")
        f.write("4. Validate membership status of no-match members\n")
        f.write("5. Create fix queue once confident\n\n")
        f.write("**DO NOT apply fixes until user approves.**\n")
    
    print(f"✅ Diagnostic report created: {output_file}")
    print()
    print("Summary:")
    print(f"  High confidence: {len(results['high_confidence'])}")
    print(f"  Likely matches: {len(results['likely_match'])}")
    print(f"  Possible matches: {len(results['possible_match'])}")
    print(f"  No matches: {len(results['no_match'])}")

if __name__ == '__main__':
    main()
