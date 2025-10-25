#!/usr/bin/env python3
"""
🧠 CLAUDE REVIEW STEP - Part 2 of canonical pipeline
Loads intermediate results and prompts Claude for intelligent decisions
"""
import json, sqlite3
from pathlib import Path
from datetime import datetime

# Load intermediate results
intermediate = Path('/tmp/batch_intermediate.json')
if not intermediate.exists():
    print("❌ No intermediate results found!")
    print("   Run generate_batch_CANONICAL.py first")
    exit(1)

with open(intermediate) as f:
    data = json.load(f)

names = data['names']
decisions = data['decisions']
needs_review = data['needs_review']

print("="*80)
print("🧠 CLAUDE INTELLIGENT REVIEW")
print("="*80)
print(f"\n{len(needs_review)} items need your review")
print("\nFor each item, you'll:")
print("  • See the name and evidence links")
print("  • Apply PAST_LEARNINGS patterns")
print("  • Check Town Hall agendas")
print("  • Provide intelligent decision")
print()

# Connect to DB for evidence
conn = sqlite3.connect('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')
cur = conn.cursor()

# Load Airtable for reference
airtable_people = []
with open('/Users/admin/ERA_Admin/airtable/people_export.csv', 'r') as f:
    import csv
    airtable_people = [row.get('Name', '') for row in csv.DictReader(f)]

reviewed_decisions = {}

print("="*80)
print(f"REVIEWING {len(needs_review)} ITEMS")
print("="*80)

for i, name in enumerate(needs_review, 1):
    print(f"\n[{i}/{len(needs_review)}] {name}")
    print("-" * 60)
    
    # Show evidence
    cur.execute("SELECT DISTINCT source_call_url FROM participants WHERE name = ? LIMIT 3", (name,))
    fathom_urls = [row[0] for row in cur.fetchall()]
    if fathom_urls:
        print(f"🎥 Fathom: {fathom_urls[0]}")
    
    # Town Hall
    cur.execute('''
        SELECT DISTINCT t.meeting_date, t.meeting_title
        FROM participants p
        JOIN calls c ON p.source_call_url = c.hyperlink
        JOIN town_hall_agendas t ON c.date = t.meeting_date
        WHERE p.name = ?
        LIMIT 2
    ''', (name,))
    th = cur.fetchall()
    if th:
        print(f"📅 Town Hall: {th[0][0]} - {th[0][1]}")
    
    # Prompt for decision
    print("\nWhat should I do with this?")
    print("  Examples:")
    print("    merge with: Joe James")
    print("    add to airtable as George Orbelian")
    print("    drop")
    print("    skip (investigate later)")
    
    decision = input("\n👉 Decision: ").strip()
    
    if decision and decision.lower() != 'skip':
        reviewed_decisions[name] = {
            'decision': decision,
            'confidence': 'HIGH',
            'reason': 'Claude intelligent review'
        }
        print(f"  ✅ Recorded: {decision}")
    else:
        print(f"  ⏭️  Skipped")

conn.close()

# Update decisions with reviewed items
for name, review in reviewed_decisions.items():
    decisions[name].update(review)

print("\n" + "="*80)
print("✅ REVIEW COMPLETE")
print("="*80)
print(f"Reviewed: {len(reviewed_decisions)}/{len(needs_review)}")
print("\nGenerating HTML...")

# Generate HTML with ALL decisions
sorted_names = sorted(names, key=lambda n: {'HIGH': 0, 'MEDIUM': 1, 'NEEDS_REVIEW': 2}[decisions[n]['confidence']])
output = Path(f'/Users/admin/ERA_Admin/integration_scripts/BATCH_REVIEWED_{datetime.now().strftime("%Y%m%d_%H%M")}.html')

high_count = sum(1 for d in decisions.values() if d['confidence'] == 'HIGH')
needs_count = sum(1 for d in decisions.values() if d['confidence'] == 'NEEDS_REVIEW')

# Get evidence for HTML
conn = sqlite3.connect('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')
cur = conn.cursor()

for name in names:
    d = decisions[name]
    
    # Add evidence
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
    d['townhall'] = '<br>'.join([f'<a href="https://docs.google.com/document/d/{a}/edit" target="_blank" class="evidence-link">📅 {dt}</a>' 
                                 for a, dt in th]) if th else "❌"

