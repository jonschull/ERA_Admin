#!/usr/bin/env python3
"""
FINAL BATCH GENERATOR with Fuzzy Review
Includes ALL remaining + uses past decisions intelligently
"""
import csv, sqlite3, glob, json
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher
from fuzzy_match_past_decisions import search_past_decisions

# Connect
conn = sqlite3.connect('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')
cur = conn.cursor()

# Load Airtable
airtable_lookup = {}
with open('/Users/admin/ERA_Admin/airtable/people_export.csv', 'r') as f:
    for row in csv.DictReader(f):
        name = row.get('Name', '').strip()
        if name: airtable_lookup[name.lower()] = name

# Get next 50
cur.execute("SELECT DISTINCT name FROM participants WHERE validated_by_airtable = 0 ORDER BY name LIMIT 50")
names = [row[0] for row in cur.fetchall()]

print(f"🧠 Generating Batch 4 with FUZZY REVIEW")
print(f"📋 {len(names)} participants")
print(f"✅ {len(airtable_lookup)} in Airtable\n")

decisions = {}
stats = {'high': 0, 'medium': 0, 'from_past': 0}

for name in names:
    d = {'confidence': 'MEDIUM', 'decision': '', 'reason': ''}
    
    # FUZZY MATCH past decisions
    past = search_past_decisions(name, threshold=0.75)
    
    if past and past[0]['similarity'] == 1.0 and past[0]['processed'] == 'YES':
        # Exact match - use past decision
        dec = past[0]['decision']
        
        if 'merge with:' in dec.lower():
            target = dec.split('merge with:')[-1].strip()
            d['decision'] = f'merge with: {target}'
            d['reason'] = 'From past decisions (exact match)'
            d['confidence'] = 'HIGH'
            stats['high'] += 1
            stats['from_past'] += 1
        elif 'add' in dec.lower():
            d['decision'] = dec
            d['reason'] = 'From past decisions (exact match)'
            d['confidence'] = 'HIGH'
            stats['high'] += 1
            stats['from_past'] += 1
        elif 'drop' in dec.lower():
            d['decision'] = 'drop'
            d['reason'] = 'From past decisions (exact match)'
            d['confidence'] = 'HIGH'
            stats['high'] += 1
            stats['from_past'] += 1
    
    # No past match - check Airtable
    if not d['decision'] and name.lower() in airtable_lookup:
        d['decision'] = f"merge with: {airtable_lookup[name.lower()]}"
        d['reason'] = 'Found in Airtable'
        d['confidence'] = 'HIGH'
        stats['high'] += 1
    
    # Still nothing - needs investigation
    if not d['decision']:
        d['decision'] = 'needs investigation'
        d['reason'] = 'No past decision, not in Airtable - check evidence'
        stats['medium'] += 1
    
    # Evidence
    cur.execute("SELECT DISTINCT source_call_url FROM participants WHERE name = ? LIMIT 5", (name,))
    fathom = [r[0] for r in cur.fetchall()]
    d['fathom'] = ' '.join([f'<a href="{u}" target="_blank" class="evidence-link">🎥</a>' for u in fathom]) if fathom else "❌"
    d['gmail'] = f'<a href="https://mail.google.com/mail/u/0/#search/{name.replace(" ", "%20")}" target="_blank" class="evidence-link">📧</a>'
    
    cur.execute('''
        SELECT DISTINCT t.agenda_id, t.meeting_date
        FROM participants p
        JOIN calls c ON p.source_call_url = c.hyperlink
        JOIN town_hall_agendas t ON c.date = t.meeting_date
        WHERE p.name = ? LIMIT 3
    ''', (name,))
    th = cur.fetchall()
    d['townhall'] = '<br>'.join([f'<a href="https://docs.google.com/document/d/{a}/edit" target="_blank" class="evidence-link">📅 {d}</a>' 
                                 for a, d in th]) if th else "❌"
    
    decisions[name] = d

conn.close()

print(f"✅ Analysis complete:")
print(f"   HIGH: {stats['high']} ({stats['from_past']} from past decisions)")
print(f"   MEDIUM: {stats['medium']}")

# Generate HTML
sorted_names = sorted(names, key=lambda n: {'HIGH': 0, 'MEDIUM': 1}[decisions[n]['confidence']])
output = Path(f'/Users/admin/ERA_Admin/integration_scripts/BATCH4_FUZZY_REVIEW_{datetime.now().strftime("%Y%m%d_%H%M")}.html')

html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Batch 4 - Fuzzy Review</title>
<style>
body{{font-family:-apple-system;max-width:100%;margin:0;padding:15px;background:#f5f5f5;font-size:13px}}
h1{{color:#2c3e50}}
table{{width:100%;border-collapse:collapse;background:white}}
th{{background:#34495e;color:white;padding:12px;position:sticky;top:0}}
td{{padding:10px;border-bottom:1px solid #ecf0f1}}
tr:hover{{background:#f8f9fa}}
.confidence-HIGH{{background:#d4edda;color:#155724;padding:4px 8px;border-radius:4px}}
.confidence-MEDIUM{{background:#fff3cd;color:#856404;padding:4px 8px;border-radius:4px}}
.evidence-link{{color:#3498db;margin-right:8px}}
input{{width:20px;height:20px}}
textarea{{width:100%;padding:6px;border:1px solid #ddd;min-height:50px}}
button{{background:#3498db;color:white;border:none;padding:10px 20px;margin:10px 0;cursor:pointer}}
</style></head><body>
<h1>🧠 Batch 4 - With Fuzzy Review of Past Decisions</h1>
<p><strong>{len(names)} participants</strong> | HIGH: {stats['high']} ({stats['from_past']} from past) | MEDIUM: {stats['medium']}</p>
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
const a=document.createElement('a');a.href=url;a.download='batch4_'+new Date().toISOString().slice(0,10)+'.csv';
a.click();window.URL.revokeObjectURL(url);
navigator.clipboard.writeText('/Users/admin/Downloads/'+a.download).then(()=>{alert('✅ Exported!\\n📋 Path copied');});}
</script></body></html>'''

with open(output, 'w') as f:
    f.write(html)

print(f"\n✅ Generated: {output}")
print("✅ Fuzzy review applied - past decisions used intelligently!")
