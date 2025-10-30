#!/usr/bin/env python3
"""
Download pre-Fathom historical documents as one big searchable markdown file.

Skips Town Hall meetings (already in database).
Downloads remaining docs and concatenates into pre_fathom_docs.md for fast grep searching.
"""

import os
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io

# Scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/drive.readonly'
]

# Use FathomInventory credentials
FATHOM_DIR = Path(__file__).parent.parent.parent / 'FathomInventory'
TOKEN_FILE = FATHOM_DIR / 'token.json'
CREDENTIALS_FILE = FATHOM_DIR / 'credentials.json'

# Historical documents folder
HISTORICAL_DOCS_FOLDER_ID = '1qEimCuk-usUdBFDUtYb8Y0x_BDWQFQ_s'
OUTPUT_FILE = Path(__file__).parent / 'pre_fathom_docs.md'


def get_drive_service():
    """Authenticate and return Google Drive service."""
    creds = None
    
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception as e:
            print(f"⚠️  Could not load existing token: {e}")
    
    needs_reauth = False
    if creds and creds.valid:
        if not any('drive' in scope for scope in (creds.scopes or [])):
            needs_reauth = True
    
    if not creds or not creds.valid or needs_reauth:
        if creds and creds.expired and creds.refresh_token and not needs_reauth:
            try:
                creds.refresh(Request())
            except Exception:
                needs_reauth = True
        
        if not creds or not creds.valid or needs_reauth:
            if not CREDENTIALS_FILE.exists():
                print(f"❌ ERROR: credentials.json not found at {CREDENTIALS_FILE}")
                sys.exit(1)
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        TOKEN_FILE.write_text(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)


def should_skip_doc(file_name, folder_path):
    """Determine if document should be skipped (Town Halls already in DB)."""
    name_lower = file_name.lower()
    path_lower = folder_path.lower()
    
    # Skip Town Hall meetings (already in database)
    if 'town hall' in path_lower or 'town hall' in name_lower:
        return True
    
    # Skip if filename suggests it's a Town Hall
    if name_lower.startswith('th ') or 'town hall' in name_lower:
        return True
    
    return False


def export_doc_as_markdown(service, file_id):
    """Export a Google Doc as markdown text."""
    try:
        # Export as plain text (markdown not directly available)
        request = service.files().export_media(
            fileId=file_id,
            mimeType='text/plain'
        )
        
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        
        return fh.getvalue().decode('utf-8')
    except Exception as e:
        print(f"      ⚠️  Failed to export: {e}")
        return None


def download_folder_docs(service, folder_id, output_handle, folder_path="", stats=None):
    """
    Recursively download all Google Docs from folder, skip Town Halls.
    
    Args:
        service: Google Drive service
        folder_id: Folder ID to process
        output_handle: File handle to write to
        folder_path: Current folder path (for display/filtering)
        stats: Dict to track statistics
    """
    if stats is None:
        stats = {'total': 0, 'skipped': 0, 'downloaded': 0, 'failed': 0}
    
    try:
        # Get all items in folder
        query = f"'{folder_id}' in parents and trashed=false"
        response = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType, webViewLink, modifiedTime)',
            pageSize=1000
        ).execute()
        
        files = response.get('files', [])
        
        for file in files:
            file_name = file['name']
            current_path = f"{folder_path}/{file_name}" if folder_path else file_name
            
            # Recurse into folders
            if 'folder' in file['mimeType']:
                print(f"📁 {current_path}")
                download_folder_docs(service, file['id'], output_handle, current_path, stats)
                continue
            
            # Only process Google Docs
            if 'document' not in file['mimeType']:
                continue
            
            stats['total'] += 1
            
            # Skip Town Hall meetings
            if should_skip_doc(file_name, folder_path):
                stats['skipped'] += 1
                print(f"   ⏭️  Skipping: {file_name[:70]} (Town Hall)")
                continue
            
            # Download document
            print(f"   📄 Downloading: {file_name[:70]}...", end='')
            content = export_doc_as_markdown(service, file['id'])
            
            if content:
                # Write to output file with metadata header
                output_handle.write(f"\n\n{'='*80}\n")
                output_handle.write(f"FILE: {file_name}\n")
                output_handle.write(f"PATH: {current_path}\n")
                output_handle.write(f"LINK: {file.get('webViewLink', 'N/A')}\n")
                output_handle.write(f"MODIFIED: {file.get('modifiedTime', 'N/A')}\n")
                output_handle.write(f"{'='*80}\n\n")
                output_handle.write(content)
                output_handle.write("\n")
                
                stats['downloaded'] += 1
                print(" ✅")
            else:
                stats['failed'] += 1
                print(" ❌")
        
    except HttpError as e:
        print(f"❌ ERROR accessing folder: {e}")


def main():
    print()
    print("=" * 80)
    print("DOWNLOAD PRE-FATHOM HISTORICAL DOCUMENTS")
    print("=" * 80)
    print(f"Output: {OUTPUT_FILE}")
    print(f"Strategy: Skip Town Halls (in DB), download rest")
    print("=" * 80)
    print()
    
    # Get Drive service
    print("🔐 Authenticating with Google Drive...")
    service = get_drive_service()
    print()
    
    # Open output file
    print(f"📝 Creating output file: {OUTPUT_FILE}")
    
    stats = {'total': 0, 'skipped': 0, 'downloaded': 0, 'failed': 0}
    
    with open(OUTPUT_FILE, 'w') as f:
        f.write("# ERA Pre-Fathom Historical Documents\n\n")
        f.write(f"Source: https://drive.google.com/drive/folders/{HISTORICAL_DOCS_FOLDER_ID}\n")
        f.write(f"Downloaded: {Path(__file__).parent}\n")
        f.write(f"Note: Town Hall meetings excluded (already in database)\n\n")
        
        print()
        print("📥 Downloading documents...")
        print("-" * 80)
        
        download_folder_docs(service, HISTORICAL_DOCS_FOLDER_ID, f, stats=stats)
    
    print("-" * 80)
    print()
    print("=" * 80)
    print("DOWNLOAD COMPLETE")
    print("=" * 80)
    print(f"Total Google Docs found: {stats['total']}")
    print(f"  Skipped (Town Halls): {stats['skipped']}")
    print(f"  Downloaded: {stats['downloaded']}")
    print(f"  Failed: {stats['failed']}")
    print()
    print(f"✅ Output: {OUTPUT_FILE}")
    print(f"   Size: {OUTPUT_FILE.stat().st_size / (1024*1024):.1f} MB")
    print()
    print("=" * 80)
    print("USAGE:")
    print(f"  grep -i 'Valer Clark' {OUTPUT_FILE}")
    print(f"  grep -i 'Jan Pokorny' {OUTPUT_FILE}")
    print("=" * 80)
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
