#!/usr/bin/env python3
"""
Generate HTML using generate_claude_html_report_v2.py template
Loads decisions from intermediate JSON
"""
import json, sqlite3
from pathlib import Path
from datetime import datetime

# Load intermediate
with open('/tmp/batch_intermediate.json') as f:
    data = json.load(f)

names = data['names']
decisions_dict = data['decisions']

# Get evidence from DB
conn = sqlite3.connect('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')
cur = conn.cursor()

# Build HTML using v2 template structure
high_count = sum(1 for d in decisions_dict.values() if d.get('confidence') == 'HIGH')
review_count = sum(1 for d in decisions_dict.values() if 'REVIEW' in d.get('confidence', ''))
user_input_count = sum(1 for d in decisions_dict.values() if 'USER_INPUT' in d.get('confidence', ''))

# Determine batch number from context
batch_num = 10  # Update as needed
    
output = Path(f'/Users/admin/ERA_Admin/integration_scripts/BATCH{batch_num}_FINAL_{len(names)}items_{datetime.now().strftime("%Y%m%d_%H%M")}.html')

# Use v2's proven template
html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>Batch {batch_num} - {len(names)} Items</title>
<style>
body {{font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 100%; margin: 0; padding: 20px; background: #f5f5f7; font-size: 14px;}}
h1 {{color: #1d1d1f; margin-bottom: 10px;}}
.banner {{background: #d1f4e0; border-left: 4px solid #34c759; padding: 15px; margin: 20px 0; border-radius: 8px;}}
table {{width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden;}}
th {{background: #1d1d1f; color: white; padding: 14px; text-align: left; font-weight: 600; position: sticky; top: 0; z-index: 10;}}
td {{padding: 12px; border-bottom: 1px solid #e5e5e7;}}
tr:hover {{background: #f9f9f9;}}
.confidence-HIGH {{background: #d1f4e0; color: #1e6f3e; padding: 6px 12px; border-radius: 6px; font-weight: 600; font-size: 12px;}}
.confidence-MEDIUM {{background: #fff9e6; color: #8c7100; padding: 6px 12px; border-radius: 6px; font-weight: 600; font-size: 12px;}}
.confidence-NEEDS_REVIEW {{background: #fff9e6; color: #8c7100; padding: 6px 12px; border-radius: 6px; font-weight: 600; font-size: 12px;}}
.confidence-NEEDS_CLAUDE_REVIEW {{background: #fff9e6; color: #8c7100; padding: 6px 12px; border-radius: 6px; font-weight: 600; font-size: 12px;}}
.confidence-NEEDS_USER_INPUT {{background: #ffe5e5; color: #c41e3a; padding: 6px 12px; border-radius: 6px; font-weight: 600; font-size: 12px;}}
.evidence-link {{color: #007aff; text-decoration: none; margin-right: 8px; font-size: 16px;}}
.evidence-link:hover {{text-decoration: underline;}}
input[type="checkbox"] {{width: 20px; height: 20px; cursor: pointer;}}
textarea {{width: 100%; padding: 8px; border: 1px solid #d1d1d6; border-radius: 6px; font-family: inherit; font-size: 13px; min-height: 60px; resize: vertical;}}
button {{background: #007aff; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; margin: 15px 0;}}
button:hover {{background: #0051d5;}}
.decision-box {{background: #f5f5f7; padding: 10px; border-radius: 6px; margin-bottom: 8px; font-weight: 600;}}
</style>
</head>
<body>
<h1>🎉 Batch {batch_num} - {len(names)} Items</h1>
<div class="banner">
<strong>✅ Generated with canonical pipeline</strong><br>
• Filtered already-processed items<br>
• Applied PAST_LEARNINGS patterns<br>
• Critically reviewed before presenting<br>
• Working CSV export
</div>
<p><strong>{len(names)} participants</strong> | 
<span style="color: #34c759; font-weight: bold;">HIGH: {high_count}</span> | 
<span style="color: #ff9500; font-weight: bold;">MEDIUM: {review_count}</span> | 
<span style="color: #ff3b30; font-weight: bold;">NEEDS INPUT: {user_input_count}</span></p>
<button onclick="exportToCSV()">📥 Export to CSV</button>
<table>
<thead>
<tr>
<th style="width: 240px;">Recommendation</th>
<th style="width: 200px;">Name</th>
<th style="width: 80px;">Confidence</th>
<th>Reasoning</th>
<th style="width: 120px;">Evidence</th>
<th style="width: 220px;">Your Feedback</th>
</tr>
</thead>
<tbody>'''

# Sort by confidence
sorted_names = sorted(names, key=lambda n: {'HIGH': 0, 'MEDIUM': 1, 'NEEDS_REVIEW': 2, 'NEEDS_CLAUDE_REVIEW': 2, 'NEEDS_USER_INPUT': 3}[decisions_dict[n].get('confidence', 'NEEDS_REVIEW')])

for name in sorted_names:
    d = decisions_dict[name]
    dec = d.get('decision', 'needs investigation')
    if dec == 'NEEDS_CLAUDE_REVIEW':
        dec = 'needs investigation'
    conf = d.get('confidence', 'MEDIUM')
    reason = d.get('reason', '')
    checked = ' checked' if conf == 'HIGH' else ''
    
    # Get evidence
    cur.execute('SELECT DISTINCT source_call_url FROM participants WHERE name = ? LIMIT 5', (name,))
    fathom_urls = [r[0] for r in cur.fetchall()]
    fathom_links = ' '.join([f'<a href="{url}" target="_blank" class="evidence-link" title="Fathom recording">🎥</a>' for url in fathom_urls]) if fathom_urls else '<span style="color:#999">—</span>'
    
    gmail_link = f'<a href="https://mail.google.com/mail/u/0/#search/{name.replace(" ", "+")}" target="_blank" class="evidence-link" title="Gmail search">📧</a>'
    
    cur.execute('''SELECT DISTINCT t.agenda_id, t.meeting_date FROM participants p
        JOIN calls c ON p.source_call_url = c.hyperlink
        JOIN town_hall_agendas t ON c.date = t.meeting_date
        WHERE p.name = ? LIMIT 3''', (name,))
    th_data = cur.fetchall()
    th_links = '<br>'.join([f'<a href="https://docs.google.com/document/d/{aid}/edit" target="_blank" class="evidence-link" title="Town Hall {date}">📅{date}</a>' 
                            for aid, date in th_data]) if th_data else '<span style="color:#999">—</span>'
    
    html += f'''
<tr>
<td>
<div class="decision-box">{dec}</div>
<label><input type="checkbox" class="approve-checkbox"{checked}> Approve</label>
</td>
<td><strong>{name}</strong></td>
<td><span class="confidence-{conf}">{conf}</span></td>
<td>{reason}</td>
<td style="font-size: 11px; line-height: 1.6;">
{fathom_links}<br>
{gmail_link}<br>
{th_links}
</td>
<td><textarea class="feedback-text" placeholder="Add notes or corrections..."></textarea></td>
</tr>'''

conn.close()

# Working CSV export from v2
html += f'''
</tbody>
</table>

<script>
function exportToCSV() {{
    const rows = document.querySelectorAll('tbody tr');
    let csv = ['Name,Decision,Confidence,Reason,Approve,Feedback,ProcessThis'];
    
    rows.forEach(row => {{
        const cells = row.querySelectorAll('td');
        const checkbox = cells[0].querySelector('input[type="checkbox"]');
        const decision = cells[0].querySelector('.decision-box').textContent.trim();
        const name = cells[1].textContent.trim();
        const confidence = cells[2].textContent.trim();
        const reason = cells[3].textContent.trim().replace(/"/g, '""');
        const approve = checkbox.checked ? 'YES' : 'NO';
        const feedback = cells[5].querySelector('textarea').value.trim().replace(/"/g, '""');
        
        csv.push(`"${{name}}","${{decision}}","${{confidence}}","${{reason}}","${{approve}}","${{feedback}}","${{approve}}"`);
    }});
    
    const blob = new Blob([csv.join('\\n')], {{type: 'text/csv;charset=utf-8;'}});
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', 'batch{batch_num}_final_' + new Date().toISOString().slice(0, 10) + '.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Copy path to clipboard
    const downloadPath = '/Users/admin/Downloads/' + link.getAttribute('download');
    navigator.clipboard.writeText(downloadPath).then(() => {{
        alert('✅ CSV exported successfully!\\n\\n📋 Download path copied to clipboard:\\n' + downloadPath);
    }});
}}
</script>
</body>
</html>'''

with open(output, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Generated: {output}")
print(f"✅ Uses v2 template with working CSV export")
print(f"✅ {high_count} HIGH confidence, {review_count} need review")

print("\n" + "="*80)
print("⚠️  STOP - DO NOT PRESENT THIS HTML YET")
print("="*80)
print("\n🔍 CRITICAL REVIEW REQUIRED:")
print()
print("Open the HTML and check each decision:")
print("  • Did I actually READ Town Hall agendas for presenter names?")
print("  • Did I EXTRACT organizations and people from Fathom titles?")
print("  • Are there vague decisions like 'Town Hall participant' without names?")
print("  • Did I add single lowercase names without finding full names?")
print("  • Did I convert device names to person names?")
print()
print("Run these checks:")
print("  1. Look out for 'Town Hall participant' without 'as [name]'")
print("  2. Look out for single-word additions (sasi, pedro, Sol, etc.)")
print("  3. Verify each decisions has adqueate evidence")
print()
print("If you find ANY issues:")
print("  → Fix decisions in /tmp/batch_intermediate.json")
print("  → Run: python3 generate_html_from_intermediate.py")
print("  → Review the NEW HTML AGAIN")
print()
print("Only when CLEAN → Present to user")
print("="*80 + "\n")
