#!/usr/bin/env python3
"""
Mark ERA Town Hall and ERA Africa meetings for analysis in era connections.tsv
"""
import csv
import sys

TSV_FILE = 'era connections.tsv'

# Keywords to identify ERA meetings
ERA_KEYWORDS = [
    'town hall',
    'era africa',
    'africa town',
    'enable town hall',  # e-NABLE is related
]

def mark_era_meetings():
    """Mark ERA-related meetings in the TSV file"""
    
    print("📖 Reading era connections.tsv...")
    with open(TSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        fieldnames = reader.fieldnames
        rows = list(reader)
    
    print(f"📊 Total rows: {len(rows)}")
    
    # Find and mark ERA meetings
    marked_count = 0
    already_marked = 0
    
    for row in rows:
        title_lower = row['Title'].lower()
        
        # Check if it's an ERA meeting
        is_era = any(kw in title_lower for kw in ERA_KEYWORDS)
        
        if is_era:
            if row['Analyze'].strip():
                already_marked += 1
            else:
                row['Analyze'] = 'x'
                marked_count += 1
    
    print(f"\n✅ Marked {marked_count} new ERA meetings")
    print(f"ℹ️  {already_marked} ERA meetings already marked")
    print(f"📊 Total ERA meetings: {marked_count + already_marked}")
    
    # Show sample of what was marked
    print("\n📋 Sample of newly marked meetings:")
    sample_count = 0
    for row in rows:
        if row['Analyze'] == 'x':
            title_lower = row['Title'].lower()
            if any(kw in title_lower for kw in ERA_KEYWORDS):
                if sample_count < 5:
                    print(f"  - {row['Date']} - {row['Title']}")
                    sample_count += 1
    
    # Write back
    print(f"\n💾 Writing updated TSV...")
    with open(TSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)
    
    print("✅ TSV updated successfully")
    
    return marked_count + already_marked

if __name__ == '__main__':
    try:
        total = mark_era_meetings()
        print(f"\n{'='*60}")
        print(f"✅ SUCCESS: {total} ERA meetings marked for analysis")
        print(f"{'='*60}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
