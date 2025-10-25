#!/usr/bin/env python3
"""
Generate HTML report of Claude's AI analysis for human review.
Includes proper evidence links and approve checkboxes.

⚠️  CRITICAL: Before running this script, Claude MUST review:
    1. AI_ASSISTANT_CONTEXT_RECOVERY.md (the complete workflow)
    2. PAST_LEARNINGS.md (known patterns and mappings)
    
    This prevents context loss and ensures consistent judgment.
"""

import json
import re
from datetime import datetime
from pathlib import Path

# ============================================================================
# 🚨 CLAUDE: READ BEFORE PROCEEDING 🚨
# ============================================================================
print("="*80)
print("🤖 CLAUDE'S PRE-FLIGHT CHECKLIST")
print("="*80)
print("\nBefore generating this HTML report, confirm you have reviewed:")
print("")
print("  1. ✓ AI_ASSISTANT_CONTEXT_RECOVERY.md")
print("     → Location: /Users/admin/ERA_Admin/integration_scripts/")
print("     → Contains: Complete workflow, evidence requirements, common mistakes")
print("")
print("  2. ✓ PAST_LEARNINGS.md")
print("     → Location: /Users/admin/ERA_Admin/integration_scripts/")
print("     → Contains: Phone mappings, organizations, name variants")
print("")
print("  3. ✓ Evidence checklist:")
print("     □ Fathom recording links (from DB)")
print("     □ Gmail query links (generated)")
print("     □ Town Hall links (from ai_analysis_input.md)")
print("     □ Airtable status (query for canonical names)")
print("")
print("  4. ✓ Pattern recognition active:")
print("     □ Person in parentheses extraction")
print("     □ Comma patterns (location vs organization)")
print("     □ Number variants")
print("     □ Username checking (don't auto-drop)")
print("")
print("="*80)
print("If you haven't reviewed these, STOP and read them now.")
print("Context loss is the main cause of regressions.")
print("="*80)
print("")

# Load participants
with open('/tmp/phase4b2_test_data.json', 'r') as f:
    participants = json.load(f)

# Load the AI analysis input to get Town Hall evidence
with open('/Users/admin/ERA_Admin/integration_scripts/ai_analysis_input.md', 'r') as f:
    ai_input = f.read()

