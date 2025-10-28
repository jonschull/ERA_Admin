#!/usr/bin/env python3
"""
Identify ERA members needing bios and prioritize by Town Hall engagement.

Generates prioritized list of members without bios, with context summary.
"""

import csv
import sqlite3
from pathlib import Path
from collections import defaultdict

# Paths
SCRIPT_DIR = Path(__file__).parent
ERA_ADMIN_ROOT = SCRIPT_DIR.parent.parent
AIRTABLE_CSV = ERA_ADMIN_ROOT / "airtable" / "people_export.csv"
FATHOM_DB = ERA_ADMIN_ROOT / "FathomInventory" / "fathom_emails.db"

def load_members_without_bios():
    """Load all members from Airtable who don't have bios."""
    members = []
    
    with open(AIRTABLE_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            bio = row.get('Bio', '').strip()
            email = row.get('Email', '').strip()
            affiliated_orgs = row.get('Affiliated Orgs', '').strip()
            
            if name and not bio:
                members.append({
                    'name': name,
                    'email': email,
                    'affiliated_orgs': affiliated_orgs,
                    'airtable_row': row
                })
    
    return members

def get_townhall_context(member_name, conn):
    """Get Town Hall participation context for a member."""
    cursor = conn.cursor()
    
    # Get Town Hall meetings attended
    cursor.execute('''
        SELECT DISTINCT c.title, c.date, c.public_share_url
        FROM calls c
        JOIN participants p ON c.hyperlink = p.call_hyperlink
        WHERE p.name = ?
        AND c.title LIKE '%Town Hall%'
        ORDER BY c.date DESC
    ''', (member_name,))
    
    meetings = cursor.fetchall()
    
    return {
        'th_count': len(meetings),
        'meetings': [
            {
                'title': m[0],
                'date': m[1],
                'url': m[2]
            }
            for m in meetings
        ]
    }

def prioritize_members(members, conn):
    """Add Town Hall context and prioritize members."""
    
    for member in members:
        context = get_townhall_context(member['name'], conn)
        member['th_count'] = context['th_count']
        member['meetings'] = context['meetings']
    
    # Sort by Town Hall attendance (descending), then alphabetically
    members.sort(key=lambda x: (-x['th_count'], x['name']))
    
    return members

def generate_report(members, output_path):
    """Generate prioritized report."""
    
    with_th = [m for m in members if m['th_count'] > 0]
    without_th = [m for m in members if m['th_count'] == 0]
    
    # CSV output
    csv_path = output_path.parent / 'batch1_priority_list.csv'
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'name', 'email', 'affiliated_orgs', 'th_count', 'th_meetings', 'linkedin_url'
        ])
        writer.writeheader()
        
        for member in members:
            writer.writerow({
                'name': member['name'],
                'email': member['email'],
                'affiliated_orgs': member['affiliated_orgs'],
                'th_count': member['th_count'],
                'th_meetings': '; '.join([f"{m['date']}: {m['title']}" for m in member['meetings']]),
                'linkedin_url': ''  # To be filled by user
            })
    
    # Markdown summary
    with open(output_path, 'w') as f:
        f.write("# Members Needing Bios - Prioritized List\n\n")
        f.write(f"**Generated:** {Path(__file__).name}\n\n")
        f.write("---\n\n")
        
        f.write("## Summary\n\n")
        f.write(f"- **Total members without bios:** {len(members)}\n")
        f.write(f"- **Attended Town Halls:** {len(with_th)}\n")
        f.write(f"- **Never attended Town Halls:** {len(without_th)}\n\n")
        f.write("---\n\n")
        
        f.write("## Priority 1: Town Hall Attendees\n\n")
        f.write("These members have participated in Town Halls, so we have context to craft personalized bios.\n\n")
        
        for member in with_th:
            f.write(f"### {member['name']}\n\n")
            f.write(f"- **Email:** {member['email']}\n")
            f.write(f"- **Organizations:** {member['affiliated_orgs']}\n")
            f.write(f"- **Town Halls attended:** {member['th_count']}\n")
            
            if member['meetings']:
                f.write(f"- **Meetings:**\n")
                for meeting in member['meetings']:
                    f.write(f"  - [{meeting['date']}] {meeting['title']}\n")
                    f.write(f"    - Video: {meeting['url']}\n")
            
            f.write("\n")
        
        f.write("---\n\n")
        f.write("## Priority 2: Non-Town Hall Members\n\n")
        f.write("These members have not attended Town Halls. Bios will be based on LinkedIn + Airtable data only.\n\n")
        
        for member in without_th[:10]:  # Show first 10
            f.write(f"- **{member['name']}** - {member['email']}")
            if member['affiliated_orgs']:
                f.write(f" ({member['affiliated_orgs']})")
            f.write("\n")
        
        if len(without_th) > 10:
            f.write(f"\n... and {len(without_th) - 10} more\n")
        
        f.write("\n---\n\n")
        f.write("## Next Steps\n\n")
        f.write("1. Review `batch1_priority_list.csv`\n")
        f.write("2. Add LinkedIn URLs for Priority 1 members (Town Hall attendees)\n")
        f.write("3. Save as `batch1_linkedin_urls.csv`\n")
        f.write("4. Run `research_member_context.py` to gather context\n")
        f.write("5. Review context notes\n")
        f.write("6. Run `generate_bio_drafts.py` to create drafts\n")
        f.write("7. Review and edit drafts\n")
        f.write("8. Approve final bios\n")
        f.write("9. Run `update_airtable_bios.py` to apply\n")
        f.write("10. Manually activate 'Publish' field in Airtable when ready\n\n")

def main():
    print("=" * 70)
    print("Member Bio Identification & Prioritization")
    print("=" * 70)
    print()
    
    # Create batches directory
    batches_dir = SCRIPT_DIR / "batches"
    batches_dir.mkdir(exist_ok=True)
    
    print("📊 Loading members from Airtable...")
    members = load_members_without_bios()
    print(f"   Found {len(members)} members without bios")
    print()
    
    print("🔍 Checking Town Hall participation...")
    conn = sqlite3.connect(FATHOM_DB)
    members = prioritize_members(members, conn)
    conn.close()
    
    with_th = sum(1 for m in members if m['th_count'] > 0)
    print(f"   {with_th} attended Town Halls")
    print(f"   {len(members) - with_th} never attended Town Halls")
    print()
    
    print("📝 Generating report...")
    output_path = batches_dir / "batch1_member_analysis.md"
    generate_report(members, output_path)
    print(f"   ✅ Created: {output_path}")
    print(f"   ✅ Created: {batches_dir / 'batch1_priority_list.csv'}")
    print()
    
    print("=" * 70)
    print("✅ Analysis complete!")
    print("=" * 70)
    print()
    print("📋 Next steps:")
    print(f"   1. Review: {output_path}")
    print(f"   2. Add LinkedIn URLs to: {batches_dir / 'batch1_priority_list.csv'}")
    print(f"   3. Save as: {batches_dir / 'batch1_linkedin_urls.csv'}")
    print()

if __name__ == '__main__':
    main()
