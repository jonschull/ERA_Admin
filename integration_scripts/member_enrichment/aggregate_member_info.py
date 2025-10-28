#!/usr/bin/env python3
"""
Aggregate all available information about a member from multiple sources.

This is a COLLECTION tool (mechanical) - no judgment, just gather facts.
"""

import csv
import sqlite3
import json
import sys
from pathlib import Path
from fuzzywuzzy import fuzz

# Paths
SCRIPT_DIR = Path(__file__).parent
ERA_ADMIN_ROOT = SCRIPT_DIR.parent.parent
AIRTABLE_CSV = ERA_ADMIN_ROOT / "airtable" / "people_export.csv"
FATHOM_DB = ERA_ADMIN_ROOT / "FathomInventory" / "fathom_emails.db"
TH_TRANSCRIPTS = ERA_ADMIN_ROOT / "fathom" / "output" / "era_townhalls_complete.md"
LINKEDIN_CSV = Path("/Users/admin/Downloads/Linkedin/Complete_LinkedInDataExport_07-07-2025.zip (1)/Connections.csv")
GOOGLE_CONTACTS = SCRIPT_DIR / "google_contacts.csv"

def load_linkedin_connections():
    """Load LinkedIn connections export."""
    connections = {}
    with open(LINKEDIN_CSV, 'r') as f:
        # Skip first 3 lines (notes)
        for _ in range(3):
            next(f)
        
        reader = csv.DictReader(f)
        for row in reader:
            first = row.get('First Name', '').strip()
            last = row.get('Last Name', '').strip()
            if first and last:
                full_name = f'{first} {last}'
                connections[full_name] = {
                    'url': row.get('URL', '').strip(),
                    'email': row.get('Email Address', '').strip(),
                    'company': row.get('Company', '').strip(),
                    'position': row.get('Position', '').strip(),
                    'connected_on': row.get('Connected On', '').strip()
                }
    return connections

