#!/usr/bin/env python3
"""
AUDIT: Compare database state against all past decisions.

Goal: Find EVERY discrepancy and classify by pattern.
This is the comprehension phase - no fixes, just understanding.
"""

import sqlite3
import csv
from pathlib import Path
from collections import defaultdict

DB_PATH = Path('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')
PAST_DECISIONS_DIR = Path('/Users/admin/ERA_Admin/integration_scripts/past_decisions')

# Load database state
def get_all_participant_names():
    """Get all current participant names from database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM participants ORDER BY name")
    names = set(row[0] for row in cursor.fetchall())
    conn.close()
    return names

# Load all past decisions
def load_all_decisions():
    """Load every decision with ProcessThis=YES from all CSVs."""
    decisions = []
    
    for csv_file in sorted(PAST_DECISIONS_DIR.glob('phase4b2_approvals_batch*.csv')):
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Clean emoji markers
                fathom_name = row.get('Fathom_Name', '').strip().split('🔁')[0].strip()
                process_this = row.get('ProcessThis', '').upper() == 'YES'
                comment = row.get('Comments', '').strip()
                
                if process_this and fathom_name:
                    decisions.append({
                        'name': fathom_name,
                        'comment': comment,
                        'csv_file': csv_file.name
                    })
    
    return decisions

# Classify decisions
def classify_decision(comment):
    """Classify what type of action was intended."""
    comment_lower = comment.lower()
    
    if comment_lower in ['drop', 'drop it', 'duplicate']:
        return 'DROP', None
    elif comment.startswith('merge with:'):
        target = comment[len('merge with:'):].strip()
        return 'MERGE', target
    elif 'add to airtable' in comment_lower:
        # Try to extract target name
        if ' as ' in comment_lower:
            target = comment.split(' as ', 1)[1].strip()
            return 'ADD_AS', target
        else:
            return 'ADD', None
    else:
        return 'OTHER', comment

def main():
    print("=" * 80)
    print("DATABASE vs DECISIONS AUDIT")
    print("=" * 80)
    
    # Load current state
    print("\n📊 Loading current database state...")
    current_names = get_all_participant_names()
    print(f"   Found {len(current_names)} distinct names in database")
    
    # Load all decisions
    print("\n📋 Loading all past decisions...")
    decisions = load_all_decisions()
    print(f"   Found {len(decisions)} decisions with ProcessThis=YES")
    
    # Analyze discrepancies
    print("\n🔍 Analyzing discrepancies...")
    
    discrepancies = defaultdict(list)
    
    for decision in decisions:
        name = decision['name']
        comment = decision['comment']
        csv_file = decision['csv_file']
        
        action_type, target = classify_decision(comment)
        still_exists = name in current_names
        
        # Check for discrepancy
        discrepancy = None
        
        if action_type in ['DROP', 'MERGE', 'ADD_AS']:
            # These actions should result in name being GONE from database
            if still_exists:
                discrepancy = f"Should be gone (action: {action_type})"
                if target:
                    discrepancy += f" → {target}"
        
        if discrepancy:
            discrepancies[action_type].append({
                'name': name,
                'action': action_type,
                'target': target,
                'comment': comment,
                'csv_file': csv_file,
                'issue': discrepancy
            })
    
    # Report by pattern
    print("\n" + "=" * 80)
    print("DISCREPANCIES BY PATTERN")
    print("=" * 80)
    
    total_issues = 0
    
    for action_type, issues in sorted(discrepancies.items()):
        print(f"\n### {action_type}: {len(issues)} issues")
        print(f"\nFirst 10 examples:")
        for item in issues[:10]:
            print(f"  - {item['name']}")
            print(f"    Comment: {item['comment']}")
            print(f"    File: {item['csv_file']}")
            print()
        
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")
        
        total_issues += len(issues)
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total decisions: {len(decisions)}")
    print(f"Total discrepancies: {total_issues}")
    print(f"Success rate: {((len(decisions) - total_issues) / len(decisions) * 100):.1f}%")
    
    # Export detailed report
    report_file = Path('audit_report.csv')
    with open(report_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Action', 'Target', 'Comment', 'CSV_File', 'Issue'])
        
        for action_type, issues in sorted(discrepancies.items()):
            for item in issues:
                writer.writerow([
                    item['name'],
                    item['action'],
                    item['target'] or '',
                    item['comment'],
                    item['csv_file'],
                    item['issue']
                ])
    
    print(f"\n📄 Detailed report written to: {report_file}")
    print("\n✅ Audit complete!")

if __name__ == '__main__':
    main()
