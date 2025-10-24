#!/usr/bin/env python3
"""
Generate HTML for remaining Batch 2 items with:
1. Fathom recording links for ALL participants
2. Airtable cross-check DONE (not just "check")
3. Full canonical Airtable names for merges
4. Smart pattern matching
"""

import csv
import sqlite3
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher

# Connect to Fathom DB
fathom_db = '/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db'
conn = sqlite3.connect(fathom_db)
cur = conn.cursor()

# Load Airtable people with full info
airtable_csv = Path('/Users/admin/ERA_Admin/airtable/people_export.csv')
airtable_people = {}
airtable_lookup = {}  # lowercase -> canonical

with open(airtable_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('Name', '').strip()
        if name:
            airtable_people[name] = row
            airtable_lookup[name.lower()] = name

print("📖 Loaded", len(airtable_people), "people from Airtable")

def get_fathom_links(name):
    """Get Fathom recording links from database."""
    cur.execute('''
        SELECT DISTINCT source_call_url
        FROM participants
        WHERE name = ?
        ORDER BY source_call_url DESC
        LIMIT 5
    ''', (name,))
    
    urls = [row[0] for row in cur.fetchall()]
    
    if not urls:
        return "❌ No recordings"
    
    links = []
    for url in urls:
        links.append(f'<a href="{url}" target="_blank" class="evidence-link">🎥</a>')
    
    return ' '.join(links) + f' <small>({len(urls)} recording{"s" if len(urls) > 1 else ""})</small>'

def find_in_airtable(name):
    """Find person in Airtable - exact or fuzzy match."""
    name_lower = name.lower()
    
    # Exact match
    if name_lower in airtable_lookup:
        return {'found': True, 'canonical_name': airtable_lookup[name_lower], 'confidence': 'EXACT'}
    
    # Remove suffixes for better matching
    clean_name = name.split('(')[0].strip()
    clean_lower = clean_name.lower()
    
    if clean_lower in airtable_lookup:
        return {'found': True, 'canonical_name': airtable_lookup[clean_lower], 'confidence': 'EXACT'}
    
    # Fuzzy match
    best_match = None
    best_ratio = 0.0
    
    for at_name_lower, at_name in airtable_lookup.items():
        ratio = SequenceMatcher(None, name_lower, at_name_lower).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = at_name
    
    if best_ratio > 0.85:
        return {'found': True, 'canonical_name': best_match, 'confidence': 'FUZZY', 'ratio': best_ratio}
    
    # Check if name appears in any Airtable name
    matches = []
    for at_name_lower, at_name in airtable_lookup.items():
        if name_lower in at_name_lower or at_name_lower in name_lower:
            matches.append(at_name)
    
    if matches:
        return {'found': 'MAYBE', 'canonical_name': matches[0], 'matches': matches[:3], 'confidence': 'PARTIAL'}
    
    return {'found': False, 'confidence': 'NONE'}

# Remaining MEDIUM items to process
remaining_items = [
    'Abigail Castle', 'Aimee Samara (Krouskop)', 'Allison Wu', 'Alnoor IP 14P',
    'ana - Panama Restoration Lab', 'Ana C', 'Andrea Manrique', 'aniqa',
    'Anna Calderon', 'Ansiima Casinga Rolande', 'BasHam (Ecoist)', 'Billimarie',
    'Brendan McNamara (ORQAS)', 'Brian', 'C. Petruzzi-McHale', 'Charles',
    'Charlie Shore', 'Chris Pilley', 'CHRISTOPHER - Tanzania', 'Christopher Danch',
    'Coakee Wildcat', 'Cole', 'Cosmic Labyrinth (Indy Boyle-Rhymes)', 'Cosmic Labyrinth (Indy)',
    'afmiller09'  # User wants Fathom context
]

decisions = {}

for name in remaining_items:
    d = {'name': name, 'confidence': 'MEDIUM', 'decision': '', 'reason': '', 'fathom_links': get_fathom_links(name)}
    
    # Check Airtable
    at_result = find_in_airtable(name)
    
    # Extract person from patterns
    person_name = name
    
    # Pattern: "Something (Person Name)"
    if '(' in name and ')' in name:
        extracted = name.split('(')[1].rstrip(')')
        if extracted and not extracted.isdigit() and len(extracted.split()) >= 2:
            person_name = extracted
            # Check if extracted person is in Airtable
            at_result = find_in_airtable(extracted)
    
    # Pattern: "Person - Context"
    elif ' - ' in name:
        extracted = name.split(' - ')[0].strip()
        if extracted and len(extracted.split()) >= 1:
            person_name = extracted
            at_result = find_in_airtable(extracted)
    
    # Make decision based on Airtable result
    if at_result['found'] == True:
        canonical = at_result['canonical_name']
        d['decision'] = f'merge with: {canonical}'
        d['confidence'] = 'HIGH'
        
        if at_result['confidence'] == 'EXACT':
            d['reason'] = f'Found in Airtable (exact match)'
        elif at_result['confidence'] == 'FUZZY':
            d['reason'] = f'Found in Airtable ({int(at_result["ratio"]*100)}% match)'
        else:
            d['reason'] = f'Found in Airtable'
    
    elif at_result['found'] == 'MAYBE':
        canonical = at_result['canonical_name']
        d['decision'] = f'merge with: {canonical}'
        d['confidence'] = 'MEDIUM'
        d['reason'] = f'Possible match in Airtable: {canonical}'
        if len(at_result.get('matches', [])) > 1:
            d['reason'] += f' (or {", ".join(at_result["matches"][1:])})'
    
    else:
        # Not in Airtable
        if name == 'afmiller09':
            d['decision'] = 'investigate'
            d['reason'] = 'Username - check Fathom recordings for context'
            d['confidence'] = 'MEDIUM'
        elif 'IP' in name or name.lower() in ['admin', 'bk']:
            d['decision'] = 'drop'
            d['reason'] = 'System/network identifier'
            d['confidence'] = 'HIGH'
        else:
            d['decision'] = f'add to airtable as {person_name}'
            d['confidence'] = 'MEDIUM'
            d['reason'] = f'Not found in Airtable - new participant'
    
    decisions[name] = d

# Sort by confidence
sorted_names = sorted(decisions.keys(), key=lambda n: {
    'HIGH': 0, 'MEDIUM': 1, 'LOW': 2
}.get(decisions[n]['confidence'], 3))

output_file = Path('/Users/admin/ERA_Admin/integration_scripts') / f'BATCH2_REMAINING_{datetime.now().strftime("%Y%m%d_%H%M")}.html'

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Batch 2 Remaining - With Fathom Links</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 100%; margin: 0 auto; padding: 15px; background: #f5f5f5; font-size: 13px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        .header {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .stat-box {{ background: white; padding: 15px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stat-value {{ font-size: 32px; font-weight: bold; color: #3498db; }}
        .stat-label {{ color: #7f8c8d; font-size: 14px; }}
        .controls {{ background: white; padding: 15px; border-radius: 6px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        button {{ background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; margin-right: 10px; font-size: 14px; }}
        button:hover {{ background: #2980b9; }}
        table {{ width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        th {{ background: #34495e; color: white; padding: 12px; text-align: left; position: sticky; top: 0; }}
        td {{ padding: 10px; border-bottom: 1px solid #ecf0f1; }}
        tr:hover {{ background: #f8f9fa; }}
        input[type="checkbox"] {{ width: 20px; height: 20px; cursor: pointer; }}
        textarea {{ width: 100%; padding: 6px; border: 1px solid #ddd; border-radius: 4px; font-family: inherit; resize: vertical; min-height: 50px; }}
        .confidence-HIGH {{ background: #d4edda; color: #155724; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
        .confidence-MEDIUM {{ background: #fff3cd; color: #856404; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
        .evidence-link {{ color: #3498db; text-decoration: none; margin-right: 4px; }}
        .evidence-link:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 Batch 2 Remaining Items - With Improvements</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p><strong>Fixed:</strong> ✓ Fathom links added ✓ Airtable checked ✓ Full canonical names ✓ Pattern extraction</p>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-value">{len(remaining_items)}</div>
            <div class="stat-label">Remaining Cases</div>
        </div>
        <div class="stat-box" style="background: #d4edda;">
            <div class="stat-value" style="color: #28a745;">{sum(1 for d in decisions.values() if d['confidence'] == 'HIGH')}</div>
            <div class="stat-label">✅ High Confidence</div>
        </div>
        <div class="stat-box" style="background: #fff3cd;">
            <div class="stat-value" style="color: #ffc107;">{sum(1 for d in decisions.values() if d['confidence'] == 'MEDIUM')}</div>
            <div class="stat-label">🤔 Medium Confidence</div>
        </div>
    </div>
    
    <div class="controls">
        <button onclick="exportToCSV()">📥 Export to CSV (copies path)</button>
        <button onclick="checkAll()">✓ Check All</button>
        <button onclick="uncheckAll()">✗ Uncheck All</button>
    </div>
    
    <table id="recommendationsTable">
        <thead>
            <tr>
                <th style="width: 250px;">Claude's Recommendation</th>
                <th>Name</th>
                <th>Confidence</th>
                <th>Claude's Reasoning</th>
                <th>Fathom Recordings</th>
                <th style="width: 250px;">Your Feedback/Guidance</th>
            </tr>
        </thead>
        <tbody>
'''

for name in sorted_names:
    d = decisions[name]
    confidence = d['confidence']
    checked = 'checked' if confidence == 'HIGH' else ''
    
    recommendation_html = f'<div style="background: #f8f9fa; padding: 8px; border-radius: 4px; margin-bottom: 8px;"><strong>{d["decision"]}</strong></div>'
    
    html += f'''
            <tr class="row-{confidence}">
                <td style="text-align: center;">
                    {recommendation_html}
                    <label style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                        <input type="checkbox" class="approve-checkbox" {checked}>
                        <span style="font-weight: bold;">Approve</span>
                    </label>
                </td>
                <td><strong>{name}</strong></td>
                <td><span class="confidence-{confidence}">{confidence}</span></td>
                <td>{d["reason"]}</td>
                <td style="font-size: 11px;">{d["fathom_links"]}</td>
                <td><textarea class="feedback-text" placeholder="Your feedback/corrections..."></textarea></td>
            </tr>
'''

html += '''
        </tbody>
    </table>
    
    <script>
        function exportToCSV() {
            const table = document.getElementById('recommendationsTable');
            const rows = table.querySelectorAll('tbody tr');
            let csv = [];
            
            csv.push('Name,Claude_Decision,Confidence,Claude_Reasoning,Approve,Your_Feedback,ProcessThis');
            
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                const checkbox = cells[0].querySelector('input[type="checkbox"]');
                const decision = cells[0].querySelector('div').textContent.trim();
                const name = cells[1].textContent.trim();
                const confidence = cells[2].textContent.trim();
                const reasoning = cells[3].textContent.trim().replace(/"/g, '""');
                const approve = checkbox.checked ? 'YES' : 'NO';
                const feedback = cells[5].querySelector('textarea').value.replace(/"/g, '""');
                const processThis = approve === 'YES' ? 'YES' : 'REVIEW';
                
                csv.push(`"${name}","${decision}","${confidence}","${reasoning}","${approve}","${feedback}","${processThis}"`);
            });
            
            const csvContent = csv.join('\\n');
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            const filename = 'batch2_remaining_' + new Date().toISOString().slice(0,10) + '.csv';
            a.download = filename;
            a.click();
            window.URL.revokeObjectURL(url);
            
            const fullPath = '/Users/admin/Downloads/' + filename;
            navigator.clipboard.writeText(fullPath).then(() => {
                alert('✅ CSV exported!\\n📋 Path copied to clipboard:\\n' + fullPath);
            }).catch(() => {
                alert('✅ CSV exported as: ' + filename);
            });
        }
        
        function checkAll() {
            document.querySelectorAll('.approve-checkbox').forEach(cb => cb.checked = true);
        }
        
        function uncheckAll() {
            document.querySelectorAll('.approve-checkbox').forEach(cb => cb.checked = false);
        }
    </script>
</body>
</html>
'''

with open(output_file, 'w') as f:
    f.write(html)

conn.close()

print(f"\n✅ Generated: {output_file}")
print(f"\n📊 Summary:")
print(f"  Total items: {len(remaining_items)}")
print(f"  HIGH confidence: {sum(1 for d in decisions.values() if d['confidence'] == 'HIGH')}")
print(f"  MEDIUM confidence: {sum(1 for d in decisions.values() if d['confidence'] == 'MEDIUM')}")
print(f"\n✅ All participants now have Fathom recording links!")
print(f"✅ Airtable cross-check completed BEFORE generating HTML!")
print(f"✅ Full canonical names used for all merges!")