def load_google_contacts():
    """Load Google Contacts export for phone numbers."""
    contacts = {}
    if not GOOGLE_CONTACTS.exists():
        return contacts
    
    with open(GOOGLE_CONTACTS, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            first = row.get('First Name', '').strip()
            last = row.get('Last Name', '').strip()
            if first and last:
                full_name = f'{first} {last}'
                
                # Get all phone numbers
                phones = []
                for i in range(1, 6):
                    phone = row.get(f'Phone {i} - Value', '').strip()
                    phone_label = row.get(f'Phone {i} - Label', '').strip()
                    if phone:
                        phones.append({'label': phone_label, 'number': phone})
                
                if phones:
                    contacts[full_name.lower()] = {
                        'name': full_name,
                        'phones': phones
                    }
    return contacts

def get_database_info(name, conn):
    """Get member info from Fathom database."""
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, location, affiliation, email, era_member, is_donor, 
               era_africa, airtable_id, projects
        FROM participants
        WHERE name = ?
    ''', (name,))
    
    row = cursor.fetchone()
    if not row:
        return None
    
    # Get ALL calls (not just Town Halls)
    cursor.execute('''
        SELECT DISTINCT c.title, c.date, c.duration, c.public_share_url, c.hyperlink
        FROM calls c
        JOIN participants p ON c.hyperlink = p.call_hyperlink
        WHERE p.name = ?
        ORDER BY c.date DESC
    ''', (name,))
    
    all_calls = cursor.fetchall()
    
    # Categorize calls and get summaries
    town_halls = []
    other_calls = []
    
    for title, date, duration, url, hyperlink in all_calls:
        # Get summary from emails table
        cursor.execute('''
            SELECT body_md
            FROM emails
            WHERE meeting_url = ?
            LIMIT 1
        ''', (url,))
        
        summary_row = cursor.fetchone()
        summary = summary_row[0] if summary_row else None
        
        call_data = {
            'title': title,
            'date': date,
            'duration': duration,
            'url': url,
            'summary': summary,
            'summary_length': len(summary) if summary else 0
        }
        
        if 'Town Hall' in title:
            town_halls.append(call_data)
        else:
            other_calls.append(call_data)
    
    return {
        'name': row[0],
        'location': row[1],
        'affiliation': row[2],
        'email': row[3],
        'era_member': bool(row[4]),
        'is_donor': bool(row[5]),
        'era_africa': bool(row[6]),
        'airtable_id': row[7],
        'projects': row[8],
        'town_halls': town_halls,
        'other_calls': other_calls,
        'total_calls': len(all_calls)
    }

def get_airtable_info(name):
    """Get member info from Airtable export."""
    with open(AIRTABLE_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Name', '').strip() == name:
                return {
                    'name': row.get('Name', '').strip(),
                    'email': row.get('Email', '').strip(),
                    'phone': row.get('Phone', '').strip(),
                    'bio': row.get('Bio', '').strip(),
                    'affiliated_orgs': row.get('Affiliated Orgs', '').strip(),
                    'publish': row.get('Publish', '').strip(),
                }
    return None

def search_transcripts(name, transcript_path):
    """Search Town Hall transcripts for mentions of this person.
    
    Captures FULL speaker turns, not just lines around name.
    People can speak multiple times - capture each turn separately.
    """
    if not transcript_path.exists():
        return []
    
    mentions = []
    with open(transcript_path, 'r') as f:
        content = f.read()
        
        # Split into meetings (assuming markdown structure)
        lines = content.split('\n')
        current_meeting = None
        
        for i, line in enumerate(lines):
            # Detect meeting headers (adjust based on actual format)
            if 'ERA Town Hall' in line and line.startswith('#'):
                current_meeting = line.strip('#').strip()
            
            # Check if this is a speaking turn by this person
            # Pattern: "8:24 - Mary Minton" or "[00:14:00] Jacob Denlinger"
            is_speaker_line = False
            if ' - ' in line and name.lower() in line.lower():
                # Check if name appears after timestamp pattern
                parts = line.split(' - ', 1)
                if len(parts) == 2 and name.lower() in parts[1].lower():
                    is_speaker_line = True
            elif name.lower() in line.lower() and any(c.isdigit() for c in line[:20]):
                # Bracket timestamp format like "[00:14:00] Name"
                is_speaker_line = True
            
            if is_speaker_line:
                # Capture FULL speaking turn (from this line until next timestamp)
                speaker_lines = [line]
                j = i + 1
                
                # Keep going until we hit another timestamp or end
                while j < len(lines):
                    next_line = lines[j]
                    
                    # Stop if we hit another timestamp (new speaker)
                    if (' - ' in next_line and any(c.isdigit() for c in next_line[:20])) or \
                       (next_line.startswith('[') and ':' in next_line[:20]):
                        break
                    
                    # Stop if we hit section header
                    if next_line.startswith('#'):
                        break
                    
                    speaker_lines.append(next_line)
                    j += 1
                
                # Also include a few lines BEFORE for context (who asked them to speak)
                context_before = []
                k = max(0, i - 3)
                while k < i:
                    context_before.append(lines[k])
                    k += 1
                
                full_context = '\n'.join(context_before + speaker_lines)
                
                mentions.append({
                    'meeting': current_meeting or 'Unknown meeting',
                    'line_number': i + 1,
                    'context': full_context,
                    'is_speaker': True
                })
    
    return mentions

def find_linkedin_matches(name, linkedin_connections):
    """Find LinkedIn matches (exact and fuzzy)."""
    matches = []
    
    # Exact match
    if name in linkedin_connections:
        matches.append({
            'type': 'exact',
            'score': 100,
            'linkedin_name': name,
            'data': linkedin_connections[name]
        })
    else:
        # Fuzzy matching
        for linkedin_name, data in linkedin_connections.items():
            score = fuzz.ratio(name.lower(), linkedin_name.lower())
            if score >= 75:  # Include medium-confidence matches
                matches.append({
                    'type': 'fuzzy',
                    'score': score,
                    'linkedin_name': linkedin_name,
                    'data': data
                })
    
    # Sort by score
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches[:5]  # Top 5 matches

def aggregate_member_info(name):
    """Aggregate all available information about a member."""
    
    print(f"Aggregating information for: {name}")
    print("=" * 80)
    
    # Load LinkedIn connections
    print("Loading LinkedIn connections...")
    linkedin = load_linkedin_connections()
    
    # Load Google Contacts
    print("Loading Google Contacts...")
    google_contacts = load_google_contacts()
    
    # Connect to database
    print("Querying Fathom database...")
    conn = sqlite3.connect(FATHOM_DB)
    db_info = get_database_info(name, conn)
    conn.close()
    
    # Get Airtable info
    print("Checking Airtable...")
    at_info = get_airtable_info(name)
    
    # Search transcripts
    print("Searching Town Hall transcripts...")
    transcript_mentions = search_transcripts(name, TH_TRANSCRIPTS)
    
    # Find LinkedIn matches
    print("Finding LinkedIn matches...")
    linkedin_matches = find_linkedin_matches(name, linkedin)
    
    # Check for phone numbers in Google Contacts
    print("Checking Google Contacts for phone...")
    phone_info = google_contacts.get(name.lower())
    
    print()
    
    # Compile results
    result = {
        'name': name,
        'database': db_info,
        'airtable': at_info,
        'linkedin_matches': linkedin_matches,
        'transcript_mentions': transcript_mentions,
        'phone_info': phone_info,
        'sources_found': {
            'database': db_info is not None,
            'airtable': at_info is not None,
            'linkedin': len(linkedin_matches) > 0,
            'transcripts': len(transcript_mentions) > 0,
            'phone': phone_info is not None
        }
    }
    
    return result

def format_report(data):
    """Format aggregated data as readable report."""
    report = []
    report.append(f"# MEMBER INFORMATION AGGREGATION")
    report.append(f"## {data['name']}")
    report.append("")
    report.append("=" * 80)
    report.append("")
    
    # Database info
    report.append("## SOURCE 1: FATHOM DATABASE")
    report.append("")
    if data['database']:
        db = data['database']
        report.append(f"- **Name:** {db['name']}")
        report.append(f"- **Location:** {db['location'] or '(none)'}")
        report.append(f"- **Affiliation:** {db['affiliation'] or '(none)'}")
        report.append(f"- **Email:** {db['email'] or '(none)'}")
        report.append(f"- **ERA Member:** {'Yes' if db['era_member'] else 'No'}")
        report.append(f"- **Donor:** {'Yes' if db['is_donor'] else 'No'}")
        report.append(f"- **ERA Africa:** {'Yes' if db['era_africa'] else 'No'}")
        report.append(f"- **Airtable ID:** {db['airtable_id'] or '(none)'}")
        report.append(f"- **Total Calls:** {db['total_calls']}")
        report.append("")
        
        if db['town_halls']:
            report.append(f"### Town Hall Meetings ({len(db['town_halls'])})")
            report.append("")
            for i, th in enumerate(db['town_halls'], 1):
                report.append(f"**{i}. [{th['date']}] {th['title']}** ({th['duration']})")
                report.append(f"- Video: {th['url']}")
                if th['summary']:
                    report.append(f"- Summary: {th['summary_length']} chars")
                    report.append("")
                    report.append("<details>")
                    report.append(f"<summary>View Fathom Summary</summary>")
                    report.append("")
                    report.append("```")
                    report.append(th['summary'][:2000])  # First 2000 chars
                    if th['summary_length'] > 2000:
                        report.append(f"\n... ({th['summary_length'] - 2000} more chars)")
                    report.append("```")
                    report.append("")
                    report.append("</details>")
                else:
                    report.append(f"- Summary: Not available")
                report.append("")
        
        if db['other_calls']:
            report.append(f"### Other Calls ({len(db['other_calls'])})")
            report.append("")
            for i, call in enumerate(db['other_calls'], 1):
                report.append(f"**{i}. [{call['date']}] {call['title']}** ({call['duration']})")
                report.append(f"- Video: {call['url']}")
                if call['summary']:
                    report.append(f"- Summary: {call['summary_length']} chars")
                    report.append("")
                    report.append("<details>")
                    report.append(f"<summary>View Fathom Summary</summary>")
                    report.append("")
                    report.append("```")
                    report.append(call['summary'][:2000])  # First 2000 chars
                    if call['summary_length'] > 2000:
                        report.append(f"\n... ({call['summary_length'] - 2000} more chars)")
                    report.append("```")
                    report.append("")
                    report.append("</details>")
                else:
                    report.append(f"- Summary: Not available")
                report.append("")
    else:
        report.append("*Not found in database*")
        report.append("")
    
    # Airtable info
    report.append("## SOURCE 2: AIRTABLE")
    report.append("")
    if data['airtable']:
        at = data['airtable']
        report.append(f"- **Email:** {at['email'] or '(none)'}")
        report.append(f"- **Phone:** {at['phone'] or '(none)'}")
        report.append(f"- **Bio:** {'YES (' + str(len(at['bio'])) + ' chars)' if at['bio'] else 'NO'}")
        report.append(f"- **Affiliated Orgs:** {at['affiliated_orgs'] or '(none)'}")
        report.append(f"- **Published:** {at['publish'] or 'No'}")
        report.append("")
    else:
        report.append("*Not found in Airtable*")
        report.append("")
    
    # LinkedIn matches
    report.append("## SOURCE 3: LINKEDIN CONNECTIONS")
    report.append("")
    if data['linkedin_matches']:
        for i, match in enumerate(data['linkedin_matches'], 1):
            report.append(f"### Match {i}: {match['linkedin_name']} ({match['score']}% - {match['type'].upper()})")
            report.append(f"- **Position:** {match['data']['position']}")
            report.append(f"- **Company:** {match['data']['company']}")
            report.append(f"- **Email:** {match['data']['email'] or '(not shared)'}")
            report.append(f"- **URL:** {match['data']['url']}")
            report.append(f"- **Connected:** {match['data']['connected_on']}")
            report.append("")
    else:
        report.append("*No matches found in LinkedIn connections*")
        report.append("")
    
    # Transcript mentions
    report.append("## SOURCE 4: TOWN HALL TRANSCRIPTS")
    report.append("")
    if data['transcript_mentions']:
        report.append(f"**Found {len(data['transcript_mentions'])} mentions:**")
        report.append("")
        for i, mention in enumerate(data['transcript_mentions'][:10], 1):  # Show first 10
            report.append(f"### Mention {i}: {mention['meeting']}")
            report.append(f"*Line {mention['line_number']}:*")
            report.append("```")
            report.append(mention['context'])
            report.append("```")
            report.append("")
        
        if len(data['transcript_mentions']) > 10:
            report.append(f"*... and {len(data['transcript_mentions']) - 10} more mentions*")
            report.append("")
    else:
        report.append("*No mentions found in transcripts*")
        report.append("")
    
    # Phone info
    report.append("## SOURCE 5: GOOGLE CONTACTS")
    report.append("")
    if data['phone_info']:
        phone_data = data['phone_info']
        report.append(f"**Found {len(phone_data['phones'])} phone number(s):**")
        report.append("")
        for phone in phone_data['phones']:
            label = phone['label'] if phone['label'] else 'Phone'
            report.append(f"- **{label}:** {phone['number']}")
        report.append("")
    else:
        report.append("*No phone numbers found in Google Contacts*")
        report.append("")
    
    # Summary
    report.append("=" * 80)
    report.append("## SOURCES SUMMARY")
    report.append("")
    sources = data['sources_found']
    report.append(f"- Database: {'✅' if sources['database'] else '❌'}")
    report.append(f"- Airtable: {'✅' if sources['airtable'] else '❌'}")
    report.append(f"- LinkedIn: {'✅' if sources['linkedin'] else '❌'}")
    report.append(f"- Transcripts: {'✅' if sources['transcripts'] else '❌'}")
    report.append(f"- Phone: {'✅' if sources['phone'] else '❌'}")
    report.append("")
    
    return '\n'.join(report)

def main(member_names, batch_number=None):
    """Aggregate information for one or more members."""
    
    if isinstance(member_names, str):
        member_names = [member_names]
    
    all_data = []
    
    for member_name in member_names:
        data = aggregate_member_info(member_name)
        all_data.append(data)
        
        # Save individual JSON
        output_dir = SCRIPT_DIR / "batches" / "aggregated_data"
        output_dir.mkdir(exist_ok=True, parents=True)
        
        json_path = output_dir / f"{member_name.replace(' ', '_').lower()}.json"
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Saved JSON: {json_path}")
    
    # If batch mode, create combined report
    if batch_number is not None:
        print()
        print(f"📦 Creating batch{batch_number}.md...")
        batch_report = []
        batch_report.append(f"# BATCH {batch_number} - Member Bio Review")
        batch_report.append("")
        batch_report.append(f"**Date:** {__import__('datetime').datetime.now().strftime('%B %d, %Y')}")
        batch_report.append(f"**Members:** {len(all_data)}")
        batch_report.append("")
        batch_report.append("=" * 80)
        batch_report.append("")
        
        for i, data in enumerate(all_data, 1):
            if i > 1:
                batch_report.append("")
                batch_report.append("=" * 80)
                batch_report.append("=" * 80)
                batch_report.append("")
            
            # Get the individual report
            report = format_report(data)
            batch_report.append(report)
        
        batch_path = SCRIPT_DIR / "batches" / f"batch{batch_number}.md"
        with open(batch_path, 'w') as f:
            f.write('\n'.join(batch_report))
        print(f"✅ Saved batch report: {batch_path}")
    else:
        # Single member - save individual report
        for data in all_data:
            report = format_report(data)
            md_path = output_dir / f"{data['name'].replace(' ', '_').lower()}.md"
            with open(md_path, 'w') as f:
                f.write(report)
            print(f"✅ Saved report: {md_path}")
    
    print()
    print("Review the report, then provide intelligent assessment.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python aggregate_member_info.py 'Member Name' ['Member 2' ...] [--batch N]")
        sys.exit(1)
    
    # Parse arguments
    args = sys.argv[1:]
    batch_number = None
    member_names = []
    
    i = 0
    while i < len(args):
        if args[i] == '--batch' and i + 1 < len(args):
            batch_number = args[i + 1]
            i += 2
        else:
            member_names.append(args[i])
            i += 1
    
    if not member_names:
        print("Error: No member names provided")
        sys.exit(1)
    
    main(member_names, batch_number)
