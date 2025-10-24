#!/usr/bin/env python3
"""
Prepare Phase 4B-2 data for INTELLIGENT AI analysis.

This extracts ALL the context and formats it for Claude to analyze:
- Full Town Hall snippets (not just counts)
- Actual Gmail content (not just counts)
- Airtable fuzzy matches with scores
- Learned patterns from previous rounds

Claude then makes intelligent decisions by READING the content,
not just looking at statistics.
"""

import json
import sqlite3
from pathlib import Path
from town_hall_search import TownHallSearch

def get_gmail_details(name):
    """Get actual Gmail email subjects/snippets for this person."""
    import subprocess
    
    try:
        cmd = ['python3', 'gmail_research.py', name, '--limit', '3']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if 'No emails found' in result.stdout:
            return None
        
        # Extract actual email content
        lines = result.stdout.split('\n')
        emails = []
        current_email = {}
        
        for line in lines:
            if line.startswith(('1. **', '2. **', '3. **')):
                if current_email:
                    emails.append(current_email)
                current_email = {'subject': line.split('**')[1]}
            elif 'From:' in line:
                current_email['from'] = line.split('From:', 1)[1].strip()
            elif 'Date:' in line:
                current_email['date'] = line.split('Date:', 1)[1].strip()
            elif 'Context:' in line or 'Snippet:' in line:
                current_email['context'] = line.split(':', 1)[1].strip()
        
        if current_email:
            emails.append(current_email)
        
        return emails if emails else None
        
    except Exception as e:
        return None


def format_for_claude(participants):
    """Format all participants for Claude's intelligent analysis."""
    
    # Load Town Hall searcher
    th_search = TownHallSearch(use_local_db=True)
    
    output = """# Phase 4B-2: Intelligent AI Analysis

You are Claude, an intelligent assistant helping reconcile 195 Fathom participants with the ERA Airtable database.

## Your Task

For each participant below, **MAKE A DECISION**:
- `merge with: [Full Name]` - if this is an existing person (use exact Airtable name)
- `add to airtable` - if this is a new ERA participant who should be added
- `drop` - if this is a device, organization, or clearly not ERA-related

## Guidelines

1. **3+ Town Hall meetings = probably add** (unless already in Airtable)
2. **Number variants** (e.g., "Joshua (2)", "Joshua (4)") = same person as base name
3. **Jon Schull variants** = merge to "Jon Schull" (that's the user)
4. **High Airtable match (80%+)** = merge with confidence
5. **Device names** ("iPhone", "Galaxy") = drop
6. **Single names in 3+ meetings** = check Gmail/context to get full name, then add
7. **Read the actual content** - don't just look at counts

## Output Format

For each case, provide:
```
CASE N: [Name]
DECISION: [merge with: X | add to airtable | drop]
REASON: [brief 1-2 sentence explanation]
VALIDATE: [link if applicable]
```

---

"""
    
    for i, p in enumerate(participants, 1):
        output += f"\n## CASE {i}: {p['name']}\n\n"
        
        # Basic info
        output += f"**Category:** {p.get('category', 'unknown')}\n"
        output += f"**Fathom records:** {p.get('record_count', p.get('count', 1))}\n\n"
        
        # Town Hall - GET ACTUAL SNIPPETS
        th_results = th_search.search_agendas_for_name(p['name'], max_results=3)
        if th_results:
            output += f"**Town Hall:** Found in {len(th_results)} meeting(s)\n"
            for th in th_results:
                output += f"- **{th['date']}:** {th.get('snippet', '')}\n"
            output += "\n"
        else:
            output += "**Town Hall:** Not found\n\n"
        
        # Gmail - GET ACTUAL CONTENT
        gmail_details = get_gmail_details(p['name'])
        if gmail_details:
            output += f"**Gmail:** Found {len(gmail_details)} emails\n"
            for email in gmail_details[:2]:
                output += f"- **Subject:** {email.get('subject', 'N/A')}\n"
                if email.get('context'):
                    output += f"  Context: {email['context'][:100]}...\n"
            output += "\n"
        else:
            output += "**Gmail:** Not found\n\n"
        
        # Airtable match
        if p.get('in_airtable'):
            output += f"**Airtable match:** {p['airtable_match']} ({p['airtable_score']}% confidence)\n"
            output += f"   Match method: {p.get('airtable_method', 'full_name')}\n\n"
        else:
            output += "**Airtable:** No match found\n\n"
        
        # Learned mapping (if any)
        if p.get('has_learned_mapping'):
            output += f"**Previous round:** {p.get('learned_reason', 'Resolved before')}\n"
            output += f"   Decision was: {p.get('suggested_action', 'N/A')}\n\n"
        
        # Videos for reference
        if p.get('videos'):
            output += f"**Fathom recording:** {p['videos'][0]['url']}\n\n"
        
        output += "---\n"
    
    return output


def main():
    # Load participant data
    data_file = '/tmp/phase4b2_test_data.json'
    
    if not Path(data_file).exists():
        print("❌ Error: No participant data found")
        print("   Run generate_phase4b2_table.py first")
        return
    
    with open(data_file, 'r') as f:
        participants = json.load(f)
    
    print(f"📝 Preparing {len(participants)} participants for AI analysis...")
    print("   This will:")
    print("   - Search Town Hall agendas for each person")
    print("   - Fetch Gmail content (not just counts)")
    print("   - Format everything for Claude to read and decide")
    print()
    print("   This may take 2-3 minutes...")
    print()
    
    # Format for Claude
    markdown = format_for_claude(participants)
    
    # Save to file
    output_file = Path(__file__).parent / 'ai_analysis_input.md'
    with open(output_file, 'w') as f:
        f.write(markdown)
    
    print(f"✅ Prepared AI analysis input")
    print(f"📄 Saved to: {output_file}")
    print()
    print("📋 Next steps:")
    print("  1. Open ai_analysis_input.md")
    print("  2. Copy entire contents")
    print("  3. Paste to Claude")
    print("  4. Claude will analyze and return decisions")
    print("  5. Apply Claude's decisions to CSV")
    print()


if __name__ == '__main__':
    main()
