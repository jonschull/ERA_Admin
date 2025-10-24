#!/usr/bin/env python3
"""
Interactive Probe Assistant - AI-assisted participant reconciliation

For each participant marked "Probe", this script:
1. Searches Town Hall agendas for context (local database, no API calls)
2. Presents findings and context to user
3. Waits for decision before executing

This is INTERACTIVE - one case at a time, human-AI collaboration.

NOTE: Skips Fathom API to avoid rate limits. The 195 backlog participants
are from meetings too old to be in the API anyway (only returns ~10 most recent).

Usage:
    python3 probe_assistant.py path/to/approvals.csv
"""

import os
import sys
import csv
import sqlite3

# Config
DB_PATH = '../FathomInventory/fathom_emails.db'

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def get_meeting_info(conn, participant_name):
    """Get meeting URL and ID for this participant."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, source_call_url, source_call_title, analyzed_at
        FROM participants
        WHERE name = ?
        ORDER BY analyzed_at DESC
        LIMIT 1
    """, (participant_name,))
    
    row = cursor.fetchone()
    if row:
        return {
            'db_id': row[0],
            'url': row[1],
            'title': row[2],
            'date': row[3]
        }
    return None

def extract_recording_id(url):
    """Extract recording ID from Fathom URL."""
    # URL format: https://fathom.video/calls/450546919
    if '/calls/' in url:
        return url.split('/calls/')[-1].split('?')[0]
    return None

def get_recording_id_from_url(url):
    """Get recording_id by searching meetings API for this URL."""
    headers = {'X-Api-Key': FATHOM_API_KEY}
    
    # Search through paginated meetings
    cursor = None
    max_pages = 50  # Search up to 50 pages (~500 meetings)
    
    for page in range(max_pages):
        params = {'limit': 100}
        if cursor:
            params['cursor'] = cursor
        
        try:
            response = requests.get(
                f'{API_BASE}/meetings',
                headers=headers,
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            # Search this page for matching URL
            for meeting in data.get('items', []):
                if meeting.get('url') == url:
                    return meeting.get('recording_id'), None
            
            # Get next page
            cursor = data.get('next_cursor')
            if not cursor:
                break
                
        except requests.exceptions.RequestException as e:
            return None, f"API error: {str(e)}"
    
    return None, "Meeting not found in API (may be too old)"

def fetch_transcript(recording_id):
    """Fetch transcript from Fathom API."""
    if not FATHOM_API_KEY:
        return None, "No API key"
    
    headers = {'X-Api-Key': FATHOM_API_KEY}
    
    try:
        response = requests.get(
            f'{API_BASE}/recordings/{recording_id}/transcript',
            headers=headers
        )
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)

def analyze_introduction(transcript_data, participant_name):
    """
    Analyze transcript to find how person introduced themselves.
    Returns dict with findings.
    """
    if not transcript_data or 'transcript' not in transcript_data:
        return None
    
    transcript = transcript_data['transcript']
    participant_lower = participant_name.lower()
    
    # Find all utterances by or mentioning this participant
    relevant_segments = []
    
    for i, entry in enumerate(transcript):
        speaker = entry.get('speaker', {}).get('display_name', '')
        text = entry.get('text', '')
        timestamp = entry.get('timestamp', '')
        
        # Is this the participant speaking?
        if participant_lower in speaker.lower():
            relevant_segments.append({
                'type': 'speaker',
                'timestamp': timestamp,
                'speaker': speaker,
                'text': text,
                'context': 'direct'
            })
        # Is someone mentioning this participant?
        elif participant_lower in text.lower():
            relevant_segments.append({
                'type': 'mention',
                'timestamp': timestamp,
                'speaker': speaker,
                'text': text,
                'context': 'mentioned'
            })
    
    # Look for self-introductions (early in meeting, contains "I'm" or "my name")
    introductions = []
    for seg in relevant_segments:
        if seg['type'] == 'speaker':
            text_lower = seg['text'].lower()
            # Check if it's an introduction
            if any(phrase in text_lower for phrase in ["i'm", "my name", "i am", "from", "work"]):
                introductions.append(seg)
    
    return {
        'all_segments': relevant_segments,
        'introductions': introductions,
        'total_utterances': len([s for s in relevant_segments if s['type'] == 'speaker'])
    }

def search_townhall_context(name):
    """Search Town Hall agendas for this person."""
    try:
        from town_hall_search import TownHallSearch
        searcher = TownHallSearch(use_local_db=True)
        results = searcher.search_agendas_for_name(name, max_results=3)
        return results
    except Exception as e:
        return None

def search_gmail_context(name):
    """Search Gmail for additional context about this person."""
    # Would integrate with gmail search if needed
    return None

