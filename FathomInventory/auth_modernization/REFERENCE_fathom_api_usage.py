#!/usr/bin/env python3
"""
Use Fathom API to enrich the 195 remaining unenriched participants.

This is a ONE-TIME cleanup script using email matching from the API.
Much faster and more accurate than manual review.

Usage:
    export FATHOM_API_KEY="your_key_here"
    python3 api_enrich_remaining.py
"""

import os
import sys
import sqlite3
import requests
import csv
from datetime import datetime

# Config
API_KEY = os.environ.get('FATHOM_API_KEY')
DB_PATH = '../FathomInventory/fathom_emails.db'
AIRTABLE_CSV = '../airtable/people_export.csv'
API_BASE = 'https://api.fathom.ai/external/v1'

def load_airtable_people():
    """Load Airtable people with emails for matching."""
    people = {}
    with open(AIRTABLE_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row.get('Email', '').strip().lower()
            if email:
                people[email] = {
                    'name': row.get('Name', ''),
                    'is_member': row.get('ERA Member?', '').lower() == 'true',
                    'location': row.get('Location', ''),
                    'affiliation': row.get('Affiliation', ''),
                    'notes': row.get('Notes', '')
                }
    return people

def get_fathom_meetings(start_date='2025-10-17', end_date='2025-10-22'):
    """Query Fathom API for meetings in date range."""
    if not API_KEY:
        print("❌ Error: FATHOM_API_KEY environment variable not set")
        print("   Get your key from: https://fathom.video/customize")
        print("   Then: export FATHOM_API_KEY='your_key_here'")
        sys.exit(1)
    
    headers = {'X-Api-Key': API_KEY}
    params = {
        'created_after': f'{start_date}T00:00:00Z',
        'created_before': f'{end_date}T23:59:59Z',
        'limit': 100  # Max per page
    }
    
    all_meetings = []
    cursor = None
    
    while True:
        if cursor:
            params['cursor'] = cursor
        
        try:
            response = requests.get(f'{API_BASE}/meetings', headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            all_meetings.extend(data.get('items', []))
            
            cursor = data.get('next_cursor')
            if not cursor:
                break
                
            print(f"  Fetched {len(all_meetings)} meetings so far...")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            if hasattr(e.response, 'text'):
                print(f"   Response: {e.response.text}")
            sys.exit(1)
    
    return all_meetings

def extract_participants_with_emails(meetings):
    """Extract all participants with emails from meeting data."""
    participants = {}
    
    for meeting in meetings:
        meeting_title = meeting.get('meeting_title', meeting.get('title', 'Unknown'))
        invitees = meeting.get('calendar_invitees', [])
        
        for invitee in invitees:
            email = invitee.get('email', '').strip().lower()
            name = invitee.get('name', '').strip()
            
            if email and name:
                if email not in participants:
                    participants[email] = {
                        'name': name,
                        'meetings': []
                    }
                participants[email]['meetings'].append(meeting_title)
    
    return participants

def get_unenriched_participants(conn):
    """Get the 195 participants that still need enrichment."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, email, source_call_title, source_call_url
        FROM participants 
        WHERE validated_by_airtable = 0
        ORDER BY name
    """)
    
    return [
        {
            'id': row[0],
            'name': row[1],
            'email': row[2] or '',
            'meeting': row[3],
            'url': row[4]
        }
        for row in cursor.fetchall()
    ]

def match_and_enrich(unenriched, api_participants, airtable_people):
    """Match unenriched participants via email and enrich from Airtable."""
    
    matches = []
    partial_matches = []
    no_match = []
    
    for person in unenriched:
        db_email = person['email'].strip().lower()
        db_name = person['name']
        
        # Try email match from API
        if db_email and db_email in api_participants:
            api_name = api_participants[db_email]['name']
            
            # Check if email in Airtable
            if db_email in airtable_people:
                airtable_data = airtable_people[db_email]
                matches.append({
                    'db_id': person['id'],
                    'db_name': db_name,
                    'api_name': api_name,
                    'email': db_email,
                    'airtable_data': airtable_data,
                    'confidence': 'HIGH - email match'
                })
            else:
                partial_matches.append({
                    'db_id': person['id'],
                    'db_name': db_name,
                    'api_name': api_name,
                    'email': db_email,
                    'confidence': 'MEDIUM - email in API, not in Airtable'
                })
        else:
            no_match.append({
                'db_id': person['id'],
                'db_name': db_name,
                'email': db_email or 'NO EMAIL',
                'meeting': person['meeting']
            })
    
    return matches, partial_matches, no_match

def apply_enrichments(conn, matches, dry_run=True):
    """Apply enrichments to database."""
    cursor = conn.cursor()
    
    for match in matches:
        airtable = match['airtable_data']
        
        if dry_run:
            print(f"  Would enrich: {match['db_name']} → {airtable['name']}")
            print(f"    Email: {match['email']}")
            print(f"    Member: {airtable['is_member']}, Location: {airtable['location']}")
        else:
            cursor.execute("""
                UPDATE participants
                SET 
                    email = ?,
                    location = ?,
                    affiliation = ?,
                    era_member = ?,
                    validated_by_airtable = 1
                WHERE id = ?
            """, (
                match['email'],
                airtable['location'],
                airtable['affiliation'],
                1 if airtable['is_member'] else 0,
                match['db_id']
            ))
    
    if not dry_run:
        conn.commit()
        print(f"✅ Enriched {len(matches)} participants")

def main():
    print("=" * 80)
    print("FATHOM API ENRICHMENT - One-Time Cleanup")
    print("=" * 80)
    print()
    
    # Load Airtable data
    print("📊 Loading Airtable people...")
    airtable_people = load_airtable_people()
    print(f"   Loaded {len(airtable_people)} people with emails")
    print()
    
    # Query Fathom API
    print("🔍 Querying Fathom API for recent meetings...")
    meetings = get_fathom_meetings()
    print(f"   Found {len(meetings)} meetings")
    print()
    
    # Extract participants
    print("👥 Extracting participants with emails from API...")
    api_participants = extract_participants_with_emails(meetings)
    print(f"   Found {len(api_participants)} unique participants with emails")
    print()
    
    # Get unenriched from database
    print("📂 Loading unenriched participants from database...")
    conn = sqlite3.connect(DB_PATH)
    unenriched = get_unenriched_participants(conn)
    print(f"   Found {len(unenriched)} unenriched participants")
    print()
    
    # Match and categorize
    print("🔗 Matching participants...")
    matches, partial, no_match = match_and_enrich(unenriched, api_participants, airtable_people)
    print()
    
    # Report
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()
    print(f"✅ HIGH CONFIDENCE (email match to Airtable): {len(matches)}")
    print(f"⚠️  MEDIUM (email in API, not Airtable): {len(partial)}")
    print(f"❌ NO MATCH (no email or not in API): {len(no_match)}")
    print()
    
    if matches:
        print("\n✅ HIGH CONFIDENCE MATCHES (ready to auto-enrich):")
        for match in matches[:10]:
            print(f"  • {match['db_name']} → {match['email']}")
        if len(matches) > 10:
            print(f"  ... and {len(matches) - 10} more")
    
    if no_match:
        print(f"\n❌ STILL NEED MANUAL REVIEW ({len(no_match)} people):")
        for person in no_match[:10]:
            print(f"  • {person['db_name']} ({person['email']})")
        if len(no_match) > 10:
            print(f"  ... and {len(no_match) - 10} more")
    
    print()
    print("=" * 80)
    print(f"SUMMARY: Can auto-enrich {len(matches)}/{len(unenriched)} ({len(matches)*100//len(unenriched)}%)")
    print(f"         Manual review needed: {len(no_match)} ({len(no_match)*100//len(unenriched)}%)")
    print("=" * 80)
    print()
    
    # Dry run by default
    print("💡 This was a DRY RUN - no changes made to database")
    print("   To apply enrichments: python3 api_enrich_remaining.py --apply")
    print()
    
    conn.close()

if __name__ == '__main__':
    main()
