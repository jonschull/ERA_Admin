#!/usr/bin/env python3
"""
List and explore pre-Fathom historical documents from Google Drive.

Folder: ERA Historical Documents (Pre-Fathom)
URL: https://drive.google.com/drive/folders/1qEimCuk-usUdBFDUtYb8Y0x_BDWQFQ_s

This script uses the existing Google Drive API authentication from FathomInventory.
"""

import os
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes - need Drive readonly access
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/drive.readonly'  # Read-only access to Drive
]

# Use FathomInventory credentials
FATHOM_DIR = Path(__file__).parent.parent.parent / 'FathomInventory'
TOKEN_FILE = FATHOM_DIR / 'token.json'
CREDENTIALS_FILE = FATHOM_DIR / 'credentials.json'

# Historical documents folder
HISTORICAL_DOCS_FOLDER_ID = '1qEimCuk-usUdBFDUtYb8Y0x_BDWQFQ_s'


def get_drive_service():
    """Authenticate and return Google Drive service."""
    creds = None
    
    # Load existing token
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception as e:
            print(f"⚠️  Could not load existing token: {e}")
    
    # Check if we need to re-auth for new scopes
    needs_reauth = False
    if creds and creds.valid:
        # Check if Drive scope is present
        if not any('drive' in scope for scope in (creds.scopes or [])):
            print("⚠️  Token doesn't have Drive scope - need to re-authenticate")
            needs_reauth = True
    
    # Refresh or get new credentials
    if not creds or not creds.valid or needs_reauth:
        if creds and creds.expired and creds.refresh_token and not needs_reauth:
            print("🔄 Refreshing expired credentials...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"⚠️  Refresh failed: {e}")
                print("   Will re-authenticate...")
                needs_reauth = True
        
        if not creds or not creds.valid or needs_reauth:
            if not CREDENTIALS_FILE.exists():
                print(f"❌ ERROR: credentials.json not found at {CREDENTIALS_FILE}")
                print("Run FathomInventory Gmail setup first.")
                sys.exit(1)
            
            print("🔐 Need to authorize Google Drive access...")
            print(f"   Account: fathomizer@ecorestorationalliance.org")
            print()
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save credentials
        TOKEN_FILE.write_text(creds.to_json())
        print(f"✅ Credentials saved to {TOKEN_FILE}")
    
    return build('drive', 'v3', credentials=creds)


def list_folder_contents(service, folder_id, indent=0):
    """Recursively list folder contents."""
    try:
        # Query for all items in folder
        query = f"'{folder_id}' in parents and trashed=false"
        response = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType, modifiedTime, size, webViewLink)',
            orderBy='folder,name'
        ).execute()
        
        files = response.get('files', [])
        
        if not files:
            print(f"{'  ' * indent}(empty)")
            return []
        
        all_items = []
        
        for file in files:
            file_info = {
                'id': file['id'],
                'name': file['name'],
                'type': file['mimeType'],
                'modified': file.get('modifiedTime', 'N/A'),
                'size': file.get('size', 'N/A'),
                'link': file.get('webViewLink', 'N/A'),
                'indent': indent
            }
            all_items.append(file_info)
            
            # Print item
            prefix = '  ' * indent
            if 'folder' in file['mimeType']:
                print(f"{prefix}📁 {file['name']}/")
                # Recursively list subfolder
                subfolder_items = list_folder_contents(service, file['id'], indent + 1)
                all_items.extend(subfolder_items)
            elif 'document' in file['mimeType']:
                print(f"{prefix}📄 {file['name']} (Google Doc)")
            elif 'spreadsheet' in file['mimeType']:
                print(f"{prefix}📊 {file['name']} (Google Sheet)")
            elif 'presentation' in file['mimeType']:
                print(f"{prefix}📽️  {file['name']} (Google Slides)")
            else:
                size_mb = int(file.get('size', 0)) / (1024 * 1024) if file.get('size') else 0
                if size_mb > 0:
                    print(f"{prefix}📎 {file['name']} ({size_mb:.1f}MB)")
                else:
                    print(f"{prefix}📎 {file['name']}")
        
        return all_items
        
    except HttpError as e:
        print(f"❌ ERROR accessing folder: {e}")
        return []


