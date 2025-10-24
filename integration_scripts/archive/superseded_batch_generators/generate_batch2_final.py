#!/usr/bin/env python3
"""
Generate Batch 2 HTML with:
1. Past learnings applied
2. Fixed export button (copies path to clipboard)
"""

import json
from datetime import datetime
from pathlib import Path

# Load past learnings
PAST_LEARNINGS = {
    'phones': {
        '16319034965': 'Sean Pettersen',
        '18022588598': 'Michael Mayer',
    },
    'organizations': {
        'BioIntegrity': 'Chris Searles',
        'Agri-Tech Producers LLC, Joe James': 'Joe James',
        'Cosmic Labyrinth': 'Indy Singh',
        'Beck Bio4Climate': 'Beck Mordini',
        'Flip Town': 'Muhange Musinga',
    },
    'variants': {
        'Belizey': 'Kalombo Mbilizi',
        'Brendah': 'Mbilizi Kalombo',
        'CBiradar': 'Chandrashekhar Biradar',
        'Climbien': 'Climbien Babungire',
        'charlotte': 'Charlotte Anthony',
        'Aditi': 'Aditi Singh',
        'Ana': 'Ana Calderon',
        'Angelique': 'Angelique Garcia',
        'Betty Bitengo': 'Betty Atandi',
        'Benamara Elhabib': 'Elhabib Benamara',
    }
}

# Batch 2 names
batch2_names = [
    '16319034965', '18022588598', 'Abigail Castle', 'Aditi', 'admin', 'afmiller09',
    'Agri-Tech Producers LLC, Joe James', 'Aimee Samara (Krouskop)', 'Allison Wu',
    'Alnoor IP 14P', 'Ana', 'ana - Panama Restoration Lab', 'Ana C',
    'Ananda Fitzsimmons (4)', 'Andrea Manrique', 'andreaseke', "Andres's iPhone (2)",
    'Angelique', 'aniqa', 'aniqa Locations: Bangladesh, Egypt, Sikkim',
    'Anna Calderon', 'Ansiima Casinga Rolande', 'BasHam (Ecoist)', 'Beck Bio4Climate',
    'Benamara Elhabib', 'Betty Bitengo', 'Billimarie', 'Billimarie (3)',
    'Bio4Climate1 (Beck Mordini)', 'BioIntegrity', 'bk', 'Brendah',
    'Brendan McNamara (ORQAS)', 'Brian', 'Bru Pearce (4)', 'C. Petruzzi-McHale',
    'CBiradar', 'Charles', 'Charlie Shore', 'Charlie Shore, Gaithersburg, MD',
    'charlotte', 'Chris Pilley', 'CHRISTOPHER - Tanzania', 'Christopher Danch',
    'Climbien', 'Climbien (3)', 'Coakee Wildcat', 'Cole',
    'Cosmic Labyrinth (Indy Boyle-Rhymes)', 'Cosmic Labyrinth (Indy)'
]

decisions = {}

