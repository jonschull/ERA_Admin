#!/usr/bin/env python3
"""
One-time setup: Authenticate jschull@gmail.com for research tool
Creates token_jschull.json for Gmail API access
"""

import os
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCRIPT_DIR = Path(__file__).parent
TOKEN_FILE = SCRIPT_DIR / "token_jschull.json"
CREDENTIALS_FILE = SCRIPT_DIR / "credentials.json"

# Gmail API scopes (read-only)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def setup_gmail_authentication():
    """
    Authenticate with jschull@gmail.com and save token.
    Opens browser for one-time OAuth consent.
    """
    print("=" * 80)
    print("GMAIL AUTHENTICATION SETUP")
    print("=" * 80)
    print()
    print("This will authenticate jschull@gmail.com for research purposes.")
    print("A browser window will open - please log in with jschull@gmail.com")
    print()
    
    # Check for credentials file
    if not CREDENTIALS_FILE.exists():
        print(f"❌ ERROR: credentials.json not found at {CREDENTIALS_FILE}")
        print()
        print("To get credentials.json:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Enable Gmail API")
        print("3. Create OAuth 2.0 Client ID (Desktop app)")
        print("4. Download credentials.json")
        print(f"5. Save to: {CREDENTIALS_FILE}")
        return False
    
    creds = None
    
    # Check if token already exists
    if TOKEN_FILE.exists():
        print(f"⚠️  Token file already exists: {TOKEN_FILE}")
        response = input("Overwrite? (yes/no): ").strip().lower()
        if response != 'yes':
            print("Cancelled.")
            return False
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("Starting OAuth flow...")
            print("Browser will open - please:")
            print("  1. Select jschull@gmail.com account")
            print("  2. Allow access to Gmail (read-only)")
            print()
            input("Press ENTER to open browser...")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), 
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save credentials
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        
        print()
        print(f"✅ Token saved: {TOKEN_FILE}")
    
    # Verify it works
    print()
    print("Verifying authentication...")
    from googleapiclient.discovery import build
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        
        print()
        print("=" * 80)
        print("✅ AUTHENTICATION SUCCESSFUL")
        print("=" * 80)
        print(f"Email: {profile['emailAddress']}")
        print(f"Messages: {profile.get('messagesTotal', 'N/A')}")
        print()
        print("You can now use gmail_research.py to search this account.")
        return True
    
    except Exception as e:
        print(f"❌ Error verifying authentication: {e}")
        return False


if __name__ == "__main__":
    import sys
    
    success = setup_gmail_authentication()
    sys.exit(0 if success else 1)
