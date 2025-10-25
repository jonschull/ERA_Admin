#!/usr/bin/env python3
"""
Create review CSV from Claude's analysis for human approval.

Takes Claude's markdown analysis and converts it to a CSV format
that the human can review, annotate, and pass back.
"""

import json
import csv
from pathlib import Path

# Load original participant data
with open('/tmp/phase4b2_test_data.json', 'r') as f:
    participants = json.load(f)

# Parse Claude's analysis from markdown
# (In production, this would parse the markdown file)
# For now, hardcoding the decisions

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
    
    # Low/Drop
    'Belizey': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    'John K Carroll': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    "John's iPhone": {'decision': 'drop', 'confidence': 'LOW', 'reason': 'Device name'},
    "Josean's iPhone": {'decision': 'drop', 'confidence': 'LOW', 'reason': 'Device name'},
    "Josean's iPhone (11)": {'decision': 'drop', 'confidence': 'LOW', 'reason': 'Device name'},
    'Joseph Manning': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    'Joshua Shepard': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    'Juan José Pimento': {'decision': 'add to airtable', 'confidence': 'MEDIUM', 'reason': '1 Town Hall from Panama'},
    'Juan from Panama': {'decision': 'merge with: Juan Carlos Monterrey', 'confidence': 'MEDIUM', 'reason': 'Your comment suggests this name'},
    'Judith Rosen': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    'Jules': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    'Justin Ritchie': {'decision': 'add to airtable', 'confidence': 'MEDIUM', 'reason': '1 Town Hall presenting Transition US'},
    'Joshua Laizer': {'decision': 'add to airtable', 'confidence': 'HIGH', 'reason': '5 Fathom recordings = clear participant'},
    'Joshua Price': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'Context is about economics not person'},
    'Kaitlin Sullivan': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    'Kathia Burillo': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    'Kinari Webb': {'decision': 'drop', 'confidence': 'LOW', 'reason': 'No context found'},
    "Lastborn's Galaxy A11": {'decision': 'drop', 'confidence': 'LOW', 'reason': 'Device name'},
    "Lastborn's Galaxy A11 (3)": {'decision': 'merge with: Ilarion', 'confidence': 'MEDIUM', 'reason': '3 Town Halls. Your comment: Ilarion Mercullief'},
    'Kaluki Paul Mutuku': {'decision': 'add to airtable', 'confidence': 'HIGH', 'reason': 'Base name for variants'},
}

# Create CSV
output_file = Path(__file__).parent / 'phase4b2_CLAUDE_RECOMMENDATIONS.csv'

with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Name',
        'Claude_Decision',
        'Confidence',
        'Claude_Reasoning',
        'Town_Hall_Count',
        'Your_Feedback_Here',
        'ProcessThis'
    ])
    
    for p in participants:
        name = p['name']
        decision_info = decisions.get(name, {
            'decision': '[NO DECISION]',
            'confidence': 'NONE',
            'reason': 'Not analyzed'
        })
        
        # Get Town Hall count from our search
        # (Would normally read from database)
        th_count = '?'
        
        # Auto-check ProcessThis for HIGH confidence
        process = 'YES' if decision_info['confidence'] == 'HIGH' else 'NO'
        
        writer.writerow([
            name,
            decision_info['decision'],
            decision_info['confidence'],
            decision_info['reason'],
            th_count,
            '',  # Empty for your feedback
            process
        ])

print(f"✅ Created review CSV: {output_file}")
print()
print("📋 Next steps:")
print("  1. Open the CSV in Excel/Numbers")
print("  2. Review Claude's decisions")
print("  3. Add your feedback/corrections in 'Your_Feedback_Here' column")
print("  4. Change ProcessThis to YES/NO as needed")
print("  5. Save and send back to Claude")
