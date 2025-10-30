#!/usr/bin/env python3
"""
Search pre-Fathom historical documents for member names.

Uses Google Drive API to search document content without downloading.
Useful for verifying membership based on historical meeting participation.
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


def export_doc_as_text(service, file_id):
    """Export a Google Doc as plain text."""
    try:
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
        return None


def search_in_folder(service, folder_id, search_terms, recursive=True):
    """
    Search for terms in all documents within a folder.
    
    Args:
        service: Google Drive service
        folder_id: Folder ID to search in
        search_terms: List of search terms (e.g., ["Valer Clark", "Jan Pokorny"])
        recursive: Whether to search subfolders
    
    Returns:
        List of matches with file info and context
    """
    matches = []
    
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
        total_files = len(files)
        processed = 0
        
        for file in files:
            processed += 1
            
            # Recurse into folders
            if 'folder' in file['mimeType'] and recursive:
                subfolder_matches = search_in_folder(
                    service, file['id'], search_terms, recursive=True
                )
                matches.extend(subfolder_matches)
                continue
            
            # Only search Google Docs for now
            if 'document' not in file['mimeType']:
                continue
            
            print(f"  [{processed}/{total_files}] Searching: {file['name'][:60]}...", end='\r')
            
            # Export and search document
            text = export_doc_as_text(service, file['id'])
            if not text:
                continue
            
            text_lower = text.lower()
            
            # Check each search term
            for term in search_terms:
                term_lower = term.lower()
                if term_lower in text_lower:
                    # Find context around the match
                    idx = text_lower.find(term_lower)
                    start = max(0, idx - 100)
                    end = min(len(text), idx + len(term) + 100)
                    context = text[start:end].replace('\n', ' ').strip()
                    
                    matches.append({
                        'file_name': file['name'],
                        'file_id': file['id'],
                        'link': file.get('webViewLink', 'N/A'),
                        'modified': file.get('modifiedTime', 'N/A'),
                        'search_term': term,
                        'context': context
                    })
                    break  # Only report once per document
        
        print(" " * 80, end='\r')  # Clear progress line
        
    except HttpError as e:
        print(f"❌ ERROR searching folder: {e}")
    
    return matches


def search_names(service, names):
    """Search for a list of names in historical documents."""
    print(f"\n🔍 Searching for {len(names)} names in historical documents...")
    print(f"   This may take a few minutes (240+ documents to scan)")
    print()
    
    matches = search_in_folder(service, HISTORICAL_DOCS_FOLDER_ID, names)
    
    return matches


def format_results(matches):
    """Format search results for display."""
    if not matches:
        print("❌ No matches found")
        return
    
    print(f"\n✅ Found {len(matches)} matches:\n")
    print("=" * 80)
    
    # Group by search term
    by_term = {}
    for match in matches:
        term = match['search_term']
        if term not in by_term:
            by_term[term] = []
        by_term[term].append(match)
    
    for term, term_matches in sorted(by_term.items()):
        print(f"\n🔍 '{term}' - {len(term_matches)} mention(s):")
        print("-" * 80)
        
        for match in term_matches:
            print(f"\n📄 {match['file_name']}")
            print(f"   Link: {match['link']}")
            print(f"   Modified: {match['modified'][:10]}")
            print(f"   Context: ...{match['context']}...")


def save_results(matches, output_file='search_results.txt'):
    """Save search results to file."""
    output_path = Path(__file__).parent / output_file
    
    with open(output_path, 'w') as f:
        f.write("ERA Historical Documents Search Results\n")
        f.write("=" * 80 + "\n\n")
        
        by_term = {}
        for match in matches:
            term = match['search_term']
            if term not in by_term:
                by_term[term] = []
            by_term[term].append(match)
        
        for term, term_matches in sorted(by_term.items()):
            f.write(f"\n'{term}' - {len(term_matches)} mention(s):\n")
            f.write("-" * 80 + "\n")
            
            for match in term_matches:
                f.write(f"\nFile: {match['file_name']}\n")
                f.write(f"Link: {match['link']}\n")
                f.write(f"Modified: {match['modified']}\n")
                f.write(f"Context: ...{match['context']}...\n")
                f.write("\n")
    
    print(f"\n✅ Results saved to: {output_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Search historical ERA documents for member names'
    )
    parser.add_argument(
        'names',
        nargs='+',
        help='Names to search for (e.g., "Valer Clark" "Jan Pokorny")'
    )
    parser.add_argument(
        '--save',
        action='store_true',
        help='Save results to file'
    )
    
    args = parser.parse_args()
    
    print()
    print("=" * 80)
    print("ERA HISTORICAL DOCUMENTS SEARCH")
    print("=" * 80)
    print(f"Folder: {HISTORICAL_DOCS_FOLDER_ID}")
    print(f"Searching for: {', '.join(args.names)}")
    print("=" * 80)
    
    # Get Drive service
    service = get_drive_service()
    
    # Search
    matches = search_names(service, args.names)
    
    # Display results
    format_results(matches)
    
    # Save if requested
    if args.save:
        save_results(matches)
    
    print()
    print("=" * 80)
    print(f"Search complete: {len(matches)} total matches")
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
