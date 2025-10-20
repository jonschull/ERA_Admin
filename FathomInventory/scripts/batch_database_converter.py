#!/usr/bin/env python3
"""
Batch converter for all emails in the database.
Uses the clean conversion function from email_conversion/fathom_email_2_md.py
"""

import os
import sys
import sqlite3
from pathlib import Path

# To reliably import from the email_conversion directory at project root
script_dir = Path(__file__).resolve().parent
project_dir = script_dir.parent
conversion_dir = project_dir / 'email_conversion'
sys.path.insert(0, str(conversion_dir))

from fathom_email_2_md import convert_html_to_markdown

def batch_convert_all_emails(db_path="fathom_emails.db", limit=None, test_mode=False, new_only=False):
    """Convert all emails from database. In test mode, just count successes without saving."""
    
    if not os.path.exists(db_path):
        print(f"❌ Error: Database not found at {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Add body_md column if it doesn't exist
    try:
        cursor.execute('ALTER TABLE emails ADD COLUMN body_md TEXT')
        print("✅ Added body_md column to database")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("📋 body_md column already exists")
        else:
            print(f"❌ Error adding column: {e}")
            return False
    
    # Get total count
    cursor.execute('SELECT COUNT(*) FROM emails WHERE body_html IS NOT NULL')
    total_count = cursor.fetchone()[0]
    
    print(f"📊 Found {total_count} emails with HTML content")
    
    # Build query with optional limit
    query = 'SELECT message_id, date, subject, body_html FROM emails WHERE body_html IS NOT NULL ORDER BY date'
    if limit:
        query += f' LIMIT {limit}'
        print(f"🔄 {'TEST MODE: ' if test_mode else ''}Processing first {limit} emails...")
    else:
        print(f"🔄 {'TEST MODE: ' if test_mode else ''}Processing all {total_count} emails...")
    
    if test_mode:
        print("   (Converting in memory only - no files or database changes)")
    
    cursor.execute(query)
    
    success_count = 0
    error_count = 0
    
    print("\n" + "="*80)
    
    for i, (message_id, date, subject, html_content) in enumerate(cursor.fetchall(), 1):
        # Convert HTML to Markdown using the pure function with metadata extraction
        try:
            markdown_result, stats = convert_html_to_markdown(html_content, extract_stats=True)
            
            # Apply timestamp fix
            markdown_result = markdown_result.replace('×tamp=', '&timestamp=')
            
            # Check if conversion was successful (not an error message)
            if markdown_result.startswith("# Error:"):
                error_count += 1
                if error_count <= 5:  # Show first few errors
                    print(f"  [{i:4d}] ❌ {message_id} - {markdown_result.split('.')[0]}")
            else:
                success_count += 1
                # Count links for verification
                import re
                from datetime import datetime
                link_count = len(re.findall(r'\[([^\]]+)\]\([^\)]+\)', markdown_result))
                
                if test_mode:
                    if i % 100 == 0 or i <= 10:  # Progress updates in test mode
                        print(f"  [{i:4d}] ✅ {message_id} ({link_count} links) - {date}")
                else:
                    # Save to database body_md field AND metadata
                    cursor.execute('''UPDATE emails SET 
                        body_md = ?,
                        meeting_title = ?,
                        meeting_date = ?,
                        meeting_duration_mins = ?,
                        meeting_url = ?,
                        ask_fathom_url = ?,
                        action_items_count = ?,
                        topics_count = ?,
                        next_steps_count = ?,
                        total_links_count = ?,
                        fathom_timestamp_links_count = ?,
                        parsed_at = ?
                        WHERE message_id = ?''', 
                        (markdown_result,
                         stats.get('meeting_title'),
                         stats.get('meeting_date'),
                         stats.get('meeting_duration_mins'),
                         stats.get('meeting_url'),
                         stats.get('ask_fathom_url'),
                         stats.get('action_items_count'),
                         stats.get('topics_count'),
                         stats.get('next_steps_count'),
                         stats.get('total_links_count'),
                         stats.get('fathom_timestamp_links_count'),
                         datetime.now().isoformat(),
                         message_id))
                    if i % 100 == 0 or i <= 10:
                        print(f"  [{i:4d}] ✅ {message_id} saved to database ({link_count} links)")
        
        except Exception as e:
            error_count += 1            
            if error_count <= 5:
                print(f"  [{i:4d}] ❌ {message_id} - Exception: {str(e)[:50]}...")
    
    # Commit changes if not in test mode
    if not test_mode:
        conn.commit()
        print(f"💾 Database changes committed")
    
    conn.close()
    
    print("="*80)
    print(f"📊 {'TEST MODE ' if test_mode else ''}CONVERSION COMPLETE")
    print(f"✅ Successful conversions: {success_count}")
    print(f"❌ Failed conversions: {error_count}")
    
    if test_mode:
        print(f"💡 Test complete - no files created, no database changes")
        success_rate = (success_count / (success_count + error_count)) * 100 if (success_count + error_count) > 0 else 0
        print(f"📈 Success rate: {success_rate:.1f}%")
    else:
        print(f"💾 {success_count} records updated in database")
    
    return success_count > 0

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert all database emails to Markdown')
    parser.add_argument('--db', default='fathom_emails.db', help='Database file path')
    parser.add_argument('--limit', type=int, help='Limit number of emails to process')
    parser.add_argument('--test', action='store_true', help='Test mode: convert in memory only, no saving')
    
    args = parser.parse_args()
    
    batch_convert_all_emails(args.db, args.limit, args.test)