for name in batch2_names:
    d = {'name': name, 'confidence': 'MEDIUM', 'decision': '', 'reason': ''}
    
    # Check past learnings FIRST
    if name in PAST_LEARNINGS['phones']:
        d['decision'] = f"merge with: {PAST_LEARNINGS['phones'][name]}"
        d['reason'] = f"Phone number identified in past round → {PAST_LEARNINGS['phones'][name]}"
        d['confidence'] = 'HIGH'
    
    elif name in PAST_LEARNINGS['organizations']:
        d['decision'] = f"merge with: {PAST_LEARNINGS['organizations'][name]}"
        d['reason'] = f"Organization identified in past round → {PAST_LEARNINGS['organizations'][name]}"
        d['confidence'] = 'HIGH'
    
    elif name in PAST_LEARNINGS['variants']:
        d['decision'] = f"merge with: {PAST_LEARNINGS['variants'][name]}"
        d['reason'] = f"Name variant identified in past round → {PAST_LEARNINGS['variants'][name]}"
        d['confidence'] = 'HIGH'
    
    # Drop patterns
    elif name in ['admin', 'bk', 'afmiller09', 'andreaseke']:
        d['decision'] = 'drop'
        d['reason'] = 'System account or username'
        d['confidence'] = 'HIGH'
    
    elif "iPhone" in name:
        d['decision'] = 'drop'
        d['reason'] = 'Device name'
        d['confidence'] = 'HIGH'
    
    # Number variants
    elif '(' in name and ')' in name and any(c.isdigit() for c in name):
        base_name = name.split('(')[0].strip()
        d['decision'] = f'merge with: {base_name}'
        d['reason'] = f'Number variant of {base_name}'
        d['confidence'] = 'HIGH'
    
    # Organization + person patterns
    elif ', ' in name:
        # Extract person after comma
        person = name.split(', ')[-1]
        d['decision'] = f'add to airtable as {person}'
        d['reason'] = f'Organization + person pattern: "{name}"'
        d['confidence'] = 'HIGH'
    
    elif ' - ' in name and not name.startswith('ana'):
        # Extract person before dash
        person = name.split(' - ')[0]
        if person and not person.isdigit():
            d['decision'] = f'add to airtable as {person}'
            d['reason'] = f'Person + context pattern'
            d['confidence'] = 'MEDIUM'
    
    # Default
    else:
        d['decision'] = 'add to airtable' if len(name.split()) > 1 else 'investigate'
        d['reason'] = 'Needs Town Hall/Gmail context' if d['decision'] == 'investigate' else 'Check if already in Airtable'
        d['confidence'] = 'MEDIUM'
    
    decisions[name] = d

# Sort by confidence
sorted_names = sorted(decisions.keys(), key=lambda n: {
    'HIGH': 0, 'MEDIUM': 1, 'LOW': 2
}.get(decisions[n]['confidence'], 3))