# Claude's decisions (from previous analysis)
decisions = {
    'JP': {'decision': 'merge with: John Perlin', 'confidence': 'HIGH', 'reason': 'Found in 3 Town Halls. JP = John Perlin pattern'},
    'Jon Schull (Enabling The Future)': {'decision': 'merge with: Jon Schull', 'confidence': 'HIGH', 'reason': 'This is you - variant name'},
    'Jon Schull, EcoRestoration Alliance': {'decision': 'merge with: Jon Schull', 'confidence': 'HIGH', 'reason': 'This is you'},
    'Jon Schull, EcoRestoration Alliance (2)': {'decision': 'merge with: Jon Schull', 'confidence': 'HIGH', 'reason': 'This is you - number variant'},
    'Jon Schull, EcoRestoration Alliance (7)': {'decision': 'merge with: Jon Schull', 'confidence': 'HIGH', 'reason': 'This is you - number variant'},
    'Joshua Konkankoh': {'decision': 'add to airtable', 'confidence': 'HIGH', 'reason': 'Found in 2 Town Halls. Cameroonian journalist'},
    'Joshua Laizer (4)': {'decision': 'merge with: Joshua Laizer', 'confidence': 'HIGH', 'reason': 'Number variant. 3 Town Halls'},
    'Joshua Laizer (7)': {'decision': 'merge with: Joshua Laizer', 'confidence': 'HIGH', 'reason': 'Number variant. 3 Town Halls'},
    'Judith D. Schwartz': {'decision': 'add to airtable', 'confidence': 'HIGH', 'reason': 'Found in 2 Town Halls. Author, Soil Centric'},
    'Julia': {'decision': 'add to airtable as Julia Lindley', 'confidence': 'HIGH', 'reason': 'Found in 2 Town Halls as Julia Lindley'},
    'Justin Ritchie (3)': {'decision': 'merge with: Justin Ritchie', 'confidence': 'HIGH', 'reason': 'Number variant. 3 Town Halls'},
    'KALOMBO-MBILIZI': {'decision': 'merge with: Kalombo Mbilizi', 'confidence': 'HIGH', 'reason': 'All-caps variant. 3 Town Halls'},
    'Kaluki Paul Mutuku (2)': {'decision': 'merge with: Kaluki Paul Mutuku', 'confidence': 'HIGH', 'reason': 'Number variant. 3 Town Halls'},
    'Kaluki Paul Mutuku (4)': {'decision': 'merge with: Kaluki Paul Mutuku', 'confidence': 'HIGH', 'reason': 'Number variant. 3 Town Halls'},
    'Karim': {'decision': 'add to airtable as Karim Camara', 'confidence': 'HIGH', 'reason': '3 Town Halls. Context: Abdoul Karim Camara, Guinea'},
    'Katrina Jeffries (5)': {'decision': 'merge with: Katrina Jeffries', 'confidence': 'HIGH', 'reason': 'Number variant. 3 Town Halls'},
    'Kethia': {'decision': 'merge with: Kethia Calixte', 'confidence': 'HIGH', 'reason': '1 Town Hall. Single name variant'},
    'Kevin A.': {'decision': 'add to airtable', 'confidence': 'HIGH', 'reason': 'Found in 3 Town Halls'},
    'Kevin Li': {'decision': 'add to airtable', 'confidence': 'HIGH', 'reason': 'Found in 3 Town Halls'},
    'Leonard': {'decision': 'merge with: Leonard Iyamuremye', 'confidence': 'HIGH', 'reason': 'Single name variant. 3 Town Halls'},
    'Leonard IYAMUREME': {'decision': 'merge with: Leonard Iyamuremye', 'confidence': 'HIGH', 'reason': 'Spelling variant. 3 Town Halls'},
    'Joshua Laizer': {'decision': 'add to airtable', 'confidence': 'HIGH', 'reason': '5 Fathom recordings = clear participant'},
    'Kaluki Paul Mutuku': {'decision': 'add to airtable', 'confidence': 'HIGH', 'reason': 'Base name for variants'},
    
    # Medium confidence
    'Jeremy - Open Forest Protocol': {'decision': 'add to airtable', 'confidence': 'MEDIUM', 'reason': '1 Town Hall. Direct msg about OpenForestProtocol.org'},
    'Justin R-Söndergaard': {'decision': 'merge with: Justin Roborg-Sondergaard', 'confidence': 'MEDIUM', 'reason': '83% Airtable match'},
    'Katharine King': {'decision': 'add to airtable', 'confidence': 'MEDIUM', 'reason': '2 Town Halls'},
    'Kathleen Groppe': {'decision': 'add to airtable', 'confidence': 'MEDIUM', 'reason': '1 Town Hall. You asked her to present'},
    'Kathryn Alexander, MA': {'decision': 'add to airtable', 'confidence': 'MEDIUM', 'reason': '1 Town Hall. Requested email list'},
    'Kim Chapple': {'decision': 'merge with: Kimberly Chapple', 'confidence': 'MEDIUM', 'reason': 'Kim = Kimberly. 1 Town Hall'},
    'Kwaxala / Pete': {'decision': 'add to airtable as Pete Corke', 'confidence': 'MEDIUM', 'reason': '1 Town Hall. Your comment suggests Pete Corke'},
    'Larry Kopald': {'decision': 'add to airtable', 'confidence': 'MEDIUM', 'reason': '1 Town Hall. Your comment: answer is obvious'},
    'Lee G': {'decision': 'merge with: Lee Golpariani', 'confidence': 'MEDIUM', 'reason': 'Lee G = Lee Golpariani pattern'},
    'Juan José Pimento': {'decision': 'add to airtable', 'confidence': 'MEDIUM', 'reason': '1 Town Hall from Panama'},
    'Juan from Panama': {'decision': 'merge with: Juan Carlos Monterrey', 'confidence': 'MEDIUM', 'reason': 'Your comment suggests this name'},
    'Justin Ritchie': {'decision': 'add to airtable', 'confidence': 'MEDIUM', 'reason': '1 Town Hall presenting Transition US'},
    "Lastborn's Galaxy A11 (3)": {'decision': 'merge with: Ilarion', 'confidence': 'MEDIUM', 'reason': '3 Town Halls. Your comment: Ilarion Mercullief'},
    
    # Low/Drop
    'Belizey': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    'John K Carroll': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    "John's iPhone": {'decision': 'drop', 'confidence': 'LOW', 'reason': 'Device name'},
    "Josean's iPhone": {'decision': 'drop', 'confidence': 'LOW', 'reason': 'Device name'},
    "Josean's iPhone (11)": {'decision': 'drop', 'confidence': 'LOW', 'reason': 'Device name'},
    'Joseph Manning': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    'Joshua Shepard': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    'Judith Rosen': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    'Jules': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    'Joshua Price': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'Context is about economics not person'},
    'Kaitlin Sullivan': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    'Kathia Burillo': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    'Kinari Webb': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    "Lastborn's Galaxy A11": {'decision': 'drop', 'confidence': 'LOW', 'reason': 'Device name'},
}

