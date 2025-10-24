#!/usr/bin/env python3
"""
Batch 3 REMAINING items - With Claude's Intelligence Applied
Based on PAST_LEARNINGS patterns I internalized
"""
import csv, sqlite3
from pathlib import Path
from datetime import datetime

conn = sqlite3.connect('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')
cur = conn.cursor()

# Load Airtable
airtable_lookup = {}
with open('/Users/admin/ERA_Admin/airtable/people_export.csv', 'r') as f:
    for row in csv.DictReader(f):
        name = row.get('Name', '').strip()
        if name: airtable_lookup[name.lower()] = name

# Get remaining items from batch3 CSV
with open('/Users/admin/Downloads/batch3_2025-10-23.csv', 'r') as f:
    remaining_names = [r['Name'] for r in csv.DictReader(f) if r['ProcessThis'] != 'YES']

print(f"📋 Processing {len(remaining_names)} remaining Batch 3 items")
print("🧠 Applying Claude's intelligence from PAST_LEARNINGS\n")

decisions = {}
for name in remaining_names:
    d = {'confidence': 'MEDIUM', 'decision': '', 'reason': ''}
    
    # CLAUDE'S INTELLIGENCE (from internalized patterns)
    
    # Pattern 1: Number variants (3), (2), etc.
    if '(' in name and ')' in name and any(c.isdigit() for c in name.split('(')[1].split(')')[0]):
        base = name.split('(')[0].strip()
        if base.lower() in airtable_lookup:
            d['decision'] = f"merge with: {airtable_lookup[base.lower()]}"
            d['reason'] = f'Number variant of {airtable_lookup[base.lower()]}'
            d['confidence'] = 'HIGH'
        else:
            d['decision'] = f'merge with: {base}'
            d['reason'] = f'Number variant (base: {base})'
            d['confidence'] = 'MEDIUM'
    
    # Pattern 2: Person in parentheses (full name)
    elif '(' in name and ')' in name:
        person = name.split('(')[1].rstrip(')')
        if len(person.split()) >= 2:  # Full name like "Indy Boyle-Rhymes"
            d['decision'] = f'add to airtable as {person}'
            d['reason'] = 'Person extracted from parentheses'
            d['confidence'] = 'HIGH'
        else:
            d['decision'] = 'investigate'
            d['reason'] = 'Parentheses but not clear person name'
            d['confidence'] = 'MEDIUM'
    
    # Pattern 3: Person - Context
    elif ' - ' in name and not name.startswith('e-'):
        person = name.split(' - ')[0].strip()
        if person.lower() in airtable_lookup:
            d['decision'] = f"merge with: {airtable_lookup[person.lower()]}"
            d['reason'] = 'Person - Context pattern, found in Airtable'
            d['confidence'] = 'HIGH'
        elif len(person.split()) >= 2:
            d['decision'] = f'add to airtable as {person}'
            d['reason'] = 'Person - Context pattern'
            d['confidence'] = 'MEDIUM'
        else:
            d['decision'] = 'investigate'
            d['reason'] = 'Single name with context - need more info'
            d['confidence'] = 'MEDIUM'
    
    # Pattern 4: Known organizations
    elif any(org in name for org in ['EcoAgriculture Partners', 'e-NABLE Events']):
        d['decision'] = 'drop'
        d['reason'] = 'Organization, not person'
        d['confidence'] = 'HIGH'
    
    # Pattern 5: Dr/Dr. variants - Brian von Herzen
    elif 'von Herzen' in name:
        if 'brian von herzen' in airtable_lookup:
            d['decision'] = f"merge with: {airtable_lookup['brian von herzen']}"
            d['reason'] = 'Dr./Dr variant, found in Airtable'
            d['confidence'] = 'HIGH'
        else:
            d['decision'] = 'merge with: Brian Von Herzen'
            d['reason'] = 'Dr./Dr variant (assuming exists)'
            d['confidence'] = 'MEDIUM'
    
    # Pattern 6: Climbien pattern (from past learnings)
    elif 'Climbien' in name:
        d['decision'] = 'merge with: Climbien Babungire'
        d['reason'] = 'Climbien → Climbien Babungire (from past learnings)'
        d['confidence'] = 'HIGH'
    
    # Pattern 7: Single names - need investigation
    elif len(name.split()) == 1:
        d['decision'] = 'investigate'
        d['reason'] = 'Single name - check Fathom recordings for full name'
        d['confidence'] = 'MEDIUM'
    
    # Default: check Airtable
    else:
        if name.lower() in airtable_lookup:
            d['decision'] = f"merge with: {airtable_lookup[name.lower()]}"
            d['reason'] = 'Found in Airtable'
            d['confidence'] = 'HIGH'
        else:
            d['decision'] = 'add to airtable'
            d['reason'] = 'Not in Airtable - likely new participant'
            d['confidence'] = 'MEDIUM'
    
    # Get evidence
    cur.execute("SELECT DISTINCT source_call_url FROM participants WHERE name = ? LIMIT 5", (name,))
    fathom_urls = [row[0] for row in cur.fetchall()]
    d['fathom'] = ' '.join([f'<a href="{url}" target="_blank" class="evidence-link">🎥</a>' 
                            for url in fathom_urls]) if fathom_urls else "❌"
    
    d['gmail'] = f'<a href="https://mail.google.com/mail/u/0/#search/{name.replace(" ", "%20")}" target="_blank" class="evidence-link">📧</a>'
    
    # Town Hall
    cur.execute('''
        SELECT DISTINCT t.agenda_id, t.meeting_date
        FROM participants p
        JOIN calls c ON p.source_call_url = c.hyperlink
        JOIN town_hall_agendas t ON c.date = t.meeting_date
        WHERE p.name = ?
        LIMIT 3
    ''', (name,))
    agendas = cur.fetchall()
    if agendas:
        th_links = [f'<a href="https://docs.google.com/document/d/{aid}/edit" target="_blank" class="evidence-link">📅 {date}</a>' 
                   for aid, date in agendas]
        d['townhall'] = '<br>'.join(th_links)
    else:
        d['townhall'] = "❌"
    
    decisions[name] = d