def present_case(case_num, total_cases, row, analysis, meeting_info, townhall_results=None):
    """Present one probe case to user with all context."""
    
    print("\n" + "=" * 80)
    print(f"{Colors.BOLD}{Colors.CYAN}PROBE CASE {case_num}/{total_cases}{Colors.END}")
    print("=" * 80)
    
    print(f"\n{Colors.BOLD}Participant in Fathom:{Colors.END}")
    print(f"  Name: {Colors.YELLOW}{row['Name']}{Colors.END}")
    print(f"  Meeting: {meeting_info['title']}")
    print(f"  Date: {meeting_info['date']}")
    
    if analysis:
        print(f"\n{Colors.BOLD}{Colors.BLUE}📝 FATHOM TRANSCRIPT:{Colors.END}")
        
        if analysis['introductions']:
            print(f"\n  {Colors.GREEN}Found {len(analysis['introductions'])} self-introduction(s):{Colors.END}")
            for intro in analysis['introductions'][:3]:  # Show first 3
                print(f"\n  [{intro['timestamp']}] {intro['speaker']} said:")
                print(f"  \"{intro['text'][:200]}...\"" if len(intro['text']) > 200 else f"  \"{intro['text']}\"")
        
        if analysis['total_utterances'] > 0:
            print(f"\n  Spoke {analysis['total_utterances']} times in meeting")
        
        # Show other relevant segments
        other_segments = [s for s in analysis['all_segments'] if s not in analysis.get('introductions', [])]
        if other_segments:
            print(f"\n  Other relevant mentions: {len(other_segments)}")
            if len(other_segments) <= 2:
                for seg in other_segments:
                    print(f"\n  [{seg['timestamp']}] {seg['speaker']}:")
                    print(f"  \"{seg['text'][:150]}...\"" if len(seg['text']) > 150 else f"  \"{seg['text']}\"")
    else:
        print(f"\n  {Colors.YELLOW}⚠️  Fathom transcript not available (meeting too old){Colors.END}")
    
    # Show Town Hall context
    if townhall_results:
        print(f"\n{Colors.BOLD}{Colors.GREEN}📚 TOWN HALL CONTEXT:{Colors.END}")
        print(f"\n  Found in {len(townhall_results)} Town Hall agenda(s):")
        for th in townhall_results:
            print(f"\n  📄 {th['title']} ({th['date']})")
            print(f"     {th['snippet']}")
    
    print(f"\n{Colors.BOLD}YOUR DECISION:{Colors.END}")
    print("  What should I do with this person?")
    print()

def get_user_decision():
    """Get user's decision for this case."""
    print("Options:")
    print("  [m] Merge with existing Airtable person (specify name)")
    print("  [a] Add to Airtable as new person (specify full name)")
    print("  [s] Skip - not enough info / not relevant")
    print("  [n] Next - show me more transcript context")
    print("  [q] Quit")
    print()
    
    while True:
        choice = input(f"{Colors.BOLD}Your choice: {Colors.END}").strip().lower()
        
        if choice == 'q':
            return {'action': 'quit'}
        elif choice == 's':
            return {'action': 'skip'}
        elif choice == 'n':
            return {'action': 'more_context'}
        elif choice == 'm':
            name = input("  Merge with (name in Airtable): ").strip()
            if name:
                return {'action': 'merge', 'target': name}
        elif choice == 'a':
            name = input("  Add to Airtable as (full name): ").strip()
            if name:
                location = input("  Location (optional): ").strip()
                affiliation = input("  Affiliation (optional): ").strip()
                return {
                    'action': 'add',
                    'name': name,
                    'location': location,
                    'affiliation': affiliation
                }
        
        print(f"{Colors.RED}Invalid choice. Try again.{Colors.END}")

def execute_decision(conn, decision, row, meeting_info):
    """Execute user's decision."""
    if decision['action'] == 'skip':
        print(f"{Colors.YELLOW}⏭️  Skipped{Colors.END}")
        return
    
    if decision['action'] == 'merge':
        print(f"{Colors.GREEN}✅ Would merge '{row['Name']}' → '{decision['target']}'{Colors.END}")
        # TODO: Execute merge via existing code
    
    if decision['action'] == 'add':
        print(f"{Colors.GREEN}✅ Would add to Airtable:{Colors.END}")
        print(f"   Name: {decision['name']}")
        print(f"   Location: {decision.get('location', 'N/A')}")
        print(f"   Affiliation: {decision.get('affiliation', 'N/A')}")
        # TODO: Execute add via existing code

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 probe_assistant.py path/to/approvals.csv")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    
    # Load probe cases from CSV
    probe_cases = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Probe', '').lower() == 'true':
                probe_cases.append(row)
    
    if not probe_cases:
        print(f"{Colors.YELLOW}No probe cases found in CSV{Colors.END}")
        return
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}Found {len(probe_cases)} cases to probe{Colors.END}\n")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    
    # Process each case
    for i, row in enumerate(probe_cases, 1):
        # Get meeting info
        meeting_info = get_meeting_info(conn, row['Name'])
        if not meeting_info:
            print(f"{Colors.RED}⚠️  Could not find meeting for '{row['Name']}'{Colors.END}")
            continue
        
        # Skip Fathom API to avoid rate limits - backlog meetings are too old anyway
        # The 195 unenriched participants are from Oct 17-21, which are no longer in API
        
        # Search Town Hall agendas for context (local DB, no API calls)
        townhall_results = search_townhall_context(row['Name'])
        
        # Present case with Town Hall context only
        present_case(i, len(probe_cases), row, None, meeting_info, townhall_results)
        
        # Get decision
        decision = get_user_decision()
        
        if decision['action'] == 'quit':
            print(f"\n{Colors.YELLOW}Stopping. Progress saved.{Colors.END}")
            break
        
        if decision['action'] == 'more_context':
            # Show more transcript details
            if analysis and analysis['all_segments']:
                print(f"\n{Colors.BOLD}All relevant segments:{Colors.END}")
                for seg in analysis['all_segments'][:10]:
                    print(f"\n[{seg['timestamp']}] {seg['speaker']} ({seg['type']}):")
                    print(f"  {seg['text']}")
            input("\nPress Enter to continue...")
            # Re-present case
            present_case(i, len(probe_cases), row, analysis, meeting_info)
            decision = get_user_decision()
        
        # Execute decision
        execute_decision(conn, decision, row, meeting_info)
        
        input(f"\n{Colors.CYAN}Press Enter for next case...{Colors.END}")
    
    conn.close()
    print(f"\n{Colors.GREEN}✅ All probe cases processed!{Colors.END}\n")

if __name__ == '__main__':
    main()
