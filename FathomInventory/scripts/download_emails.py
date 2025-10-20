import os
import sys
import sqlite3
import base64
import email
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Import the conversion function
sys.path.append('email_conversion')
from fathom_email_2_md import convert_html_to_markdown

# --- Configuration ---
# IMPORTANT: Both readonly and send scopes needed for full system operation
# - readonly: For downloading emails
# - send: For sending daily reports (used by send_daily_report.py)
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]
DB_FILE = 'fathom_emails.db'

def get_gmail_service():
    """Authenticates with the Gmail API and returns a service object."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def setup_database():
    """Sets up the SQLite database and the emails table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            message_id TEXT PRIMARY KEY,
            thread_id TEXT,
            date TEXT,
            subject TEXT,
            body_html TEXT,
            body_md TEXT
        )
    ''')
    conn.commit()
    return conn

def get_existing_message_ids(conn):
    """Gets a set of all message IDs already in the database."""
    cursor = conn.cursor()
    cursor.execute('SELECT message_id FROM emails')
    return {row[0] for row in cursor.fetchall()}

def main():
    """Main function to download emails and store them in the database."""
    print("📧 FATHOM EMAIL DOWNLOAD STARTING")
    print("=" * 50)
    print("🔍 Searching for new Fathom summary emails...")
    print("")
    
    conn = setup_database()
    service = get_gmail_service()
    if not service:
        print("Failed to connect to Gmail API.")
        conn.close()
        return
    
    # CRITICAL: Verify we're using the correct Gmail account
    try:
        profile = service.users().getProfile(userId='me').execute()
        current_email = profile['emailAddress']
        expected_email = 'fathomizer@ecorestorationalliance.org'
        
        print(f"📧 Authenticated as: {current_email}")
        
        if current_email != expected_email:
            print(f"❌ ERROR: Wrong Gmail account!")
            print(f"   Current:  {current_email}")
            print(f"   Expected: {expected_email}")
            print(f"")
            print(f"   To fix: Delete token.json and re-authenticate")
            print(f"   Command: rm token.json && python scripts/download_emails.py")
            conn.close()
            sys.exit(1)
        
        print(f"✅ Correct account verified")
        print("")
    except HttpError as error:
        print(f"❌ Failed to verify account: {error}")
        conn.close()
        sys.exit(1)

    existing_ids = get_existing_message_ids(conn)
    print(f"Found {len(existing_ids)} emails already in the local database.")

    # Fetch all message IDs from Gmail
    print("Fetching all email message IDs from Gmail...")
    query = 'from:("no-reply@fathom.video")'
    response = service.users().messages().list(userId='me', q=query).execute()
    all_message_refs = response.get('messages', [])
    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        all_message_refs.extend(response.get('messages', []))
    
    print(f"Found a total of {len(all_message_refs)} emails in the inbox.")

    # Filter out messages that are already downloaded
    new_message_refs = [m for m in all_message_refs if m['id'] not in existing_ids]
    if not new_message_refs:
        print("No new emails to download. Database is up to date.")
        conn.close()
        return

    print(f"Downloading {len(new_message_refs)} new emails...")
    cursor = conn.cursor()
    for i, msg_ref in enumerate(new_message_refs):
        msg_id = msg_ref['id']
        print(f"  - Downloading message {i+1}/{len(new_message_refs)} (ID: {msg_id})", end='\r')
        
        try:
            message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            thread_id = message['threadId']
            headers = {h['name']: h['value'] for h in message['payload']['headers']}
            subject = headers.get('Subject', '')
            date = headers.get('Date', '')
            
            # Decode the body
            if 'parts' in message['payload']:
                part = message['payload']['parts'][0]
                if 'data' in part['body']:
                    body_data = part['body']['data']
                    body_html = base64.urlsafe_b64decode(body_data).decode('utf-8')
                else:
                    body_html = ""
            else:
                 body_data = message['payload']['body']['data']
                 body_html = base64.urlsafe_b64decode(body_data).decode('utf-8')

            # Convert HTML to Markdown and extract metadata
            try:
                markdown_result, stats = convert_html_to_markdown(body_html, extract_stats=True)
                markdown_result = markdown_result.replace('×tamp=', '&timestamp=')
            except Exception as e:
                print(f"\nWarning: Conversion failed for {msg_id}: {e}")
                markdown_result = f"# Conversion Error\n\n{str(e)}"
                stats = {}

            # Insert email with metadata extracted from HTML
            cursor.execute('''
                INSERT INTO emails (
                    message_id, thread_id, date, subject, body_html, body_md,
                    meeting_title, meeting_date, meeting_duration_mins,
                    meeting_url, ask_fathom_url,
                    action_items_count, topics_count, next_steps_count,
                    total_links_count, fathom_timestamp_links_count
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                msg_id, thread_id, date, subject, body_html, markdown_result,
                stats.get('meeting_title'), stats.get('meeting_date'),
                stats.get('meeting_duration_mins'), stats.get('meeting_url'),
                stats.get('ask_fathom_url'), stats.get('action_items_count'),
                stats.get('topics_count'), stats.get('next_steps_count'),
                stats.get('total_links_count'), stats.get('fathom_timestamp_links_count')
            ))

        except HttpError as error:
            print(f"\nAn error occurred downloading message {msg_id}: {error}")

    conn.commit()
    
    # Link public URLs to calls table
    print("\n🔗 Linking public URLs to calls table...")
    link_public_urls(conn)
    
    conn.close()
    print("\nDownload complete. The local database is now up to date.")


