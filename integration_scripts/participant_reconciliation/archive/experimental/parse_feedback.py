#!/usr/bin/env python3
"""
Parse the PDF feedback more carefully to identify:
1. Which HIGH confidence items were UNCHECKED (have corrections)
2. Which MEDIUM/LOW items were CHECKED (approved)
3. What the actual corrections/guidance are
"""

# Read the extracted PDF text
with open('/tmp/pdf_feedback.txt', 'r') as f:
    content = f.read()

# Parse entries
entries = []
lines = content.split('\n')

current_entry = None
in_feedback = False

i = 0
while i < len(lines):
    line = lines[i].strip()
    
    # Look for recommendation patterns
    if 'merge with:' in line or 'add to airtable' in line or line == 'drop':
        if current_entry:
            entries.append(current_entry)
        current_entry = {
            'recommendation': line,
            'name': '',
            'confidence': '',
            'feedback': []
        }
    elif current_entry and not current_entry['name'] and 'Approve' in line:
        # Next should be the name
        i += 1
        if i < len(lines):
            current_entry['name'] = lines[i].strip()
    elif current_entry and line in ['HIGH', 'MEDIUM', 'LOW']:
        current_entry['confidence'] = line
    elif current_entry and ('Your feedback' in line or 'Need full' in line or 'Add as' in line or 
                            'NOTE:' in line or 'merge with:' in line.lower() and 'Your' not in line):
        # This is feedback
        current_entry['feedback'].append(line)
        # Continue collecting multi-line feedback
        i += 1
        while i < len(lines) and lines[i].strip() and not any(x in lines[i] for x in ['Approve', 'HIGH', 'MEDIUM', 'LOW', 'Town Hall', 'Email Query']):
            current_entry['feedback'].append(lines[i].strip())
            i += 1
        continue
    
    i += 1

if current_entry:
    entries.append(current_entry)

# Categorize
print("="*80)
print("FEEDBACK ANALYSIS")
print("="*80)

high_with_corrections = []
medium_low_approved = []
high_approved_nochange = []
all_feedback = []

for entry in entries:
    feedback_text = ' '.join(entry['feedback'])
    
    # Skip if just placeholder text
    if feedback_text in ['Your feedback, corrections, or guidance...', '']:
        if entry['confidence'] == 'HIGH':
            high_approved_nochange.append(entry)
        continue
    
    # Has actual feedback
    all_feedback.append({
        'name': entry['name'],
        'recommendation': entry['recommendation'],
        'confidence': entry['confidence'],
        'feedback': feedback_text
    })
    
    if entry['confidence'] == 'HIGH':
        high_with_corrections.append({
            'name': entry['name'],
            'recommendation': entry['recommendation'],
            'feedback': feedback_text
        })

print(f"\n✅ HIGH CONFIDENCE - APPROVED WITH NO CHANGES: {len(high_approved_nochange)}")
for e in high_approved_nochange[:5]:
    print(f"  • {e['name']}: {e['recommendation']}")
if len(high_approved_nochange) > 5:
    print(f"  ... and {len(high_approved_nochange) - 5} more")

print(f"\n🔧 HIGH CONFIDENCE - APPROVED BUT WITH CORRECTIONS: {len(high_with_corrections)}")
for e in high_with_corrections:
    print(f"  • {e['name']}")
    print(f"    Recommendation: {e['recommendation']}")
    print(f"    Correction: {e['feedback']}")

print(f"\n📝 ALL ENTRIES WITH FEEDBACK (including MEDIUM/LOW):")
for e in all_feedback:
    print(f"\n  {e['confidence']}: {e['name']}")
    print(f"    Recommendation: {e['recommendation']}")
    print(f"    Feedback: {e['feedback']}")

print("\n" + "="*80)