conn.close()

html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Batch - Reviewed</title>
<style>
body{{font-family:-apple-system;max-width:100%;margin:0;padding:15px;background:#f5f5f5;font-size:13px}}
h1{{color:#2c3e50}}
table{{width:100%;border-collapse:collapse;background:white}}
th{{background:#34495e;color:white;padding:12px;position:sticky;top:0}}
td{{padding:10px;border-bottom:1px solid #ecf0f1}}
tr:hover{{background:#f8f9fa}}
.confidence-HIGH{{background:#d4edda;color:#155724;padding:4px 8px;border-radius:4px}}
.confidence-MEDIUM{{background:#fff3cd;color:#856404;padding:4px 8px;border-radius:4px}}
.confidence-NEEDS_REVIEW{{background:#f8d7da;color:#721c24;padding:4px 8px;border-radius:4px}}
.evidence-link{{color:#3498db;margin-right:8px}}
input{{width:20px;height:20px}}
textarea{{width:100%;padding:6px;border:1px solid #ddd;min-height:50px}}
button{{background:#3498db;color:white;border:none;padding:10px 20px;margin:10px 0;cursor:pointer}}
</style></head><body>
<h1>🧠 Batch - Claude Reviewed</h1>
<p><strong>{len(names)} participants</strong> | HIGH: {high_count} | Need Review: {needs_count}</p>
<p>✅ Safeguards: Number suffix stripping, repeat filtering, intelligent review</p>
<button onclick="exportToCSV()">📥 Export CSV</button>
<table><thead><tr><th style="width:200px">Recommendation</th><th>Name</th><th>Conf</th><th>Reasoning</th><th>Evidence</th><th style="width:200px">Feedback</th></tr></thead><tbody>'''

for name in sorted_names:
    d = decisions[name]
    checked = 'checked' if d['confidence'] == 'HIGH' else ''
    dec = d.get('decision', 'needs investigation')
    conf = d.get('confidence', 'MEDIUM')
    reason = d.get('reason', '')
    
    html += f'''<tr><td><div style="background:#f8f9fa;padding:8px;margin-bottom:8px"><strong>{dec}</strong></div>
<label><input type="checkbox" class="approve-checkbox" {checked}> Approve</label></td>
<td><strong>{name}</strong></td><td><span class="confidence-{conf}">{conf}</span></td>
<td>{reason}</td><td style="font-size:11px">{d.get("fathom", "")}<br>{d.get("gmail", "")}<br>{d.get("townhall", "")}</td>
<td><textarea class="feedback-text"></textarea></td></tr>'''

html += '''</tbody></table><script>
function exportToCSV(){const rows=document.querySelectorAll('tbody tr');let csv=['Name,Decision,Confidence,Reason,Approve,Feedback,ProcessThis'];
rows.forEach(row=>{const cells=row.querySelectorAll('td');const cb=cells[0].querySelector('input');
const dec=cells[0].querySelector('div').textContent.trim();const name=cells[1].textContent.trim();
const conf=cells[2].textContent.trim();const reason=cells[3].textContent.trim().replace(/"/g,'""');
const app=cb.checked?'YES':'NO';const fb=cells[5].querySelector('textarea').value.replace(/"/g,'""');
csv.push(`"${name}","${dec}","${conf}","${reason}","${app}","${fb}","${app}"`);});
const blob=new Blob([csv.join('\\n')],{type:'text/csv'});const url=window.URL.createObjectURL(blob);
const a=document.createElement('a');a.href=url;a.download='batch_'+new Date().toISOString().slice(0,10)+'.csv';
a.click();window.URL.revokeObjectURL(url);
navigator.clipboard.writeText('/Users/admin/Downloads/'+a.download).then(()=>{alert('✅ Exported!\\n📋 Path copied');});}
</script></body></html>'''

with open(output, 'w') as f:
    f.write(html)

print(f"\n✅ Generated: {output}")
print(f"✅ HIGH confidence: {high_count}")
print(f"⚠️  Still need review: {needs_count}")
print("\n🔒 Canonical pipeline complete!")