def extract_townhall_evidence(name):
    """Extract Town Hall meeting evidence from ai_analysis_input.md"""
    # Find the case for this name
    pattern = rf'## CASE \d+: {re.escape(name)}.*?\*\*Town Hall:\*\*(.*?)(?:\*\*Gmail:|\*\*Airtable:|\*\*Fathom recording:)'
    match = re.search(pattern, ai_input, re.DOTALL)
    
    if not match:
        return "No Town Hall data"
    
    townhall_text = match.group(1).strip()
    
    if "Not found" in townhall_text:
        return "❌ No Town Hall meetings"
    
    # Extract meeting dates
    date_pattern = r'\*\*(\d{4}-\d{2}-\d{2}):\*\*'
    dates = re.findall(date_pattern, townhall_text)
    
    if not dates:
        # Try to count meetings
        meeting_match = re.search(r'Found in (\d+) meeting', townhall_text)
        if meeting_match:
            count = meeting_match.group(1)
            return f"<strong>{count} Town Hall meetings</strong><br><small>See ai_analysis_input.md for details</small>"
        return "Town Hall data present"
    
    html = f"<strong>{len(dates)} Town Hall meeting(s):</strong><br>"
    for date in dates[:3]:  # Show up to 3
        # Create link to Town Hall agenda (generic for now)
        html += f'<small>📅 <a href="https://docs.google.com/document/d/1oPYGLKfQ0PFWJHpME0hKhRHYXZbh73kFXnq2kRF8UiU/edit" target="_blank" class="evidence-link">{date}</a></small><br>'
    
    return html

