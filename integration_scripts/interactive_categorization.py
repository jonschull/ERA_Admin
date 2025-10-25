#!/usr/bin/env python3
"""
Interactive Categorization: Force Claude to judge each case individually.

This is the "Evaluator-Optimizer" pattern - Claude must apply intelligence
to each case rather than trying to script pattern matching.
"""

import sqlite3
import csv
import json
from pathlib import Path

DB_PATH = Path('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')
PAST_DECISIONS_DIR = Path('/Users/admin/ERA_Admin/integration_scripts/past_decisions')
OUTPUT_FILE = Path('claude_categorizations.json')

def load_decisions_needing_attention():
    """Load all decisions with ProcessThis=YES that still exist in DB."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all current names
    cursor.execute("SELECT DISTINCT name FROM participants")
    current_names = set(row[0] for row in cursor.fetchall())
    
    # Load decisions
    decisions = []
    for csv_file in sorted(PAST_DECISIONS_DIR.glob('phase4b2_approvals_batch*.csv')):
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                variant = row.get('Fathom_Name', '').strip().split('🔁')[0].strip()
                comment = row.get('Comments', '').strip()
                process_this = row.get('ProcessThis', '').upper() == 'YES'
                
                if process_this and variant and variant in current_names:
                    # Get meeting count
                    cursor.execute("""
                        SELECT source_call_url, source_call_title 
                        FROM participants 
                        WHERE name = ?
                    """, (variant,))
                    row_data = cursor.fetchone()
                    url_list = row_data[0] if row_data else ""
                    meeting_count = len([u for u in url_list.split(',') if u.strip()])
                    
                    decisions.append({
                        'variant': variant,
                        'csv_comment': comment,
                        'csv_file': csv_file.name,
                        'meeting_count': meeting_count
                    })
    
    conn.close()
    return decisions

def main():
    print("=" * 80)
    print("INTERACTIVE CATEGORIZATION")
    print("Claude must judge each case using PAST_LEARNINGS knowledge")
    print("=" * 80)
    
    decisions = load_decisions_needing_attention()
    print(f"\nFound {len(decisions)} decisions that need attention")
    print(f"(Variants still exist in database)")
    
    print("\n" + "=" * 80)
    print("INSTRUCTIONS FOR CLAUDE:")
    print("=" * 80)
    print("For each variant, YOU must determine:")
    print("1. What is the correct target name? (or 'DROP' if no target)")
    print("2. What is your confidence? (HIGH/MEDIUM/LOW)")
    print("3. What is your reasoning?")
    print()
    print("Use your memory of PAST_LEARNINGS.md to answer.")
    print("Type your answers when prompted.")
    print("=" * 80)
    
    input("\nPress Enter when you (Claude) are ready to begin...")
    
    categorizations = []
    
    # Test mode: only do first 10
    import sys
    limit = 10 if '--test' in sys.argv else len(decisions)
    
    for i, decision in enumerate(decisions[:limit], 1):
        print(f"\n{'=' * 80}")
        print(f"CASE {i}/{limit}")
        print(f"{'=' * 80}")
        print(f"Variant: {decision['variant']}")
        print(f"CSV says: {decision['csv_comment']}")
        print(f"Meetings: {decision['meeting_count']} Town Hall attendances")
        print()
        
        print("CLAUDE - Based on your memory of PAST_LEARNINGS:")
        target = input("  Target name (or 'DROP' or 'SKIP'): ").strip()
        
        if target.upper() == 'SKIP':
            continue
        
        confidence = input("  Confidence (HIGH/MEDIUM/LOW): ").strip().upper()
        reasoning = input("  Reasoning: ").strip()
        
        categorizations.append({
            'variant': decision['variant'],
            'target': target if target.upper() != 'DROP' else None,
            'action': 'DROP' if target.upper() == 'DROP' else 'MERGE',
            'confidence': confidence,
            'reasoning': reasoning,
            'csv_comment': decision['csv_comment'],
            'csv_file': decision['csv_file'],
            'meeting_count': decision['meeting_count']
        })
        
        # Save progress after each entry
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(categorizations, f, indent=2)
    
    print(f"\n{'=' * 80}")
    print(f"COMPLETE!")
    print(f"{'=' * 80}")
    print(f"Processed: {len(categorizations)} cases")
    print(f"Saved to: {OUTPUT_FILE}")
    print()
    print("Next: Review categorizations and generate diagnostic report")

if __name__ == '__main__':
    main()
