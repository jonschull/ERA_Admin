#!/usr/bin/env python3
"""
Apply Claude's intelligent decisions back to the Phase 4B-2 CSV.

Takes Claude's analysis output and updates the CSV with:
- Claude's decision
- Claude's reasoning
- Auto-checks "ProcessThis" for high-confidence decisions
"""

import csv
import sys
import re
from pathlib import Path

def parse_claude_output(text):
    """Parse Claude's decisions from markdown output."""
    
    decisions = {}
    
    # Pattern: CASE N: [Name]
    # DECISION: [decision]
    # REASON: [reason]
    
    cases = re.findall(
        r'CASE\s+(\d+):\s+(.+?)\n.*?DECISION:\s+(.+?)\n.*?REASON:\s+(.+?)(?:\nVALIDATE:|---|\n\n|$)',
        text,
        re.DOTALL
    )
    
    for case_num, name, decision, reason in cases:
        decisions[name.strip()] = {
            'decision': decision.strip(),
            'reason': reason.strip(),
            'case_num': int(case_num)
        }
    
    return decisions


def apply_decisions_to_csv(csv_path, decisions):
    """Apply Claude's decisions to the CSV file."""
    
    # Read CSV
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    updated = 0
    high_confidence = 0
    
    for row in rows:
        name = row['Fathom_Name']
        
        if name in decisions:
            decision = decisions[name]
            
            # Update Comments with Claude's analysis
            claude_note = f"[CLAUDE] {decision['decision']}\nReason: {decision['reason']}"
            
            # Preserve any existing comments
            existing = row['Comments'].strip()
            if existing and not existing.startswith('[CLAUDE]'):
                row['Comments'] = f"{claude_note}\n\nPrevious: {existing}"
            else:
                row['Comments'] = claude_note
            
            # Auto-check ProcessThis for non-drop decisions
            if decision['decision'].lower() != 'drop':
                row['ProcessThis'] = 'YES'
                high_confidence += 1
            else:
                row['ProcessThis'] = 'NO'
            
            updated += 1
    
    # Write updated CSV
    output_path = Path(csv_path).parent / f"{Path(csv_path).stem}_WITH_AI_DECISIONS.csv"
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\n✅ Applied Claude's decisions")
    print(f"   Updated: {updated}/{len(rows)} participants")
    print(f"   Auto-checked: {high_confidence} for processing")
    print(f"   Output: {output_path}")
    print()
    print("📖 Next steps:")
    print("  1. Review the updated CSV")
    print("  2. Make any overrides needed")
    print("  3. Run: python3 execute_phase4b2_actions.py [csv_path]")
    print()
    
    return output_path


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 apply_ai_decisions.py [csv_file] [claude_output_file]")
        print()
        print("Example:")
        print("  1. Save Claude's response to 'claude_decisions.txt'")
        print("  2. python3 apply_ai_decisions.py approvals.csv claude_decisions.txt")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    claude_output_path = sys.argv[2]
    
    # Read Claude's output
    with open(claude_output_path, 'r') as f:
        claude_text = f.read()
    
    # Parse decisions
    print("📖 Parsing Claude's decisions...")
    decisions = parse_claude_output(claude_text)
    print(f"   Found {len(decisions)} decisions")
    
    # Apply to CSV
    apply_decisions_to_csv(csv_path, decisions)


if __name__ == '__main__':
    main()
