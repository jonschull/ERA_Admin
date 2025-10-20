#!/usr/bin/env python3
"""
Sync ERA meetings: Mark existing ERA meetings in TSV and add new ones from database
- Excludes e-NABLE Town Halls
- Includes ERA Town Hall and ERA Africa meetings
- Adds meetings from database that aren't in TSV yet
"""
import csv
import sqlite3
import sys

TSV_FILE = 'era connections.tsv'
DB_FILE = '../fathom_emails.db'

# Keywords for ERA meetings (excluding e-NABLE)
ERA_KEYWORDS = [
    'era town hall',
    'era africa',
    'africa town',
]

def get_era_meetings_from_db():
    """Get all ERA meetings from database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT title, date, duration, hyperlink, share_status, shared_with, share_timestamp
        FROM calls
        ORDER BY date DESC
    """)
    
    all_calls = cursor.fetchall()
    conn.close()
    
    era_meetings = []
    for title, date, duration, hyperlink, share_status, shared_with, share_timestamp in all_calls:
        title_lower = title.lower() if title else ''
        
        # Check if it's an ERA meeting (NOT e-NABLE)
        is_era = any(kw in title_lower for kw in ERA_KEYWORDS)
        is_enable = 'enable' in title_lower and 'era' not in title_lower
        
        if is_era and not is_enable:
            era_meetings.append({
                'Title': title,
                'Date': date,
                'Duration': duration,
                'Hyperlink': hyperlink,
                'shareStatus': share_status or '',
                'sharedWith': shared_with or '',
                'shareTimestamp': share_timestamp or ''
            })
    
    return era_meetings

def sync_tsv():
    """Sync ERA meetings: mark existing and add new"""
    
    print("📖 Reading era connections.tsv...")
    with open(TSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        fieldnames = reader.fieldnames
        existing_rows = list(reader)
    
    # Build lookup of existing hyperlinks
    existing_hyperlinks = {row['Hyperlink'] for row in existing_rows}
    
    print(f"📊 Existing TSV rows: {len(existing_rows)}")
    
    # Get ERA meetings from database
    print("🔍 Querying database for ERA meetings...")
    db_era_meetings = get_era_meetings_from_db()
    print(f"📊 ERA meetings in database: {len(db_era_meetings)}")
    
    # Mark existing ERA meetings in TSV
    marked_count = 0
    for row in existing_rows:
        title_lower = row['Title'].lower()
        is_era = any(kw in title_lower for kw in ERA_KEYWORDS)
        is_enable = 'enable' in title_lower and 'era' not in title_lower
        
        if is_era and not is_enable:
            if not row['Analyze'].strip():
                row['Analyze'] = 'x'
                marked_count += 1
    
    print(f"✅ Marked {marked_count} existing ERA meetings in TSV")
    
    # Add new ERA meetings from database
    new_meetings = []
    for meeting in db_era_meetings:
        if meeting['Hyperlink'] not in existing_hyperlinks:
            new_meetings.append({
                'Title': meeting['Title'],
                'Nickname': '',
                'ERA': '',
                'Analyze': 'x',  # Auto-mark new ERA meetings
                'Date': meeting['Date'],
                'Duration': meeting['Duration'],
                'Hyperlink': meeting['Hyperlink'],
                'shareStatus': meeting['shareStatus'],
                'sharedWith': meeting['sharedWith'],
                'shareTimestamp': meeting['shareTimestamp']
            })
    
    print(f"➕ Adding {len(new_meetings)} new ERA meetings from database")
    
    # Combine and sort
    all_rows = existing_rows + new_meetings
    
    # Show sample of what will be analyzed
    print("\n📋 Sample of ERA meetings to analyze:")
    sample_count = 0
    for row in all_rows:
        if row['Analyze'] == 'x':
            if sample_count < 5:
                print(f"  - {row['Date']} - {row['Title'][:60]}")
                sample_count += 1
    
    # Count total marked
    total_marked = sum(1 for row in all_rows if row['Analyze'].strip())
    print(f"\n📊 Total ERA meetings marked for analysis: {total_marked}")
    
    # Write back
    print(f"\n💾 Writing updated TSV...")
    with open(TSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(all_rows)
    
    print("✅ TSV updated successfully")
    
    return total_marked, len(new_meetings)

if __name__ == '__main__':
    try:
        total, added = sync_tsv()
        print(f"\n{'='*60}")
        print(f"✅ SUCCESS:")
        print(f"   {total} ERA meetings marked for analysis")
        print(f"   {added} new meetings added from database")
        print(f"{'='*60}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