output_file = Path('/Users/admin/ERA_Admin/integration_scripts') / f'BATCH2_RECOMMENDATIONS_{datetime.now().strftime("%Y%m%d_%H%M")}.html'

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Batch 2 - AI Recommendations (with Past Learnings)</title>
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
        .confidence-LOW {{ background: #f8d7da; color: #721c24; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
        .evidence-link {{ color: #3498db; text-decoration: none; }}
        .evidence-link:hover {{ text-decoration: underline; }}
        .past-learning {{ background: #e3f2fd; padding: 4px 8px; border-radius: 4px; font-size: 11px; margin-left: 8px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 Batch 2 - AI Recommendations (Past Learnings Applied)</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p><strong>Improvements:</strong> ✓ Past phone numbers ✓ Past organizations ✓ Past name variants ✓ Export copies path</p>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-value">50</div>
            <div class="stat-label">Total Cases</div>
        </div>
        <div class="stat-box" style="background: #d4edda;">
            <div class="stat-value" style="color: #28a745;">{sum(1 for d in decisions.values() if d['confidence'] == 'HIGH')}</div>
            <div class="stat-label">✅ High Confidence</div>
        </div>
        <div class="stat-box" style="background: #fff3cd;">
            <div class="stat-value" style="color: #ffc107;">{sum(1 for d in decisions.values() if d['confidence'] == 'MEDIUM')}</div>
            <div class="stat-label">🤔 Medium Confidence</div>
        </div>
        <div class="stat-box" style="background: #e3f2fd;">
            <div class="stat-value" style="color: #1976d2;">{sum(1 for d in decisions.values() if 'past round' in d['reason'].lower())}</div>
            <div class="stat-label">📚 Past Learnings Applied</div>
        </div>
    </div>
    
    <div class="controls">
        <button onclick="exportToCSV()">📥 Export to CSV (copies path)</button>
        <button onclick="checkAll()">✓ Check All</button>
        <button onclick="uncheckAll()">✗ Uncheck All</button>
        <button onclick="filterByConfidence('all')">Show All</button>
        <button onclick="filterByConfidence('HIGH')">High Only</button>
    </div>
    
    <table id="recommendationsTable">
        <thead>
            <tr>
                <th style="width: 250px;">Claude's Recommendation</th>
                <th>Name</th>
                <th>Confidence</th>
                <th>Claude's Reasoning</th>
                <th>Evidence</th>
                <th style="width: 250px;">Your Feedback/Guidance</th>
            </tr>
        </thead>
        <tbody>
'''

for name in sorted_names:
    d = decisions[name]
    confidence = d['confidence']
    checked = 'checked' if confidence == 'HIGH' else ''
    
    past_learning_badge = '<span class="past-learning">📚 Past Learning</span>' if 'past round' in d['reason'].lower() else ''
    
    recommendation_html = f'<div style="background: #f8f9fa; padding: 8px; border-radius: 4px; margin-bottom: 8px;"><strong>{d["decision"]}</strong>{past_learning_badge}</div>'
    
    gmail_link = f"https://mail.google.com/mail/u/0/#search/{name.replace(' ', '%20')}"
    
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
                <td style="font-size: 11px;">
                    <a href="{gmail_link}" target="_blank" class="evidence-link">📧 Email Query</a>
                </td>
                <td><textarea class="feedback-text" placeholder="Your feedback/corrections..."></textarea></td>
            </tr>
'''

html += f'''
        </tbody>
    </table>
    
    <script>
        function exportToCSV() {{
            const table = document.getElementById('recommendationsTable');
            const rows = table.querySelectorAll('tbody tr');
            let csv = [];
            
            csv.push('Name,Claude_Decision,Confidence,Claude_Reasoning,Approve,Your_Feedback,ProcessThis');
            
            rows.forEach(row => {{
                const cells = row.querySelectorAll('td');
                const checkbox = cells[0].querySelector('input[type="checkbox"]');
                const decision = cells[0].querySelector('div').textContent.trim().replace('📚 Past Learning', '').trim();
                const name = cells[1].textContent.trim();
                const confidence = cells[2].textContent.trim();
                const reasoning = cells[3].textContent.trim().replace(/"/g, '""');
                const approve = checkbox.checked ? 'YES' : 'NO';
                const feedback = cells[5].querySelector('textarea').value.replace(/"/g, '""');
                const processThis = approve === 'YES' ? 'YES' : 'REVIEW';
                
                csv.push(`"${{name}}","${{decision}}","${{confidence}}","${{reasoning}}","${{approve}}","${{feedback}}","${{processThis}}"`);
            }});
            
            const csvContent = csv.join('\\n');
            const blob = new Blob([csvContent], {{ type: 'text/csv' }});
            const url = window.URL.createObjectURL(blob);
            
            // Download file
            const a = document.createElement('a');
            a.href = url;
            const filename = 'batch2_feedback_' + new Date().toISOString().slice(0,10) + '.csv';
            a.download = filename;
            a.click();
            window.URL.revokeObjectURL(url);
            
            // Copy path to clipboard
            const fullPath = '/Users/admin/Downloads/' + filename;
            navigator.clipboard.writeText(fullPath).then(() => {{
                alert('✅ CSV exported!\\n📋 Path copied to clipboard:\\n' + fullPath);
            }}).catch(() => {{
                alert('✅ CSV exported as: ' + filename + '\\n⚠️  Could not copy path to clipboard');
            }});
        }}
        
        function checkAll() {{
            document.querySelectorAll('.approve-checkbox').forEach(cb => cb.checked = true);
        }}
        
        function uncheckAll() {{
            document.querySelectorAll('.approve-checkbox').forEach(cb => cb.checked = false);
        }}
        
        function filterByConfidence(level) {{
            const rows = document.querySelectorAll('#recommendationsTable tbody tr');
            rows.forEach(row => {{
                if (level === 'all') {{
                    row.style.display = '';
                }} else {{
                    const confidenceSpan = row.querySelector('[class^="confidence-"]');
                    if (confidenceSpan && confidenceSpan.textContent === level) {{
                        row.style.display = '';
                    }} else {{
                        row.style.display = 'none';
                    }}
                }}
            }});
        }}
    </script>
</body>
</html>
'''

with open(output_file, 'w') as f:
    f.write(html)

print(f"✅ Generated: {output_file}")
print(f"\n📊 Summary:")
print(f"  HIGH: {sum(1 for d in decisions.values() if d['confidence'] == 'HIGH')}")
print(f"  MEDIUM: {sum(1 for d in decisions.values() if d['confidence'] == 'MEDIUM')}")
print(f"  Past learnings applied: {sum(1 for d in decisions.values() if 'past round' in d['reason'].lower())}")
print(f"\n✅ Export button now copies path to clipboard!")

PYTHON_EOF
