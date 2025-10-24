#!/usr/bin/env python3
"""
Extract medium-confidence cases for AI (Claude) batch analysis.

Creates a markdown file with all context for each unclear case:
- Name from Fathom
- Town Hall context (with snippets)
- Gmail information
- Airtable fuzzy matches
- Existing recommendation

Human then pastes this to Claude for batch analysis.
"""

import json
import sys
from pathlib import Path

def extract_medium_cases(participants):
    """Extract all medium-confidence cases with full context."""
    
    medium_cases = []
    
    for p in participants:
        ai_rec = p.get('ai_recommendation', {})
        if ai_rec.get('confidence') == 'NEEDS AI REVIEW':
            medium_cases.append(p)
    
    return medium_cases


def format_for_ai_analysis(cases):
    """Format cases as markdown for Claude to analyze."""
    
    output = f"""# Phase 4B-2: Medium Confidence Cases for AI Review

**Total cases:** {len(cases)}

These participants need intelligent judgment to make the right decision.
For each case, I've provided:
- What Fathom shows
- Town Hall context (where they've participated)
- Gmail presence
- Possible Airtable matches

**Your task:** For each case, recommend one of:
- `merge with: [Full Name]` - if this is clearly an existing person
- `add to airtable` - if this is clearly a new person who should be added
- `drop` - if this is clearly not ERA-related or a device/org name
- `manual review` - if truly unclear and needs human judgment

**Format your response as:**
```
CASE 1: [decision]
Reasoning: [brief explanation]

CASE 2: [decision]
Reasoning: [brief explanation]
...
```

---

"""
    
    for i, p in enumerate(cases, 1):
        output += f"\n## CASE {i}: {p['name']}\n\n"
        
        # Current AI suggestion
        ai_rec = p.get('ai_recommendation', {})
        output += f"**Current AI suggestion:** {ai_rec.get('action', 'unclear')}\n"
        output += f"**Reasoning:** {ai_rec.get('reasoning', 'N/A')}\n\n"
        
        # Town Hall context
        th = p.get('town_hall', [])
        if th:
            output += f"**Town Hall presence:** Found in {len(th)} meeting(s)\n"
            for meeting in th[:3]:
                output += f"- {meeting['date']}: {meeting.get('snippet', '')[:150]}\n"
            output += "\n"
        else:
            output += "**Town Hall presence:** Not found\n\n"
        
        # Gmail
        gmail = p.get('gmail', {})
        if gmail.get('found'):
            output += f"**Gmail:** Found in {gmail['count']} emails\n"
            if gmail.get('snippet'):
                output += f"- Context: {gmail['snippet'][:150]}\n"
            output += "\n"
        else:
            output += "**Gmail:** Not found\n\n"
        
        # Airtable match
        if p.get('in_airtable'):
            output += f"**Airtable match:** {p['airtable_match']} ({p['airtable_score']}% confidence)\n\n"
        else:
            output += "**Airtable match:** None\n\n"
        
        # Category
        output += f"**Category:** {p['category']}\n"
        output += f"**Fathom appearances:** {p['record_count']} records\n\n"
        
        output += "---\n"
    
    return output


def main():
    # Load participant data
    data_file = '/tmp/phase4b2_test_data.json'
    
    if not Path(data_file).exists():
        print("❌ Error: No participant data found")
        print("   Run generate_phase4b2_table.py first")
        sys.exit(1)
    
    with open(data_file, 'r') as f:
        participants = json.load(f)
    
    # Extract medium cases
    medium_cases = extract_medium_cases(participants)
    
    if not medium_cases:
        print("✅ No medium-confidence cases found!")
        print("   All cases are either high confidence (auto-recommend) or low (skip)")
        return
    
    # Format for AI
    markdown = format_for_ai_analysis(medium_cases)
    
    # Save to file
    output_file = Path(__file__).parent / 'medium_confidence_cases.md'
    with open(output_file, 'w') as f:
        f.write(markdown)
    
    print(f"\n✅ Extracted {len(medium_cases)} medium-confidence cases")
    print(f"📄 Saved to: {output_file}")
    print()
    print("📋 Next steps:")
    print("  1. Open medium_confidence_cases.md")
    print("  2. Copy entire contents")
    print("  3. Paste to Claude in chat")
    print("  4. Claude will analyze and provide recommendations")
    print("  5. Update CSV with Claude's recommendations")
    print()


if __name__ == '__main__':
    main()
