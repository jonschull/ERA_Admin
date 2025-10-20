#!/usr/bin/env python3
"""
Process Phase 4B-2 round: Handle ProcessThis and Probe items.

Workflow:
1. Read CSV with user's ProcessThis and Probe flags
2. Process checked items automatically (merge/delete)
3. Show Probe items for manual investigation
4. User probes unclear cases in Cascade chat
5. Regenerate table with remaining + probed results
"""

import csv
import json
import sys
from pathlib import Path
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent / "FathomInventory" / "fathom_emails.db"

def read_csv_decisions(csv_path):
    """Read CSV and categorize items by user's decisions."""
    print(f"\n📖 Reading CSV: {csv_path.name}")
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    to_process = []
    to_probe = []
    to_skip = []
    
    for row in rows:
        process_this = row.get('ProcessThis', '').upper() == 'YES'
        probe = row.get('Probe', '').upper() == 'YES'
        
        if process_this:
            to_process.append(row)
        elif probe:
            to_probe.append(row)
        else:
            to_skip.append(row)
    
    print(f"\n📊 CSV Summary:")
    print(f"   ✅ Process This: {len(to_process)}")
    print(f"   🔍 Probe: {len(to_probe)}")
    print(f"   ⏭️  Skip: {len(to_skip)}")
    
    return to_process, to_probe, to_skip


def show_processing_plan(to_process):
    """Show what will be processed automatically."""
    if not to_process:
        print("\n   No items marked for processing")
        return
    
    print("\n" + "=" * 80)
    print("📋 ITEMS TO PROCESS AUTOMATICALLY")
    print("=" * 80)
    
    for row in to_process:
        name = row['Fathom_Name']
        comment = row['Comments']
        in_airtable = row['In_Airtable']
        
        print(f"\n• {name}")
        print(f"  Action: {comment}")
        print(f"  Match: {in_airtable}")


def show_probe_items(to_probe):
    """Show items that need manual probing."""
    if not to_probe:
        print("\n   No items marked for probing")
        return
    
    print("\n" + "=" * 80)
    print("🔍 ITEMS NEEDING MANUAL PROBING")
    print("=" * 80)
    print("\nThese will be investigated manually in Cascade chat:")
    
    for i, row in enumerate(to_probe, 1):
        name = row['Fathom_Name']
        gmail = row['Gmail_Count']
        in_airtable = row['In_Airtable']
        category = row['Category']
        
        print(f"\n{i}. {name}")
        print(f"   Category: {category}")
        print(f"   In Airtable: {in_airtable}")
        print(f"   Gmail: {gmail}")
        print(f"   → Will probe for: identity, matches, context")


def save_probe_list(to_probe, output_path):
    """Save probe list with embedded instructions for AI."""
    
    probe_data = {
        "_INSTRUCTIONS_FOR_CASCADE": {
            "mission": "Manually investigate each person using thoughtful analysis, not automatic pattern matching",
            "workflow": "Phase 4B-2: Iterative probing of unenriched Fathom participants",
            "methodology": [
                "1. ANALYZE NAME STRUCTURE: Identify person vs org components, clean formatting",
                "2. SEARCH AIRTABLE: Try full name + word variations, check org field for context",
                "3. SEARCH GMAIL: Run gmail_research.py, look for mentions/context/relationships",
                "4. CROSS-REFERENCE: Compare Airtable org field with name, verify Gmail matches",
                "5. RECOMMEND: Action (merge/add/ignore) + confidence + evidence + method"
            ],
            "decision_criteria": {
                "merge": "High confidence match (>85%) with corroborating evidence from multiple sources",
                "add_to_airtable": "Real person, ERA-related work, not currently in Airtable",
                "ignore": "Not ERA-related, organizational junk, or duplicate",
                "needs_more_info": "Insufficient evidence to make confident decision"
            },
            "tools_available": {
                "gmail_research": "/Users/admin/ERA_Admin/integration_scripts/gmail_research.py",
                "airtable_csv": "/Users/admin/ERA_Admin/airtable/people_export.csv (592 people)",
                "fathom_db": "/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db"
            },
            "output_format": {
                "example": "🔍 Probing [Name]...\n1. Analysis: [structure]\n2. Airtable: [results]\n3. Gmail: [findings]\n4. Cross-ref: [verification]\nRECOMMENDATION: [action]\nCONFIDENCE: [0-100]%\nEVIDENCE: [list]\nMETHOD: [approach]"
            }
        },
        "items_to_probe": []
    }
    
    for row in to_probe:
        probe_data["items_to_probe"].append({
            'name': row['Fathom_Name'],
            'category': row['Category'],
            'in_airtable': row['In_Airtable'],
            'gmail_count': row['Gmail_Count'],
            'gmail_snippet': row['Gmail_Snippet'],
            'videos': row['Videos_Count'],
            'status': 'needs_probing',
            'why_flagged': _explain_why_flagged(row)
        })
    
    with open(output_path, 'w') as f:
        json.dump(probe_data, f, indent=2)
    
    print(f"\n💾 Saved probe list with instructions: {output_path}")
    return probe_data