# Generate HTML
output_file = Path(__file__).parent / f'CLAUDE_RECOMMENDATIONS_{datetime.now().strftime("%Y%m%d_%H%M")}.html'

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude's AI Recommendations - Phase 4B-2</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 100%;
            margin: 0 auto;
            padding: 15px;
            background: #f5f5f5;
            font-size: 13px;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .header {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .instructions {{
            background: #e8f4f8;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin-bottom: 20px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .stat-box {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
            color: #3498db;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            font-size: 14px;
        }}
        
        .controls {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        button {{
            background: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 10px;
            font-size: 14px;
        }}
        
        button:hover {{
            background: #2980b9;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        th {{
            background: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
            position: sticky;
            top: 0;
        }}
        
        td {{
            padding: 10px;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        input[type="checkbox"] {{
            width: 20px;
            height: 20px;
            cursor: pointer;
        }}
        
        textarea {{
            width: 100%;
            padding: 6px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: inherit;
            resize: vertical;
            min-height: 50px;
        }}
        
        .confidence-HIGH {{
            background: #d4edda;
            color: #155724;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
        }}
        
        .confidence-MEDIUM {{
            background: #fff3cd;
            color: #856404;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
        }}
        
        .confidence-LOW {{
            background: #f8d7da;
            color: #721c24;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
        }}
        
        .evidence-link {{
            color: #3498db;
            text-decoration: none;
        }}
        
        .evidence-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 Claude's AI Recommendations - Phase 4B-2</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p><strong>Purpose:</strong> AI-first intelligent analysis with evidence. Review, provide feedback, export CSV.</p>
    </div>
    
    <div class="instructions">
        <h3>📖 How This Works</h3>
        <ol>
            <li><strong>Review my recommendation:</strong> Each row shows my unambiguous decision above the Approve checkbox</li>
            <li><strong>Check evidence:</strong> Click Town Hall dates, Email Query, and Fathom links to verify</li>
            <li><strong>Approve checkbox:</strong> 
                <ul>
                    <li>✓ Checked = Process this recommendation (HIGH confidence pre-checked)</li>
                    <li>✗ Unchecked = Don't process (needs more review)</li>
                </ul>
            </li>
            <li><strong>Add feedback/guidance:</strong> I ALWAYS read comments (even if approved):
                <ul>
                    <li>✅ Leave blank if you agree with my decision</li>
                    <li>❌ "wrong because..." - Teach me what I got wrong</li>
                    <li>🔧 "should be: [correct action]" - Override my decision</li>
                    <li>💡 "guidance: ..." - Help me improve future judgment</li>
                    <li>❓ I may pre-fill questions where I need your help</li>
                </ul>
            </li>
            <li><strong>Export CSV:</strong> Click button, save, send back to me to learn and apply</li>
        </ol>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-value">{len(participants)}</div>
            <div class="stat-label">Total Cases</div>
        </div>
        <div class="stat-box" style="background: #d4edda;">
            <div class="stat-value" style="color: #28a745;">{sum(1 for d in decisions.values() if d.get('confidence') == 'HIGH')}</div>
            <div class="stat-label">✅ High Confidence (Auto-Approved)</div>
        </div>
        <div class="stat-box" style="background: #fff3cd;">
            <div class="stat-value" style="color: #ffc107;">{sum(1 for d in decisions.values() if d.get('confidence') == 'MEDIUM')}</div>
            <div class="stat-label">🤔 Medium Confidence</div>
        </div>
        <div class="stat-box" style="background: #f8d7da;">
            <div class="stat-value" style="color: #dc3545;">{sum(1 for d in decisions.values() if d.get('confidence') == 'LOW')}</div>
            <div class="stat-label">⚠️ Low/Drop</div>
        </div>
    </div>
    
    <div class="controls">
        <button onclick="exportToCSV()">📥 Export to CSV</button>
        <button onclick="checkAll()">✓ Check All</button>
        <button onclick="uncheckAll()">✗ Uncheck All</button>
        <button onclick="filterByConfidence('all')">Show All</button>
        <button onclick="filterByConfidence('HIGH')">High Only</button>
        <button onclick="filterByConfidence('MEDIUM')">Medium Only</button>
        <button onclick="filterByConfidence('LOW')">Low Only</button>
    </div>
    
    <table id="recommendationsTable">
        <thead>
            <tr>
                <th style="width: 250px;">Claude's Recommendation</th>
                <th>Name</th>
                <th>Confidence</th>
                <th>Claude's Reasoning</th>
                <th>Evidence Links</th>
                <th style="width: 250px;">Your Feedback/Guidance</th>
            </tr>
        </thead>
        <tbody>
'''

# Sort by confidence: HIGH -> MEDIUM -> LOW
sorted_participants = sorted(participants, key=lambda p: {
    'HIGH': 0, 'MEDIUM': 1, 'LOW': 2, 'NONE': 3
}.get(decisions.get(p['name'], {}).get('confidence', 'NONE'), 3))

for p in sorted_participants:
    name = p['name']
    decision_info = decisions.get(name, {
        'decision': '[NO DECISION]',
        'confidence': 'NONE',
        'reason': 'Not analyzed'
    })
    
    decision = decision_info['decision']
    confidence = decision_info.get('confidence', 'NONE')
    reason = decision_info['reason']
    
    # Approve checkbox - checked for HIGH confidence
    checked = 'checked' if confidence == 'HIGH' else ''
    
    # Format clear recommendation
    recommendation_html = f'<div style="background: #f8f9fa; padding: 8px; border-radius: 4px; margin-bottom: 8px;"><strong>{decision}</strong></div>'
    
    # Get evidence
    townhall_evidence = extract_townhall_evidence(name)
    
    # Gmail link
    gmail_link = f"https://mail.google.com/mail/u/0/#search/{name.replace(' ', '%20')}"
    
    # Fathom recording link (if we have it from participant data)
    fathom_link = ''
    if 'fathom_url' in p:
        fathom_link = f'<a href="{p["fathom_url"]}" target="_blank" class="evidence-link">🎥 Fathom</a> | '
    
    # Pre-fill guidance in comment box for cases that need it
    prefill_guidance = ''
    if 'Open Forest Protocol' in name:
        prefill_guidance = 'Need full name from OpenForestProtocol.org'
    elif 'Kevin A.' in name or 'Lee G' in name:
        prefill_guidance = 'Need full last name'
    elif decision == 'drop' and 'No context' in reason:
        prefill_guidance = ''  # No guidance needed for clear drops
    
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
                <td>{reason}</td>
                <td style="font-size: 11px;">
                    <div style="margin-bottom: 5px;">{townhall_evidence}</div>
                    {fathom_link}<a href="{gmail_link}" target="_blank" class="evidence-link">📧 Email Query</a>
                </td>
                <td><textarea class="feedback-text" placeholder="Your feedback, corrections, or guidance...">{prefill_guidance}</textarea></td>
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
            
            // Header
            csv.push('Name,Claude_Decision,Confidence,Claude_Reasoning,Approve,Your_Feedback,ProcessThis');
            
            // Data rows
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
            
            // Download
            const csvContent = csv.join('\\n');
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.download = 'claude_recommendations_feedback.csv';
            a.click();
            window.URL.revokeObjectURL(url);
        }
        
        function checkAll() {
            document.querySelectorAll('.approve-checkbox').forEach(cb => cb.checked = true);
        }
        
        function uncheckAll() {
            document.querySelectorAll('.approve-checkbox').forEach(cb => cb.checked = false);
        }
        
        function filterByConfidence(level) {
            const rows = document.querySelectorAll('#recommendationsTable tbody tr');
            rows.forEach(row => {
                if (level === 'all') {
                    row.style.display = '';
                } else {
                    const confidenceSpan = row.querySelector('[class^="confidence-"]');
                    if (confidenceSpan && confidenceSpan.textContent === level) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                }
            });
        }
    </script>
</body>
</html>
'''

# Write file
with open(output_file, 'w') as f:
    f.write(html)

print(f"✅ Generated HTML report: {output_file}")
print()
print("📋 Next steps:")
print("  1. Open the HTML in your browser")
print("  2. Review Claude's decisions and evidence links")
print("  3. Uncheck 'Approve' if wrong, add feedback")
print("  4. Click 'Export to CSV'")
print("  5. Send the CSV back to Claude to learn and apply")
