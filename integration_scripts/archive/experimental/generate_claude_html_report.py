#!/usr/bin/env python3
"""
Generate HTML report of Claude's AI analysis for human review.
User reviews HTML, then provides CSV back with feedback.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

# Load participants
with open('/tmp/phase4b2_test_data.json', 'r') as f:
    participants = json.load(f)

# Connect to databases for evidence
townhall_db = '/Users/admin/ERA_Admin/FathomInventory/analysis/town_hall_enriched.db'
fathom_db = '/Users/admin/ERA_Admin/FathomInventory/analysis/fathom.db'

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

def get_townhall_evidence(name):
    """Get Town Hall meeting evidence for a name"""
    try:
        conn = sqlite3.connect(townhall_db)
        cur = conn.cursor()
        
        cur.execute('''
            SELECT meeting_date, meeting_title, context_snippet 
            FROM participant_town_hall_context 
            WHERE normalized_name LIKE ?
            ORDER BY meeting_date DESC
            LIMIT 3
        ''', (f'%{name}%',))
        
        meetings = cur.fetchall()
        conn.close()
        
        if not meetings:
            return "No Town Hall meetings found"
        
        html = f"<strong>{len(meetings)} meetings:</strong><br>"
        for date, title, snippet in meetings:
            snippet_short = snippet[:80] + "..." if len(snippet) > 80 else snippet
            html += f"<small>• {date}: {snippet_short}</small><br>"
        
        return html
    except Exception as e:
        return f"Error: {str(e)}"

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
        
        textarea {{
            width: 100%;
            padding: 6px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: inherit;
            resize: vertical;
            min-height: 60px;
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
            font-size: 11px;
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
            <li><strong>AI analyzed first:</strong> Claude read all Town Hall context, Gmail, and Airtable data</li>
            <li><strong>Review decisions:</strong> Check AI's recommendation, confidence, and evidence links</li>
            <li><strong>Add feedback:</strong> In "Your Feedback" column:
                <ul>
                    <li>✅ <code>approve</code> - AI is correct</li>
                    <li>❌ <code>wrong because...</code> - Explain the error to teach AI</li>
                    <li>🔧 <code>should be: [action]</code> - Provide correct decision</li>
                    <li>💡 <code>guidance: ...</code> - General feedback to improve AI judgment</li>
                </ul>
            </li>
            <li><strong>Export CSV:</strong> Click button below, save file</li>
            <li><strong>Send back:</strong> Give CSV to Claude to learn and apply</li>
        </ol>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-value">{len(participants)}</div>
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
        <div class="stat-box" style="background: #f8d7da;">
            <div class="stat-value" style="color: #dc3545;">{sum(1 for d in decisions.values() if d['confidence'] == 'LOW')}</div>
            <div class="stat-label">⚠️ Low/Drop</div>
        </div>
    </div>
    
    <div class="controls">
        <button onclick="exportToCSV()">📥 Export to CSV</button>
        <button onclick="filterByConfidence('all')">Show All</button>
        <button onclick="filterByConfidence('HIGH')">High Confidence Only</button>
        <button onclick="filterByConfidence('MEDIUM')">Medium Only</button>
        <button onclick="filterByConfidence('LOW')">Low/Drop Only</button>
    </div>
    
    <table id="recommendationsTable">
        <thead>
            <tr>
                <th>Name</th>
                <th>Claude's Decision</th>
                <th>Confidence</th>
                <th>Claude's Reasoning</th>
                <th>Evidence Links</th>
                <th>Your Feedback Here</th>
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
    confidence = decision_info['confidence']
    reason = decision_info['reason']
    
    # Get evidence
    townhall_evidence = get_townhall_evidence(name)
    
    # Gmail link
    gmail_link = f"https://mail.google.com/mail/u/0/#search/{name.replace(' ', '%20')}"
    
    html += f'''
            <tr class="confidence-{confidence}">
                <td><strong>{name}</strong></td>
                <td><strong>{decision}</strong></td>
                <td><span class="confidence-{confidence}">{confidence}</span></td>
                <td>{reason}</td>
                <td style="font-size: 11px;">
                    <div>{townhall_evidence}</div>
                    <a href="{gmail_link}" target="_blank" class="evidence-link">📧 Gmail Search</a>
                </td>
                <td><textarea id="feedback_{name.replace(" ", "_")}" placeholder="Your feedback, corrections, or 'approve'"></textarea></td>
            </tr>
'''

html += '''
        </tbody>
    </table>
    
    <script>
        function exportToCSV() {
            const table = document.getElementById('recommendationsTable');
            const rows = table.querySelectorAll('tr');
            let csv = [];
            
            // Header
            csv.push('Name,Claude_Decision,Confidence,Claude_Reasoning,Your_Feedback,ProcessThis');
            
            // Data rows (skip header row)
            for (let i = 1; i < rows.length; i++) {
                const cells = rows[i].querySelectorAll('td');
                if (cells.length === 0) continue;
                
                const name = cells[0].textContent.trim();
                const decision = cells[1].textContent.trim();
                const confidence = cells[2].textContent.trim();
                const reasoning = cells[3].textContent.trim().replace(/"/g, '""');
                const feedback = cells[5].querySelector('textarea').value.replace(/"/g, '""');
                const processThis = feedback.toLowerCase().includes('approve') || confidence === 'HIGH' ? 'YES' : 'NO';
                
                csv.push(`"${name}","${decision}","${confidence}","${reasoning}","${feedback}","${processThis}"`);
            }
            
            // Download
            const csvContent = csv.join('\\n');
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'claude_recommendations_feedback.csv';
            a.click();
            window.URL.revokeObjectURL(url);
        }
        
        function filterByConfidence(level) {
            const rows = document.querySelectorAll('#recommendationsTable tbody tr');
            rows.forEach(row => {
                if (level === 'all') {
                    row.style.display = '';
                } else {
                    const confidence = row.querySelector('.confidence-HIGH, .confidence-MEDIUM, .confidence-LOW');
                    if (confidence && confidence.textContent === level) {
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
print("  2. Review Claude's decisions and evidence")
print("  3. Add your feedback in the textarea")
print("  4. Click 'Export to CSV'")
print("  5. Send the CSV back to Claude")
