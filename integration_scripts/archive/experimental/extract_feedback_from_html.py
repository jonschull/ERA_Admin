#!/usr/bin/env python3
"""
Extract feedback from the HTML file by parsing the form state.
Alternative approach since CSV export isn't working.
"""

from bs4 import BeautifulSoup
import json

# Read the HTML file
html_file = '/Users/admin/ERA_Admin/integration_scripts/CLAUDE_RECOMMENDATIONS_20251023_1351.html'

with open(html_file, 'r') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Extract data from each row
results = []
rows = soup.find('tbody').find_all('tr')

for row in rows:
    cells = row.find_all('td')
    
    # Get recommendation
    recommendation = cells[0].find('div').text.strip()
    
    # Get checkbox state
    checkbox = cells[0].find('input', {'type': 'checkbox'})
    approved = checkbox.has_attr('checked')
    
    # Get name
    name = cells[1].text.strip()
    
    # Get confidence
    confidence = cells[2].text.strip()
    
    # Get reasoning
    reasoning = cells[3].text.strip()
    
    # Get feedback textarea (placeholder, since we can't get actual input)
    textarea = cells[5].find('textarea')
    feedback_placeholder = textarea.get('placeholder', '')
    prefilled = textarea.text.strip() if textarea.text else ''
    
    results.append({
        'name': name,
        'recommendation': recommendation,
        'confidence': confidence,
        'reasoning': reasoning,
        'approved': approved,
        'prefilled_guidance': prefilled,
        'feedback_placeholder': feedback_placeholder
    })

# Save to JSON for inspection
with open('/tmp/html_form_state.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"Extracted {len(results)} cases from HTML")
print("\nApproved (checked): ", sum(1 for r in results if r['approved']))
print("Not approved: ", sum(1 for r in results if not r['approved']))
print("\nSaved to: /tmp/html_form_state.json")
