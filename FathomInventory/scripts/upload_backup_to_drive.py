#!/usr/bin/env python3
"""
Upload database backups to Google Drive for off-site disaster recovery.

Uses fathomizer@ecorestorationalliance.org account.
Creates FathomInventory_Backups folder in Drive if not exists.
Automatically deletes backups older than 30 days.
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import pickle

# Add Drive scope to existing Gmail scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/drive.file'  # Only access files we create
]

SCRIPT_DIR = Path(__file__).parent
FATHOM_DIR = SCRIPT_DIR.parent
TOKEN_FILE = FATHOM_DIR / 'token.json'
CREDENTIALS_FILE = FATHOM_DIR / 'credentials.json'
BACKUP_FOLDER_NAME = 'FathomInventory_Backups'


def get_drive_service():
    """
    Authenticate and return Google Drive service.
    Will prompt for re-auth if Drive scope not yet granted.
    """
    creds = None
    
    # Load existing token
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception as e:
            print(f"⚠️  Could not load existing token: {e}")
    
    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"❌ ERROR: credentials.json not found at {CREDENTIALS_FILE}")
                print("Run Gmail setup first to create credentials.")
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


def find_or_create_backup_folder(service):
    """Find FathomInventory_Backups folder or create it."""
    try:
        # Search for existing folder
        response = service.files().list(
            q=f"name='{BACKUP_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        folders = response.get('files', [])
        
        if folders:
            folder_id = folders[0]['id']
            print(f"✅ Found backup folder: {BACKUP_FOLDER_NAME} (ID: {folder_id})")
            return folder_id
        
        # Create folder
        file_metadata = {
            'name': BACKUP_FOLDER_NAME,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = folder.get('id')
        print(f"✅ Created backup folder: {BACKUP_FOLDER_NAME} (ID: {folder_id})")
        return folder_id
        
    except HttpError as e:
        print(f"❌ ERROR accessing Drive: {e}")
        sys.exit(1)


def upload_file(service, file_path, folder_id):
    """Upload a file to Google Drive folder."""
    try:
        file_metadata = {
            'name': file_path.name,
            'parents': [folder_id]
        }
        
        media = MediaFileUpload(
            str(file_path),
            resumable=True
        )
        
        print(f"📤 Uploading: {file_path.name} ({file_path.stat().st_size // (1024*1024)}MB)")
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, size'
        ).execute()
        
        file_id = file.get('id')
        file_size = int(file.get('size', 0)) // (1024*1024)
        print(f"   ✅ Uploaded: {file.get('name')} ({file_size}MB) - ID: {file_id}")
        return file_id
        
    except HttpError as e:
        print(f"   ❌ Upload failed: {e}")
        return None


def cleanup_old_backups(service, folder_id, days_to_keep=30):
    """Delete backups older than specified days."""
    try:
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cutoff_iso = cutoff_date.isoformat() + 'Z'
        
        # Find old files in backup folder
        query = f"'{folder_id}' in parents and createdTime < '{cutoff_iso}' and trashed=false"
        response = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, createdTime)',
            orderBy='createdTime'
        ).execute()
        
        old_files = response.get('files', [])
        
        if not old_files:
            print(f"✅ No backups older than {days_to_keep} days")
            return
        
        print(f"🗑️  Found {len(old_files)} backups older than {days_to_keep} days:")
        for file in old_files:
            created = datetime.fromisoformat(file['createdTime'].replace('Z', '+00:00'))
            age_days = (datetime.now(created.tzinfo) - created).days
            print(f"   - {file['name']} (created {age_days} days ago)")
            
            # Delete file
            service.files().delete(fileId=file['id']).execute()
            print(f"     ✅ Deleted from Drive")
        
    except HttpError as e:
        print(f"⚠️  Could not cleanup old backups: {e}")


def main():
    print()
    print("=" * 60)
    print("GOOGLE DRIVE BACKUP UPLOAD")
    print(f"Account: fathomizer@ecorestorationalliance.org")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # Get Drive service
    print("🔐 Authenticating with Google Drive...")
    service = get_drive_service()
    print()
    
    # Find or create backup folder
    folder_id = find_or_create_backup_folder(service)
    print()
    
    # Find latest backups to upload
    backup_dir = FATHOM_DIR / 'backups'
    if not backup_dir.exists():
        print(f"❌ ERROR: Backup directory not found: {backup_dir}")
        sys.exit(1)
    
    # Find most recent backup files (ZIP only - 7x smaller than DB)
    zip_backups = sorted(backup_dir.glob('fathom_tables_*.zip'), reverse=True)
    
    if not zip_backups:
        print(f"❌ ERROR: No backup ZIP files found in {backup_dir}")
        sys.exit(1)
    
    latest_zip = zip_backups[0]
    
    print(f"📦 Latest backup to upload:")
    print(f"   ZIP: {latest_zip.name} ({latest_zip.stat().st_size // (1024*1024)}MB)")
    print(f"   (CSV archive - 7x smaller than DB, faster upload/download)")
    print()
    
    # Upload ZIP only
    print("📤 Starting upload...")
    
    zip_id = upload_file(service, latest_zip, folder_id)
    
    print()
    
    if zip_id:
        print(f"✅ Successfully uploaded to Google Drive")
    else:
        print(f"❌ Upload failed")
    
    print()
    
    # Cleanup old backups
    print(f"🗑️  Cleaning up backups older than 30 days...")
    cleanup_old_backups(service, folder_id, days_to_keep=30)
    
    print()
    print("=" * 60)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
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