conn.close()

# Generate HTML
sorted_names = sorted(remaining_names, key=lambda n: {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}[decisions[n]['confidence']])
output = Path('/Users/admin/ERA_Admin/integration_scripts/BATCH3_REMAINING_{}.html'.format(datetime.now().strftime("%Y%m%d_%H%M")))

html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Batch 3 Remaining - Claude's Intelligence</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont;max-width:100%;margin:0;padding:15px;background:#f5f5f5;font-size:13px}}
h1{{color:#2c3e50}}
table{{width:100%;border-collapse:collapse;background:white}}
th{{background:#34495e;color:white;padding:12px}}
td{{padding:10px;border-bottom:1px solid #ecf0f1}}
.confidence-HIGH{{background:#d4edda;color:#155724;padding:4px 8px;border-radius:4px}}
.confidence-MEDIUM{{background:#fff3cd;color:#856404;padding:4px 8px;border-radius:4px}}
.evidence-link{{color:#3498db;margin-right:8px}}
input[type="checkbox"]{{width:20px;height:20px}}
textarea{{width:100%;padding:6px;border:1px solid #ddd;min-height:50px}}
button{{background:#3498db;color:white;border:none;padding:10px 20px;margin:10px 10px 10px 0;cursor:pointer}}
</style></head><body>
<h1>🧠 Batch 3 Remaining - Claude's Intelligence Applied</h1>
<p><strong>{len(remaining_names)} items</strong> analyzed using patterns from PAST_LEARNINGS.md</p>
<p>HIGH: {sum(1 for d in decisions.values() if d['confidence']=='HIGH')} | 
   MEDIUM: {sum(1 for d in decisions.values() if d['confidence']=='MEDIUM')}</p>
<button onclick="exportToCSV()">📥 Export CSV</button>
<table><thead><tr><th style="width:200px">Recommendation</th><th>Name</th><th>Conf</th><th>Reasoning</th><th>Evidence</th><th style="width:200px">Feedback</th></tr></thead><tbody>'''

for name in sorted_names:
    d = decisions[name]
    checked = 'checked' if d['confidence'] == 'HIGH' else ''
    html += f'''<tr><td><div style="background:#f8f9fa;padding:8px;margin-bottom:8px"><strong>{d["decision"]}</strong></div>
<label><input type="checkbox" class="approve-checkbox" {checked}> Approve</label></td>
<td><strong>{name}</strong></td><td><span class="confidence-{d["confidence"]}">{d["confidence"]}</span></td>
<td>{d["reason"]}</td><td style="font-size:11px">{d["fathom"]}<br>{d["gmail"]}<br>{d["townhall"]}</td>
<td><textarea class="feedback-text"></textarea></td></tr>'''

html += '''</tbody></table><script>
function exportToCSV(){const rows=document.querySelectorAll('tbody tr');let csv=['Name,Decision,Confidence,Reason,Approve,Feedback,ProcessThis'];
rows.forEach(row=>{const cells=row.querySelectorAll('td');const cb=cells[0].querySelector('input');
const dec=cells[0].querySelector('div').textContent.trim();const name=cells[1].textContent.trim();
const conf=cells[2].textContent.trim();const reason=cells[3].textContent.trim().replace(/"/g,'""');
const app=cb.checked?'YES':'NO';const fb=cells[5].querySelector('textarea').value.replace(/"/g,'""');
csv.push(`"${name}","${dec}","${conf}","${reason}","${app}","${fb}","${app}"`);});
const blob=new Blob([csv.join('\\n')],{type:'text/csv'});const url=window.URL.createObjectURL(blob);
const a=document.createElement('a');a.href=url;a.download='batch3_remaining_'+new Date().toISOString().slice(0,10)+'.csv';
a.click();window.URL.revokeObjectURL(url);
navigator.clipboard.writeText('/Users/admin/Downloads/'+a.download).then(()=>{alert('✅ Exported!\\n📋 Path copied');});}
</script></body></html>'''

with open(output, 'w') as f: f.write(html)

print(f"\n✅ Generated: {output}")
print(f"\n🧠 Claude's intelligence applied:")
print(f"  - Number variants recognized")
print(f"  - Person from parentheses extracted")
print(f"  - Person - Context patterns identified")
print(f"  - Organizations filtered")
print(f"  - Past learnings (Climbien) applied")
