#!/usr/bin/env python3
"""
Diagnose duplicate Airtable records by comparing data between duplicates.

Does NOT fix anything - only generates diagnostic report.
"""

import csv
from pathlib import Path
from collections import defaultdict

# Paths
SCRIPT_DIR = Path(__file__).parent
ERA_ADMIN_ROOT = SCRIPT_DIR.parent.parent
AIRTABLE_CSV = ERA_ADMIN_ROOT / "airtable" / "people_export.csv"

def load_all_records():
    """Load all records from Airtable."""
    records = []
    
    with open(AIRTABLE_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            if name:
                records.append({
                    'name': name,
                    'id': row.get('airtable_id', ''),
                    'email': row.get('Email', '').strip(),
                    'bio': row.get('Bio', '').strip(),
                    'era_member': row.get('era Member', '').strip(),
                    'publish': row.get('Publish', '').strip(),
                    'affiliated_orgs': row.get('Affiliated Orgs', '').strip(),
                    'created': row.get('created_time', ''),
                })
    
    return records

def find_duplicates(records):
    """Group records by name to find duplicates."""
    by_name = defaultdict(list)
    
    for record in records:
        by_name[record['name']].append(record)
    
    # Keep only duplicates
    duplicates = {name: recs for name, recs in by_name.items() if len(recs) > 1}
    
    return duplicates

def analyze_duplicate(name, records):
    """Analyze differences between duplicate records."""
    analysis = {
        'name': name,
        'count': len(records),
        'records': records,
        'differences': [],
        'recommendation': ''
    }
    
    # Check for data differences
    emails = set(r['email'] for r in records if r['email'])
    bios = set(r['bio'] for r in records if r['bio'])
    era_flags = set(r['era_member'] for r in records)
    publish_flags = set(r['publish'] for r in records)
    
    # Determine if same person or different
    if len(emails) > 1:
        analysis['differences'].append(f"Different emails: {', '.join(emails)}")
        analysis['recommendation'] = "DIFFERENT PEOPLE - Rename to distinguish"
    elif len(bios) > 1:
        analysis['differences'].append(f"Different bios ({len(bios)} versions)")
        analysis['recommendation'] = "SAME PERSON - Merge (keep most complete bio)"
    elif emails and len(emails) == 1:
        analysis['differences'].append("Same email")
        analysis['recommendation'] = "SAME PERSON - Merge (keep most recent)"
    else:
        analysis['differences'].append("No distinguishing data")
        analysis['recommendation'] = "NEEDS MANUAL REVIEW - Insufficient data to decide"
    
    # Note other differences
    if len(era_flags) > 1:
        analysis['differences'].append(f"Different era_member flags: {', '.join(era_flags)}")
    if len(publish_flags) > 1:
        analysis['differences'].append(f"Different publish flags: {', '.join(publish_flags)}")
    
    return analysis

def main():
    print("=" * 80)
    print("DUPLICATE RECORDS DIAGNOSTIC")
    print("=" * 80)
    print()
    
    # Load and find duplicates
    print("📥 Loading Airtable records...")
    records = load_all_records()
    duplicates = find_duplicates(records)
    
    print(f"   Total records: {len(records)}")
    print(f"   Duplicate names: {len(duplicates)}")
    print(f"   Duplicate records: {sum(len(recs) for recs in duplicates.values())}")
    print()
    
    # Analyze each duplicate
    print("🔍 Analyzing duplicates...")
    print()
    
    analyses = []
    for name, recs in sorted(duplicates.items()):
        analysis = analyze_duplicate(name, recs)
        analyses.append(analysis)
    
    # Generate report
    output_file = SCRIPT_DIR / "DUPLICATES_DIAGNOSTIC.md"
    
    with open(output_file, 'w') as f:
        f.write("# Duplicate Records Diagnostic\n\n")
        f.write("**Date:** October 26, 2025\n")
        f.write(f"**Duplicate names found:** {len(duplicates)}\n")
        f.write(f"**Total duplicate records:** {sum(len(recs) for recs in duplicates.values())}\n\n")
        f.write("---\n\n")
        
        # Group by recommendation type
        merge_same = [a for a in analyses if 'SAME PERSON' in a['recommendation']]
        different = [a for a in analyses if 'DIFFERENT PEOPLE' in a['recommendation']]
        needs_review = [a for a in analyses if 'NEEDS MANUAL REVIEW' in a['recommendation']]
        
        # Same person - merge
        f.write("## Same Person - Merge Recommended\n\n")
        if merge_same:
            for analysis in merge_same:
                f.write(f"### {analysis['name']} ({analysis['count']} records)\n\n")
                f.write(f"**Recommendation:** {analysis['recommendation']}\n\n")
                f.write("**Records:**\n")
                for i, rec in enumerate(analysis['records'], 1):
                    f.write(f"{i}. `{rec['id']}`\n")
                    f.write(f"   - Email: {rec['email'] or '(none)'}\n")
                    f.write(f"   - Bio: {('Yes (' + str(len(rec['bio'])) + ' chars)') if rec['bio'] else 'No'}\n")
                    f.write(f"   - ERA member: {rec['era_member'] or '(blank)'}\n")
                    f.write(f"   - Publish: {rec['publish'] or '(blank)'}\n")
                    f.write(f"   - Created: {rec['created']}\n")
                f.write("\n**Differences:**\n")
                for diff in analysis['differences']:
                    f.write(f"- {diff}\n")
                f.write("\n**Action Queue:**\n")
                f.write("1. Choose primary record (most complete data)\n")
                f.write("2. Merge data from other records\n")
                f.write("3. Delete duplicate records\n\n")
                f.write("---\n\n")
        else:
            f.write("*None found*\n\n")
        
        # Different people - rename
        f.write("## Different People - Rename to Distinguish\n\n")
        if different:
            for analysis in different:
                f.write(f"### {analysis['name']} ({analysis['count']} records)\n\n")
                f.write(f"**Recommendation:** {analysis['recommendation']}\n\n")
                f.write("**Records:**\n")
                for i, rec in enumerate(analysis['records'], 1):
                    f.write(f"{i}. `{rec['id']}`\n")
                    f.write(f"   - Email: {rec['email'] or '(none)'}\n")
                    f.write(f"   - ERA member: {rec['era_member'] or '(blank)'}\n")
                    f.write(f"   - Created: {rec['created']}\n")
                f.write("\n**Differences:**\n")
                for diff in analysis['differences']:
                    f.write(f"- {diff}\n")
                f.write("\n**Action Queue:**\n")
                f.write("1. Identify which person is which\n")
                f.write("2. Rename records to distinguish (e.g., add middle initial, location)\n")
                f.write("3. Update any external references\n\n")
                f.write("---\n\n")
        else:
            f.write("*None found*\n\n")
        
        # Needs review
        f.write("## Needs Manual Review\n\n")
        if needs_review:
            for analysis in needs_review:
                f.write(f"### {analysis['name']} ({analysis['count']} records)\n\n")
                f.write(f"**Recommendation:** {analysis['recommendation']}\n\n")
                f.write("**Records:**\n")
                for i, rec in enumerate(analysis['records'], 1):
                    f.write(f"{i}. `{rec['id']}`\n")
                    f.write(f"   - Email: {rec['email'] or '(none)'}\n")
                    f.write(f"   - Bio: {('Yes (' + str(len(rec['bio'])) + ' chars)') if rec['bio'] else 'No'}\n")
                    f.write(f"   - ERA member: {rec['era_member'] or '(blank)'}\n")
                    f.write(f"   - Created: {rec['created']}\n")
                f.write("\n**Differences:**\n")
                for diff in analysis['differences']:
                    f.write(f"- {diff}\n")
                f.write("\n**Action Queue:** Manual review required\n\n")
                f.write("---\n\n")
        else:
            f.write("*None found*\n\n")
        
        # Summary
        f.write("---\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **Same person (merge):** {len(merge_same)}\n")
        f.write(f"- **Different people (rename):** {len(different)}\n")
        f.write(f"- **Needs review:** {len(needs_review)}\n")
        f.write(f"- **Total duplicates:** {len(analyses)}\n\n")
        f.write("---\n\n")
        f.write("## Next Steps\n\n")
        f.write("1. Review recommendations\n")
        f.write("2. User approves merge/rename actions\n")
        f.write("3. Create fix queue for approved actions\n")
        f.write("4. Execute fixes once confident\n\n")
        f.write("**DO NOT apply fixes until user approves.**\n")
    
    print(f"✅ Diagnostic report created: {output_file}")
    print()
    print("Summary:")
    print(f"  Same person (merge): {len(merge_same)}")
    print(f"  Different people (rename): {len(different)}")
    print(f"  Needs review: {len(needs_review)}")

if __name__ == '__main__':
    main()
