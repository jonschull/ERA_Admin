#!/usr/bin/env python3
"""
Test Google API authentication system.
Verifies credentials, token validity, and Gmail API access.
"""

import os
import sys
import json
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Add parent directory to path for imports
sys.path.append('..')

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def check_credentials_file():
    """Check if credentials.json exists and is valid."""
    print("🔍 Checking credentials.json...")
    
    if not os.path.exists('../credentials.json'):
        print("❌ credentials.json not found")
        return False
    
    try:
        with open('../credentials.json', 'r') as f:
            creds_data = json.load(f)
        
        required_fields = ['client_id', 'client_secret', 'auth_uri', 'token_uri']
        installed = creds_data.get('installed', {})
        
        for field in required_fields:
            if field not in installed:
                print(f"❌ Missing required field: {field}")
                return False
        
        print(f"✅ credentials.json valid")
        print(f"   Project ID: {installed.get('project_id', 'N/A')}")
        print(f"   Client ID: {installed['client_id'][:20]}...")
        return True
        
    except json.JSONDecodeError:
        print("❌ credentials.json is not valid JSON")
        return False
    except Exception as e:
        print(f"❌ Error reading credentials.json: {e}")
        return False

def check_token_file():
    """Check if token.json exists and analyze its status."""
    print("\n🔍 Checking token.json...")
    
    if not os.path.exists('../token.json'):
        print("⚠️  token.json not found (will be created on first OAuth flow)")
        return None
    
    try:
        with open('../token.json', 'r') as f:
            token_data = json.load(f)
        
        print("✅ token.json found")
        
        # Check expiry
        if 'expiry' in token_data:
            expiry_str = token_data['expiry']
            expiry_time = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
            now = datetime.now(expiry_time.tzinfo)
            
            if expiry_time > now:
                time_left = expiry_time - now
                print(f"✅ Access token valid for {time_left}")
            else:
                print("⚠️  Access token expired")
        
        # Check refresh token
        if 'refresh_token' in token_data:
            print("✅ Refresh token present")
        else:
            print("❌ No refresh token (will require full OAuth flow)")
        
        # Check scopes
        scopes = token_data.get('scopes', [])
        print(f"📋 Scopes: {', '.join(scopes)}")
        
        return token_data
        
    except json.JSONDecodeError:
        print("❌ token.json is not valid JSON")
        return None
    except Exception as e:
        print(f"❌ Error reading token.json: {e}")
        return None

def test_gmail_authentication():
    """Test Gmail API authentication and access."""
    print("\n🔍 Testing Gmail API authentication...")
    
    try:
        creds = None
        
        # Load existing token
        if os.path.exists('../token.json'):
            creds = Credentials.from_authorized_user_file('../token.json', SCOPES)
        
        # Handle expired/invalid credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refreshing expired token...")
                creds.refresh(Request())
                print("✅ Token refreshed successfully")
                
                # Save refreshed token
                with open('../token.json', 'w') as token:
                    token.write(creds.to_json())
                print("💾 Updated token saved")
                
            else:
                print("🌐 Starting OAuth flow...")
                flow = InstalledAppFlow.from_client_secrets_file('../credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                print("✅ OAuth flow completed")
                
                # Save new token
                with open('../token.json', 'w') as token:
                    token.write(creds.to_json())
                print("💾 New token saved")
        
        # Test Gmail API access
        print("📧 Testing Gmail API access...")
        service = build('gmail', 'v1', credentials=creds)
        
        # Get user profile
        profile = service.users().getProfile(userId='me').execute()
        print(f"✅ Gmail API access successful")
        print(f"   Email: {profile.get('emailAddress', 'N/A')}")
        print(f"   Messages: {profile.get('messagesTotal', 'N/A'):,}")
        print(f"   Threads: {profile.get('threadsTotal', 'N/A'):,}")
        
        # Test search for Fathom emails
        print("🔍 Testing Fathom email search...")
        query = 'from:noreply@fathom.video'
        results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
        messages = results.get('messages', [])
        print(f"✅ Found {len(messages)} recent Fathom emails")
        
        return True
        
    except HttpError as error:
        print(f"❌ Gmail API error: {error}")
        return False
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False

def main():
    """Run comprehensive Google authentication tests."""
    print("=" * 60)
    print("🔐 GOOGLE API AUTHENTICATION TEST")
    print("=" * 60)
    
    # Test credentials file
    creds_ok = check_credentials_file()
    
    # Test token file
    token_data = check_token_file()
    
    # Test actual authentication
    if creds_ok:
        auth_ok = test_gmail_authentication()
    else:
        print("\n❌ Cannot test authentication without valid credentials.json")
        auth_ok = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 AUTHENTICATION TEST SUMMARY")
    print("=" * 60)
    print(f"Credentials file: {'✅ OK' if creds_ok else '❌ FAIL'}")
    print(f"Token file: {'✅ OK' if token_data else '⚠️  MISSING'}")
    print(f"Gmail API access: {'✅ OK' if auth_ok else '❌ FAIL'}")
    
    if creds_ok and auth_ok:
        print("\n🎉 Google API authentication is fully functional!")
    else:
        print("\n⚠️  Google API authentication needs attention.")
        print("\nNext steps:")
        if not creds_ok:
            print("1. Set up Google Cloud project and download credentials.json")
        if not auth_ok:
            print("2. Run this script to complete OAuth flow")

if __name__ == "__main__":
    main()
