#!/usr/bin/env python3
"""
Cross-check jschull@gmail.com Fathom notifications against the database.
Identify any calls that appear in Gmail but not in our database.
"""
import sqlite3
import re
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

DB_FILE = "fathom_emails.db"
TOKEN_FILE = "token_jschull.json"

def get_gmail_service():
    """Get Gmail service for jschull@gmail.com"""
    creds = Credentials.from_authorized_user_file(TOKEN_FILE)
    return build('gmail', 'v1', credentials=creds)

def extract_call_info(subject, body):
    """Extract call information from notification email"""
    # Extract title from subject
    title = None
    if 'Recap for' in subject:
        match = re.search(r'Recap for ["\'](.+?)["\']', subject)
        if match:
            title = match.group(1)
    elif 'Recap of your meeting with' in subject:
        match = re.search(r'Recap of your meeting with (.+)', subject)
        if match:
            title = match.group(1).strip()
    
    # Extract call URL from body
    call_url = None
    match = re.search(r'https://fathom\.video/calls/\d+', body)
    if match:
        call_url = match.group(0)
    
    return title, call_url

def main():
    print("🔍 CROSS-CHECKING JSCHULL@GMAIL.COM NOTIFICATIONS")
    print("=" * 80)
    
    # Get database calls
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT hyperlink, title FROM calls")
    db_calls = {row[0]: row[1] for row in cursor.fetchall()}
    print(f"📊 Database has {len(db_calls)} calls\n")
    
    # Get Gmail notifications
    print("📧 Fetching notifications from jschull@gmail.com...")
    service = get_gmail_service()
    
    results = service.users().messages().list(
        userId='me',
        q='from:fathom.video recap',
        maxResults=500
    ).execute()
    
    messages = results.get('messages', [])
    print(f"   Found {len(messages)} notification emails\n")
    
    # Parse notifications
    gmail_calls = {}
    for msg_ref in messages:
        msg = service.users().messages().get(
            userId='me',
            id=msg_ref['id'],
            format='full'
        ).execute()
        
        # Get subject
        subject = ''
        for header in msg['payload']['headers']:
            if header['name'] == 'Subject':
                subject = header['value']
                break
        
        # Get body
        body = ''
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                    break
        elif 'body' in msg['payload']:
            body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8', errors='ignore')
        
        title, call_url = extract_call_info(subject, body)
        if call_url:
            gmail_calls[call_url] = title
    
    print(f"✅ Extracted {len(gmail_calls)} call URLs from notifications\n")
    
    # Compare
    print("=" * 80)
    print("📊 COMPARISON RESULTS")
    print("=" * 80)
    
    # Calls in Gmail but not in database
    missing_in_db = []
    for call_url, title in gmail_calls.items():
        if call_url not in db_calls:
            missing_in_db.append((title, call_url))
    
    # Calls in database but not in Gmail
    missing_in_gmail = []
    for call_url, title in db_calls.items():
        if call_url not in gmail_calls:
            missing_in_gmail.append((title, call_url))
    
    print(f"\n📧 Gmail notifications: {len(gmail_calls)}")
    print(f"💾 Database calls: {len(db_calls)}")
    print(f"🔗 Matching calls: {len(set(gmail_calls.keys()) & set(db_calls.keys()))}")
    print(f"\n⚠️  In Gmail but NOT in database: {len(missing_in_db)}")
    print(f"⚠️  In database but NOT in Gmail: {len(missing_in_gmail)}")
    
    if missing_in_db:
        print(f"\n" + "=" * 80)
        print(f"⚠️  CALLS IN GMAIL BUT NOT IN DATABASE ({len(missing_in_db)} calls)")
        print("=" * 80)
        print("\nThese calls may have been missed by the scraper:")
        for i, (title, url) in enumerate(missing_in_db[:10], 1):
            print(f"{i}. {title[:60]}")
            print(f"   {url}")
        if len(missing_in_db) > 10:
            print(f"   ... and {len(missing_in_db) - 10} more")
    
    if missing_in_gmail:
        print(f"\n" + "=" * 80)
        print(f"ℹ️  CALLS IN DATABASE BUT NOT IN GMAIL ({len(missing_in_gmail)} calls)")
        print("=" * 80)
        print("\nThis is expected - Gmail only has recent notifications:")
        print(f"Total: {len(missing_in_gmail)} calls")
        print("(Database has historical calls going back further)")
    
    # Summary
    print(f"\n" + "=" * 80)
    print("📈 COVERAGE SUMMARY")
    print("=" * 80)
    if len(missing_in_db) == 0:
        print("✅ All Gmail notifications are in the database")
        print("✅ No calls appear to be missing from scraper")
    else:
        print(f"⚠️  {len(missing_in_db)} calls in Gmail are missing from database")
        print("   These may need to be added via scraper or manual entry")
    
    overlap_pct = len(set(gmail_calls.keys()) & set(db_calls.keys())) / len(gmail_calls) * 100 if gmail_calls else 0
    print(f"\n📊 Gmail→Database coverage: {overlap_pct:.1f}%")
    
    conn.close()

if __name__ == "__main__":
    main()
