#!/usr/bin/env python3
"""
Batch 3 - With PROPER Town Hall Links
Following the right data flow:
  Participant → Fathom Call → Call Date → Town Hall Agenda Doc
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

# Past learnings
PAST = {
    'variants': {'Aditi': 'Aditi Singh', 'Ana': 'Ana Calderon', 'Ana C': 'Ana Calderon',
                 'Angelique': 'Angelique Garcia', 'andreaseke': 'Andreas Eke',
                 'Aimee Samara (Krouskop)': 'Aimee Samara', 'Billimarie': 'Billimarie Lubiano Robinson',
                 'Brendan McNamara (ORQAS)': 'Brendan McNamara'}
}

# Get unprocessed participants
cur.execute("SELECT DISTINCT name FROM participants WHERE validated_by_airtable = 0 ORDER BY name LIMIT 50")
names = [row[0] for row in cur.fetchall()]

print(f"📋 Processing {len(names)} participants with proper Town Hall links...")

decisions = {}
for name in names:
    # Apply judgment (same as before)
    if name in PAST['variants']:
        d = {'decision': f"merge with: {PAST['variants'][name]}", 'confidence': 'HIGH',
             'reason': f"From past learnings → {PAST['variants'][name]}"}
    elif name.lower() in airtable_lookup:
        d = {'decision': f"merge with: {airtable_lookup[name.lower()]}", 'confidence': 'HIGH',
             'reason': 'Found in Airtable'}
    elif name in ['admin', 'bk']:
        d = {'decision': 'drop', 'confidence': 'HIGH', 'reason': 'System account'}
    else:
        d = {'decision': 'add to airtable', 'confidence': 'MEDIUM', 'reason': 'Not in Airtable'}
    
    # Get PROPER evidence
    # 1. Fathom recordings
    cur.execute("SELECT DISTINCT source_call_url FROM participants WHERE name = ? LIMIT 5", (name,))
    fathom_urls = [row[0] for row in cur.fetchall()]
    d['fathom'] = ' '.join([f'<a href="{url}" target="_blank" class="evidence-link">🎥</a>' 
                            for url in fathom_urls]) if fathom_urls else "❌"
    
    # 2. Gmail query
    d['gmail'] = f'<a href="https://mail.google.com/mail/u/0/#search/{name.replace(" ", "%20")}" target="_blank" class="evidence-link">📧</a>'
    
    # 3. PROPER Town Hall links - join through calls to get agenda
    cur.execute('''
        SELECT DISTINCT t.agenda_id, t.meeting_date, t.meeting_title
        FROM participants p
        JOIN calls c ON p.source_call_url = c.hyperlink
        JOIN town_hall_agendas t ON c.date = t.meeting_date
        WHERE p.name = ?
        ORDER BY t.meeting_date DESC
        LIMIT 3
    ''', (name,))
    
    agendas = cur.fetchall()
    if agendas:
        agenda_links = []
        for agenda_id, date, title in agendas:
            doc_url = f"https://docs.google.com/document/d/{agenda_id}/edit"
            agenda_links.append(f'<a href="{doc_url}" target="_blank" class="evidence-link">📅 {date}</a>')
        d['townhall'] = '<br>'.join(agenda_links)
    else:
        d['townhall'] = "❌ No TH"
    
    decisions[name] = d

conn.close()

# Generate HTML
sorted_names = sorted(names, key=lambda n: {'HIGH': 0, 'MEDIUM': 1}[decisions[n]['confidence']])
output = Path('/Users/admin/ERA_Admin/integration_scripts/BATCH3_PROPER_{}.html'.format(datetime.now().strftime("%Y%m%d_%H%M")))

html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Batch 3 - Proper Links</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;max-width:100%;margin:0;padding:15px;background:#f5f5f5;font-size:13px}}
h1{{color:#2c3e50;border-bottom:3px solid #3498db;padding-bottom:10px}}
.header{{background:white;padding:20px;border-radius:8px;margin-bottom:20px;box-shadow:0 2px 4px rgba(0,0,0,0.1)}}
table{{width:100%;border-collapse:collapse;background:white;box-shadow:0 2px 4px rgba(0,0,0,0.1)}}
th{{background:#34495e;color:white;padding:12px;text-align:left;position:sticky;top:0}}
td{{padding:10px;border-bottom:1px solid #ecf0f1}}
tr:hover{{background:#f8f9fa}}
input[type="checkbox"]{{width:20px;height:20px;cursor:pointer}}
textarea{{width:100%;padding:6px;border:1px solid #ddd;border-radius:4px;font-family:inherit;resize:vertical;min-height:50px}}
.confidence-HIGH{{background:#d4edda;color:#155724;padding:4px 8px;border-radius:4px;font-weight:bold}}
.confidence-MEDIUM{{background:#fff3cd;color:#856404;padding:4px 8px;border-radius:4px;font-weight:bold}}
.evidence-link{{color:#3498db;text-decoration:none;margin-right:8px}}
button{{background:#3498db;color:white;border:none;padding:10px 20px;border-radius:4px;cursor:pointer;margin:10px 10px 10px 0}}
</style></head><body>
<div class="header"><h1>🤖 Batch 3 - Proper Town Hall Links</h1>
<p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
<p><strong>Evidence:</strong> Participant → Fathom Call → Meeting Date → Specific Town Hall Agenda Doc</p></div>
<button onclick="exportToCSV()">📥 Export CSV (copies path)</button>
<table><thead><tr><th style="width:250px">Recommendation</th><th>Name</th><th>Conf</th><th>Reasoning</th>
<th>Evidence (Fathom | Gmail | Town Hall Agendas)</th><th style="width:250px">Feedback</th></tr></thead><tbody>'''

for name in sorted_names:
    d = decisions[name]
    checked = 'checked' if d['confidence'] == 'HIGH' else ''
    html += f'''<tr><td style="text-align:center"><div style="background:#f8f9fa;padding:8px;border-radius:4px;margin-bottom:8px"><strong>{d["decision"]}</strong></div>
<label style="display:flex;align-items:center;justify-content:center;gap:8px"><input type="checkbox" class="approve-checkbox" {checked}><span style="font-weight:bold">Approve</span></label></td>
<td><strong>{name}</strong></td><td><span class="confidence-{d["confidence"]}">{d["confidence"]}</span></td><td>{d["reason"]}</td>
<td style="font-size:11px">{d["fathom"]}<br>{d["gmail"]}<br>{d["townhall"]}</td>
<td><textarea class="feedback-text" placeholder="Feedback..."></textarea></td></tr>'''

html += '''</tbody></table><script>
function exportToCSV(){const table=document.querySelector('table');const rows=table.querySelectorAll('tbody tr');
let csv=['Name,Decision,Confidence,Reasoning,Approve,Feedback,ProcessThis'];
rows.forEach(row=>{const cells=row.querySelectorAll('td');const checkbox=cells[0].querySelector('input[type="checkbox"]');
const decision=cells[0].querySelector('div').textContent.trim();const name=cells[1].textContent.trim();
const confidence=cells[2].textContent.trim();const reasoning=cells[3].textContent.trim().replace(/"/g,'""');
const approve=checkbox.checked?'YES':'NO';const feedback=cells[5].querySelector('textarea').value.replace(/"/g,'""');
csv.push(`"${name}","${decision}","${confidence}","${reasoning}","${approve}","${feedback}","${approve}"`);});
const csvContent=csv.join('\\n');const blob=new Blob([csvContent],{type:'text/csv'});const url=window.URL.createObjectURL(blob);
const a=document.createElement('a');a.href=url;const filename='batch3_'+new Date().toISOString().slice(0,10)+'.csv';
a.download=filename;a.click();window.URL.revokeObjectURL(url);
const fullPath='/Users/admin/Downloads/'+filename;navigator.clipboard.writeText(fullPath).then(()=>{
alert('✅ CSV exported!\\n📋 Path: '+fullPath);}).catch(()=>{alert('✅ Exported: '+filename);});}
</script></body></html>'''

with open(output, 'w') as f: f.write(html)

print(f"\n✅ Generated: {output}")
print(f"   HIGH: {sum(1 for d in decisions.values() if d['confidence']=='HIGH')}")
print(f"   MEDIUM: {sum(1 for d in decisions.values() if d['confidence']=='MEDIUM')}")
print("\n✅ Town Hall links now go to SPECIFIC agenda docs for that meeting date!")
print("✅ Data flow: Participant → Fathom Call → Date → Agenda Doc")