def link_public_urls(conn):
    """Match newly downloaded emails to calls and populate public_share_url.
    
    Uses enhanced matching with duration as tiebreaker for duplicate titles.
    """
    from datetime import datetime
    import re
    
    cursor = conn.cursor()
    
    # Get emails with metadata for matching
    # CRITICAL: ONLY process /share/ URLs (public, no login required)
    # Ignore /calls/ URLs as they require login and can cause mis-matches
    cursor.execute("""
        SELECT message_id, meeting_title, meeting_date, meeting_duration_mins, meeting_url, date
        FROM emails 
        WHERE meeting_url IS NOT NULL 
          AND meeting_url != ''
          AND meeting_url LIKE '%/share/%'
        ORDER BY date ASC
    """)
    emails = cursor.fetchall()
    
    # Get all calls without public URLs (include duration and timestamp for tiebreaker)
    cursor.execute("""
        SELECT rowid, title, date, duration, created_at
        FROM calls
        WHERE public_share_url IS NULL OR public_share_url = ''
        ORDER BY created_at ASC
    """)
    calls = cursor.fetchall()
    
    # Normalize date to YYYY-MM-DD format for comparison
    def normalize_date(date_str):
        """Convert various date formats to YYYY-MM-DD"""
        if not date_str:
            return None
        try:
            # Try common formats
            for fmt in ['%B %d, %Y', '%b %d, %Y', '%Y-%m-%d', '%m/%d/%Y']:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            return None
        except:
            return None
    
    def extract_duration_mins(duration_str):
        """Extract minutes from duration strings like '45 mins' or '1 hr 23 mins'"""
        if not duration_str:
            return None
        try:
            total_mins = 0
            # Look for hours
            hr_match = re.search(r'(\d+)\s*hr', duration_str, re.IGNORECASE)
            if hr_match:
                total_mins += int(hr_match.group(1)) * 60
            # Look for minutes
            min_match = re.search(r'(\d+)\s*min', duration_str, re.IGNORECASE)
            if min_match:
                total_mins += int(min_match.group(1))
            return total_mins if total_mins > 0 else None
        except:
            return None
    
    updated = 0
    used_call_ids = set()  # Track which calls we've already linked
    
    for msg_id, email_title, email_date, email_dur, public_url, email_timestamp in emails:
        if not email_title or not email_date:
            continue
        
        email_date_norm = normalize_date(email_date)
        if not email_date_norm:
            continue
        
        # Find all matching calls by title and date
        matching_calls = []
        for rowid, call_title, call_date, call_duration, call_timestamp in calls:
            if rowid in used_call_ids:
                continue  # Skip already-linked calls
            
            call_date_norm = normalize_date(call_date)
            if (call_date_norm == email_date_norm and 
                call_title.lower() == email_title.lower()):
                matching_calls.append((rowid, call_duration, call_timestamp))
        
        if not matching_calls:
            continue  # No matches for this email
        
        # If only one match, link it
        if len(matching_calls) == 1:
            rowid = matching_calls[0][0]
            cursor.execute("""
                UPDATE calls 
                SET public_share_url = ? 
                WHERE rowid = ?
            """, (public_url, rowid))
            updated += 1
            used_call_ids.add(rowid)
        else:
            # Multiple matches - disambiguate by duration, then by timestamp
            best_match = None
            best_match_info = None
            
            if email_dur:
                # Find best duration match (closest match wins)
                best_dur_diff = float('inf')
                for rowid, call_duration, call_timestamp in matching_calls:
                    call_dur_mins = extract_duration_mins(call_duration)
                    if call_dur_mins:
                        dur_diff = abs(call_dur_mins - email_dur)
                        if dur_diff < best_dur_diff:
                            best_dur_diff = dur_diff
                            best_match = rowid
                            best_match_info = (rowid, call_duration, call_timestamp)
            
            # If no duration match, use earliest call (by created_at timestamp)
            if not best_match:
                best_match_info = min(matching_calls, key=lambda x: x[2])  # x[2] is created_at
                best_match = best_match_info[0]
            
            cursor.execute("""
                UPDATE calls 
                SET public_share_url = ? 
                WHERE rowid = ?
            """, (public_url, best_match))
            updated += 1
            used_call_ids.add(best_match)
    
    conn.commit()
    if updated > 0:
        print(f"   ✅ Linked {updated} public URLs to calls")
    else:
        print(f"   ℹ️  No new links needed")


if __name__ == '__main__':
    main()
