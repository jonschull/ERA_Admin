#!/usr/bin/env python3
"""
Compile all 206 categorizations from the interactive Claude session into a single JSON file.
This extracts the decisions from the interactive review process.
"""

import json
import sqlite3
import csv
from pathlib import Path

DB_PATH = Path('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')
PAST_DECISIONS_DIR = Path('past_decisions')
OUTPUT_FILE = Path('all_206_categorizations.json')

# Load all decisions that need attention
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT name FROM participants")
current_names = set(row[0] for row in cursor.fetchall())

decisions = []
for csv_file in sorted(PAST_DECISIONS_DIR.glob('phase4b2_approvals_batch*.csv')):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            variant = row.get('Fathom_Name', '').strip().split('🔁')[0].strip()
            comment = row.get('Comments', '').strip()
            process_this = row.get('ProcessThis', '').upper() == 'YES'
            
            if process_this and variant and variant in current_names:
                cursor.execute("SELECT source_call_url FROM participants WHERE name = ?", (variant,))
                row_data = cursor.fetchone()
                url_list = row_data[0] if row_data else ""
                meeting_count = len([u for u in url_list.split(',') if u.strip()])
                
                decisions.append({
                    'variant': variant,
                    'csv_comment': comment,
                    'meeting_count': meeting_count
                })

conn.close()

print(f"Found {len(decisions)} decisions requiring attention")
print(f"\nNOTE: The complete categorizations with targets and actions")
print(f"were provided during the interactive Claude session in batches of 10.")
print(f"\nTo recreate the full JSON, review the chat history where Claude")
print(f"provided JSON blocks for cases 1-10, 11-20, 21-30, etc.")
print(f"\nSummary available in: categorization_summary.md")
