#!/usr/bin/env python3
"""
Generate Batch 3 HTML - Complete with ALL evidence
Following AI_ASSISTANT_CONTEXT_RECOVERY.md
"""
import csv
import sqlite3
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher

print("="*80)
print("🤖 BATCH 3 GENERATION - ALL EVIDENCE INCLUDED")
print("="*80)

# Connect to Fathom DB
fathom_db = '/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db'
conn = sqlite3.connect(fathom_db)
cur = conn.cursor()

# Load Airtable
airtable_csv = Path('/Users/admin/ERA_Admin/airtable/people_export.csv')
airtable_lookup = {}
with open(airtable_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('Name', '').strip()
        if name:
            airtable_lookup[name.lower()] = name

# Load PAST_LEARNINGS
PAST = {
    'phones': {'16319034965': 'Sean Pettersen', '18022588598': 'Michael Mayer'},
    'orgs': {'BioIntegrity': 'Chris Searles', 'Beck Bio4Climate': 'Beck Mordini', 
             'Agri-Tech Producers LLC, Joe James': 'Joe James'},
    'variants': {'Aditi': 'Aditi Singh', 'Ana': 'Ana Calderon', 'Angelique': 'Angelique Garcia',
                 'CBiradar': 'Chandrashekhar Biradar', 'andreaseke': 'Andreas Eke',
                 "Andres's iPhone (2)": 'Andres Garcia', 'aniqa': 'Aniqa Moinuddin',
                 'Ana C': 'Ana Calderon', 'Aimee Samara (Krouskop)': 'Aimee Samara',
                 'Brendan McNamara (ORQAS)': 'Brendan McNamara', 'Billimarie': 'Billimarie Lubiano Robinson'}
}

# Get next 50 unprocessed
cur.execute("SELECT DISTINCT name FROM participants WHERE validated_by_airtable = 0 ORDER BY name LIMIT 50")
names = [row[0] for row in cur.fetchall()]

decisions = {}
for name in names:
    # Check past learnings first
    if name in PAST['phones']:
        d = {'decision': f"merge with: {PAST['phones'][name]}", 'confidence': 'HIGH',
             'reason': f"Phone number from past learnings → {PAST['phones'][name]}"}
    elif name in PAST['orgs']:
        d = {'decision': f"merge with: {PAST['orgs'][name]}", 'confidence': 'HIGH',
             'reason': f"Organization from past learnings → {PAST['orgs'][name]}"}
    elif name in PAST['variants']:
        d = {'decision': f"merge with: {PAST['variants'][name]}", 'confidence': 'HIGH',
             'reason': f"Name variant from past learnings → {PAST['variants'][name]}"}
    # Check Airtable
    elif name.lower() in airtable_lookup:
        canonical = airtable_lookup[name.lower()]
        d = {'decision': f"merge with: {canonical}", 'confidence': 'HIGH',
             'reason': 'Found in Airtable (exact match)'}
    # Patterns
    elif name in ['admin', 'bk']:
        d = {'decision': 'drop', 'confidence': 'HIGH', 'reason': 'System account'}
    elif name == 'afmiller09':
        d = {'decision': 'investigate', 'confidence': 'MEDIUM', 'reason': 'Username - check Fathom recordings'}
    elif '(' in name and ')' in name and not any(c.isdigit() for c in name.split('(')[1].split(')')[0]):
        extracted = name.split('(')[1].rstrip(')')
        if len(extracted.split()) >= 2:
            # Check if extracted person in Airtable
            if extracted.lower() in airtable_lookup:
                canonical = airtable_lookup[extracted.lower()]
                d = {'decision': f"merge with: {canonical}", 'confidence': 'HIGH',
                     'reason': f"Extracted from parentheses, found in Airtable: {canonical}"}
            else:
                d = {'decision': f"add to airtable as {extracted}", 'confidence': 'MEDIUM',
                     'reason': f"Person extracted from parentheses: {extracted}"}
        else:
            d = {'decision': 'add to airtable', 'confidence': 'MEDIUM', 'reason': 'Check evidence'}
    else:
        d = {'decision': 'add to airtable', 'confidence': 'MEDIUM', 'reason': 'Not in Airtable - new participant'}
    
    # Get ALL evidence
    cur.execute("SELECT DISTINCT source_call_url FROM participants WHERE name = ? LIMIT 5", (name,))
    fathom_urls = [row[0] for row in cur.fetchall()]
    d['fathom'] = ' '.join([f'<a href="{url}" target="_blank" class="evidence-link">🎥</a>' for url in fathom_urls]) if fathom_urls else "❌ No recordings"
    d['gmail'] = f'<a href="https://mail.google.com/mail/u/0/#search/{name.replace(" ", "%20")}" target="_blank" class="evidence-link">📧 Gmail</a>'
    d['townhall'] = '📅 <a href="https://docs.google.com/document/d/1oPYGLKfQ0PFWJHpME0hKhRHYXZbh73kFXnq2kRF8UiU/edit" target="_blank" class="evidence-link">Town Hall Agendas</a>'
    
    decisions[name] = d

conn.close()

# Sort by confidence
sorted_names = sorted(names, key=lambda n: {'HIGH': 0, 'MEDIUM': 1}[decisions[n]['confidence']])

# Generate HTML
output_file = Path('/Users/admin/ERA_Admin/integration_scripts') / f'BATCH3_RECOMMENDATIONS_{datetime.now().strftime("%Y%m%d_%H%M")}.html'

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Batch 3 - Complete Evidence</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 100%; margin: 0; padding: 15px; background: #f5f5f5; font-size: 13px; }}
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
        .evidence-link {{ color: #3498db; text-decoration: none; margin-right: 8px; }}
        .evidence-link:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 Batch 3 - Claude's Recommendations</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p><strong>✓ Complete Evidence:</strong> Fathom recordings, Gmail queries, Town Hall links included for all participants</p>
    </div>
    
    <div class="stats">
        <div class="stat-box"><div class="stat-value">{len(names)}</div><div class="stat-label">Total Cases</div></div>
        <div class="stat-box" style="background: #d4edda;"><div class="stat-value" style="color: #28a745;">{sum(1 for d in decisions.values() if d['confidence'] == 'HIGH')}</div><div class="stat-label">✅ High Confidence</div></div>
        <div class="stat-box" style="background: #fff3cd;"><div class="stat-value" style="color: #ffc107;">{sum(1 for d in decisions.values() if d['confidence'] == 'MEDIUM')}</div><div class="stat-label">🤔 Medium Confidence</div></div>
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
                <th>Reasoning</th>
                <th>Evidence (Fathom, Gmail, Town Hall)</th>
                <th style="width: 250px;">Your Feedback</th>
            </tr>
        </thead>
        <tbody>
'''

for name in sorted_names:
    d = decisions[name]
    checked = 'checked' if d['confidence'] == 'HIGH' else ''
    
    html += f'''
            <tr>
                <td style="text-align: center;">
                    <div style="background: #f8f9fa; padding: 8px; border-radius: 4px; margin-bottom: 8px;"><strong>{d["decision"]}</strong></div>
                    <label style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                        <input type="checkbox" class="approve-checkbox" {checked}>
                        <span style="font-weight: bold;">Approve</span>
                    </label>
                </td>
                <td><strong>{name}</strong></td>
                <td><span class="confidence-{d["confidence"]}">{d["confidence"]}</span></td>
                <td>{d["reason"]}</td>
                <td style="font-size: 11px;">{d["fathom"]}<br>{d["gmail"]}<br>{d["townhall"]}</td>
                <td><textarea class="feedback-text" placeholder="Your feedback..."></textarea></td>
            </tr>
'''

html += '''
        </tbody>
    </table>
    <script>
        function exportToCSV() {
            const table = document.getElementById('recommendationsTable');
            const rows = table.querySelectorAll('tbody tr');
            let csv = ['Name,Claude_Decision,Confidence,Reasoning,Approve,Your_Feedback,ProcessThis'];
            
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
            const filename = 'batch3_feedback_' + new Date().toISOString().slice(0,10) + '.csv';
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
        
        function checkAll() { document.querySelectorAll('.approve-checkbox').forEach(cb => cb.checked = true); }
        function uncheckAll() { document.querySelectorAll('.approve-checkbox').forEach(cb => cb.checked = false); }
    </script>
</body>
</html>
'''

with open(output_file, 'w') as f:
    f.write(html)

print(f"\n✅ Generated: {output_file}")
print(f"   Total: {len(names)} participants")
print(f"   HIGH: {sum(1 for d in decisions.values() if d['confidence'] == 'HIGH')}")
print(f"   MEDIUM: {sum(1 for d in decisions.values() if d['confidence'] == 'MEDIUM')}")
print(f"\n✅ ALL evidence included: Fathom + Gmail + Town Hall")