def _explain_why_flagged(row):
    """Explain why this item was flagged for probing."""
    reasons = []
    
    if '❌' in row['In_Airtable']:
        reasons.append("Not found in Airtable")
    if 'emails' in row['Gmail_Count'].lower():
        reasons.append("Found in Gmail - likely real person")
    if row['Category'] == 'Single Name':
        reasons.append("Single name only - identity unclear")
    if any(char in row['Fathom_Name'] for char in [',', 'www', '(', 'Locations:']):
        reasons.append("Contains special chars/org names - ambiguous")
    if '⚠️' in row['In_Airtable']:
        reasons.append("Low confidence match - needs verification")
    
    return ' | '.join(reasons) if reasons else "Manual review requested"


def main():
    """Main execution."""
    print()
    print("=" * 80)
    print("PHASE 4B-2: PROCESS ROUND")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check for CSV
    csv_pattern = SCRIPT_DIR / "phase4b2_*.csv"
    csv_files = list(SCRIPT_DIR.glob("phase4b2_*.csv"))
    
    if not csv_files:
        print("❌ No CSV file found!")
        print(f"   Expected pattern: {csv_pattern}")
        print("\n📋 Instructions:")
        print("   1. Open the HTML table in browser")
        print("   2. Review and check ProcessThis/Probe boxes")
        print("   3. Click 'Export to CSV'")
        print("   4. Save the CSV file")
        print("   5. Run this script again")
        sys.exit(1)
    
    # Use most recent CSV
    csv_path = max(csv_files, key=lambda p: p.stat().st_mtime)
    print(f"📄 Using CSV: {csv_path.name}")
    
    # Read decisions
    to_process, to_probe, to_skip = read_csv_decisions(csv_path)
    
    # Show processing plan
    show_processing_plan(to_process)
    
    # Show probe items
    show_probe_items(to_probe)
    
    print("\n" + "=" * 80)
    print("🎯 NEXT STEPS")
    print("=" * 80)
    
    if to_process:
        print(f"\n1. ✅ PROCESS {len(to_process)} items:")
        print("   → Run enrichment script on ProcessThis items")
        print("   → Merge/delete as indicated in comments")
    
    if to_probe:
        print(f"\n2. 🔍 PROBE {len(to_probe)} items:")
        print("   → Cascade will investigate each case manually")
        print("   → Get recommendations with evidence")
        print("   → Regenerate table with probe results")
        
        # Save probe list
        probe_output = SCRIPT_DIR / f"probe_list_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        probe_data = save_probe_list(to_probe, probe_output)
        
        print(f"\n💾 Probe list saved: {probe_output.name}")
        print("\n" + "=" * 80)
        print("📋 COPY THIS PROMPT FOR CASCADE:")
        print("=" * 80)
        print()
        print(f"Please follow the methodology in integration_scripts/PROBE_INSTRUCTIONS.md")
        print(f"and probe all items in integration_scripts/{probe_output.name}")
        print()
        print("=" * 80)
    
    if to_skip:
        print(f"\n3. ⏭️  SKIP {len(to_skip)} items (will appear in next round)")
    
    print("\n" + "=" * 80)
    print("⏸️  PAUSED - Waiting for your next action")
    print("=" * 80)
    print("\n📌 Choose one:")
    print("   A. Process the ProcessThis items")
    print("   B. Ask Cascade to probe the flagged items")
    print("   C. Both (process then probe)")
    print()


if __name__ == "__main__":
    main()
