#!/usr/bin/env python3
"""
Inspect Landscape Google Sheet Structure

Purpose: Understand the data format that ERA Landscape expects
Phase: 5T Prototype - Schema Discovery

This script reads the ERA Landscape Google Sheet and documents:
- Sheet structure (tabs, columns)
- Node types and formats (person, organization, project)
- Edge/relationship format
- Required vs optional fields
"""

import sys
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Sheet ID from CONTEXT_RECOVERY.md
LANDSCAPE_SHEET_ID = '1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY'

# Try to find credentials
CREDENTIAL_PATHS = [
    '/Users/admin/ERA_Admin/integration_scripts/credentials.json',
    '/Users/admin/ERA_Admin/FathomInventory/credentials.json',
    'credentials.json'
]

def find_credentials():
    """Find credentials file"""
    for path in CREDENTIAL_PATHS:
        if os.path.exists(path):
            print(f"✓ Found credentials: {path}")
            return path
    
    print("✗ No credentials.json found in:")
    for path in CREDENTIAL_PATHS:
        print(f"  - {path}")
    return None

def inspect_sheet(sheet_id):
    """Inspect the Google Sheet structure"""
    
    cred_path = find_credentials()
    if not cred_path:
        print("\n❌ Cannot proceed without credentials")
        print("\nOptions:")
        print("1. Copy from FathomInventory: cp ../FathomInventory/credentials.json .")
        print("2. Or set up OAuth (see setup_gmail_auth.py)")
        return False
    
    try:
        # Build the service
        # Note: Using user credentials (OAuth), not service account
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        
        # Try to use existing token
        token_path = 'token_jschull.json'
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path)
            
            # Refresh if needed
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        else:
            print(f"✗ No token file found: {token_path}")
            print("Run setup_gmail_auth.py first to authenticate")
            return False
        
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        # Get sheet metadata
        print(f"\n{'='*70}")
        print(f"INSPECTING LANDSCAPE SHEET: {sheet_id}")
        print(f"{'='*70}\n")
        
        metadata = sheet.get(spreadsheetId=sheet_id).execute()
        
        print(f"📊 Sheet Title: {metadata.get('properties', {}).get('title', 'Unknown')}")
        print(f"📊 URL: https://docs.google.com/spreadsheets/d/{sheet_id}")
        print()
        
        # List all sheets/tabs
        sheets = metadata.get('sheets', [])
        print(f"📑 Found {len(sheets)} tab(s):\n")
        
        for i, s in enumerate(sheets, 1):
            props = s.get('properties', {})
            title = props.get('title', 'Untitled')
            row_count = props.get('gridProperties', {}).get('rowCount', 0)
            col_count = props.get('gridProperties', {}).get('columnCount', 0)
            
            print(f"   {i}. {title}")
            print(f"      - Rows: {row_count}, Columns: {col_count}")
            print()
        
        # For each sheet, get the first few rows to understand structure
        print(f"\n{'='*70}")
        print("DETAILED TAB INSPECTION")
        print(f"{'='*70}\n")
        
        for s in sheets:
            title = s.get('properties', {}).get('title', 'Untitled')
            
            print(f"\n📋 Tab: '{title}'")
            print("-" * 70)
            
            # Read first 10 rows
            range_name = f"'{title}'!A1:Z10"
            try:
                result = sheet.values().get(
                    spreadsheetId=sheet_id,
                    range=range_name
                ).execute()
                
                values = result.get('values', [])
                
                if not values:
                    print("   (Empty sheet)")
                    continue
                
                # Show headers
                if len(values) > 0:
                    headers = values[0]
                    print(f"\n   Headers ({len(headers)} columns):")
                    for i, header in enumerate(headers, 1):
                        print(f"      {i:2d}. {header}")
                
                # Show sample rows
                if len(values) > 1:
                    print(f"\n   Sample data ({len(values)-1} rows shown):")
                    for row_idx, row in enumerate(values[1:], 1):
                        print(f"\n      Row {row_idx}:")
                        for col_idx, cell in enumerate(row):
                            if col_idx < len(headers):
                                print(f"         {headers[col_idx]:20s}: {cell}")
                        
                        if row_idx >= 3:  # Only show first 3 data rows
                            remaining = len(values) - 4
                            if remaining > 0:
                                print(f"\n      ... ({remaining} more rows not shown)")
                            break
                
            except HttpError as e:
                print(f"   ✗ Error reading sheet: {e}")
            
        print(f"\n{'='*70}")
        print("INSPECTION COMPLETE")
        print(f"{'='*70}\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("ERA Landscape Sheet Inspector")
    print("=" * 70)
    
    success = inspect_sheet(LANDSCAPE_SHEET_ID)
    
    if success:
        print("\n✅ Next steps:")
        print("   1. Review the output above")
        print("   2. Document schema in LANDSCAPE_SHEET_SCHEMA.md")
        print("   3. Design export format to match")
        print("   4. Build prototype export script")
    else:
        print("\n❌ Inspection failed - check errors above")
        sys.exit(1)

if __name__ == '__main__':
    main()