def get_folder_info(service, folder_id):
    """Get information about the folder."""
    try:
        folder = service.files().get(
            fileId=folder_id,
            fields='id, name, modifiedTime, webViewLink'
        ).execute()
        return folder
    except HttpError as e:
        print(f"❌ ERROR: Could not access folder: {e}")
        print("\nPossible reasons:")
        print("  1. Folder not shared with fathomizer@ecorestorationalliance.org")
        print("  2. Folder ID is incorrect")
        print("  3. Need to authorize Drive access")
        sys.exit(1)


def export_inventory(items, output_file='gdrive_historical_inventory.txt'):
    """Export inventory to text file."""
    output_path = Path(__file__).parent / output_file
    
    with open(output_path, 'w') as f:
        f.write("ERA Historical Documents (Pre-Fathom) Inventory\n")
        f.write("=" * 70 + "\n")
        f.write(f"Folder: {HISTORICAL_DOCS_FOLDER_ID}\n")
        f.write(f"URL: https://drive.google.com/drive/folders/{HISTORICAL_DOCS_FOLDER_ID}\n")
        f.write(f"Total items: {len(items)}\n")
        f.write("=" * 70 + "\n\n")
        
        for item in items:
            prefix = '  ' * item['indent']
            f.write(f"{prefix}{item['name']}\n")
            f.write(f"{prefix}  ID: {item['id']}\n")
            f.write(f"{prefix}  Type: {item['type']}\n")
            f.write(f"{prefix}  Modified: {item['modified']}\n")
            f.write(f"{prefix}  Link: {item['link']}\n")
            f.write("\n")
    
    print(f"\n✅ Inventory exported to: {output_path}")


def main():
    print()
    print("=" * 70)
    print("ERA HISTORICAL DOCUMENTS EXPLORER (Pre-Fathom)")
    print("=" * 70)
    print(f"Folder ID: {HISTORICAL_DOCS_FOLDER_ID}")
    print(f"URL: https://drive.google.com/drive/folders/{HISTORICAL_DOCS_FOLDER_ID}")
    print()
    
    # Get Drive service
    print("🔐 Authenticating with Google Drive...")
    service = get_drive_service()
    print()
    
    # Get folder info
    print("📁 Accessing folder...")
    folder_info = get_folder_info(service, HISTORICAL_DOCS_FOLDER_ID)
    print(f"✅ Folder: {folder_info['name']}")
    print(f"   Last modified: {folder_info.get('modifiedTime', 'N/A')}")
    print()
    
    # List contents
    print("📂 Folder Contents:")
    print("-" * 70)
    items = list_folder_contents(service, HISTORICAL_DOCS_FOLDER_ID)
    print("-" * 70)
    print(f"\n✅ Total items found: {len(items)}")
    
    # Export inventory
    export_inventory(items)
    
    # Summary by type
    print("\n📊 Summary by Type:")
    type_counts = {}
    for item in items:
        file_type = item['type']
        if 'folder' in file_type:
            key = 'Folders'
        elif 'document' in file_type:
            key = 'Google Docs'
        elif 'spreadsheet' in file_type:
            key = 'Google Sheets'
        elif 'presentation' in file_type:
            key = 'Google Slides'
        else:
            key = 'Other files'
        type_counts[key] = type_counts.get(key, 0) + 1
    
    for file_type, count in sorted(type_counts.items()):
        print(f"   {file_type}: {count}")
    
    print()
    print("=" * 70)
    print("NEXT STEPS:")
    print("  1. Review gdrive_historical_inventory.txt")
    print("  2. Identify documents with member names/rosters")
    print("  3. Decide: Download all docs vs API search vs selective download")
    print("=" * 70)
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
