#!/usr/bin/env python3
"""
Prototype: Export Fathom Participants to ERA Landscape

Purpose: Test Phase 5T integration with small batch (5-10 people)
Phase: Prototype - validate schema, deduplication, and visualization update

This script:
1. Queries validated participants from FathomInventory DB
2. Checks for duplicates in Landscape Google Sheet
3. Formats as Landscape nodes (person::Name)
4. Exports to Google Sheet
5. Updates landscape_node_id in FathomInventory DB
6. Generates validation report

Conservative approach: Start small, validate, iterate.
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from era_config import Config

# Configuration
SHEET_ID = Config.LANDSCAPE_SHEET_ID
DB_PATH = Config.FATHOM_DB_PATH
TOKEN_PATH = Path(__file__).parent / "token_jschull.json"

# Google Sheets API scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/gmail.readonly'
]

class LandscapeExporter:
    """Export Fathom participants to Landscape Google Sheet"""
    
    def __init__(self, sheet_id, db_path, token_path, limit=10):
        self.sheet_id = sheet_id
        self.db_path = db_path
        self.token_path = token_path
        self.limit = limit
        self.service = None
        self.conn = None
        self.stats = {
            'queried': 0,
            'already_in_landscape': 0,
            'exported': 0,
            'updated_db': 0,
            'errors': []
        }
    
    def connect(self):
        """Connect to Google Sheets API and FathomInventory DB"""
        print("\n" + "="*70)
        print("LANDSCAPE EXPORT PROTOTYPE")
        print("="*70)
        
        # Connect to Sheets API
        print("\n📊 Connecting to Google Sheets API...")
        try:
            creds = None
            if self.token_path.exists():
                creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    print("   Refreshing expired token...")
                    creds.refresh(Request())
                else:
                    raise Exception(f"No valid token at {self.token_path}. Run setup_gmail_auth.py first.")
            
            self.service = build('sheets', 'v4', credentials=creds)
            print("   ✅ Connected to Google Sheets API")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
        
        # Connect to database
        print(f"\n💾 Connecting to FathomInventory DB: {self.db_path}")
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            print("   ✅ Connected to database")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
        
        return True
    
    def read_sheet_tab(self, tab_name):
        """Read data from Google Sheet tab"""
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=f"{tab_name}!A:Z"
            ).execute()
            
            rows = result.get('values', [])
            if not rows:
                return []
            
            headers = rows[0]
            return [dict(zip(headers, row + ['']*(len(headers)-len(row)))) for row in rows[1:]]
        
        except HttpError as e:
            print(f"   ⚠️  Error reading {tab_name}: {e}")
            return []
    
    def query_participants(self):
        """Query validated participants from FathomInventory DB"""
        print(f"\n🔍 Querying validated participants (limit: {self.limit})...")
        
        query = """
        SELECT DISTINCT
            p.id,
            p.name,
            p.location,
            p.affiliation,
            p.email,
            p.landscape_node_id,
            p.validated_by_airtable,
            p.era_member,
            p.is_donor,
            p.airtable_id
        FROM participants p
        WHERE p.validated_by_airtable = 1
            AND p.era_member = 1
            AND p.landscape_node_id IS NULL
        ORDER BY p.name
        LIMIT ?
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query, (self.limit,))
        participants = [dict(row) for row in cursor.fetchall()]
        
        self.stats['queried'] = len(participants)
        print(f"   ✅ Found {len(participants)} validated ERA members without landscape_node_id")
        
        return participants
    
    def check_duplicates(self, participants):
        """Check which participants already exist in Landscape"""
        print(f"\n🔎 Checking for duplicates in Landscape sheet...")
        
        # Read existing nodes from sheet
        existing_nodes = self.read_sheet_tab('nodes')
        existing_ids = {node.get('id', '') for node in existing_nodes}
        
        print(f"   📊 Found {len(existing_nodes)} existing nodes in sheet")
        
        # Check each participant
        new_participants = []
        for p in participants:
            node_id = f"person::{p['name']}"
            if node_id in existing_ids:
                print(f"   ⚠️  Already exists: {p['name']}")
                self.stats['already_in_landscape'] += 1
            else:
                new_participants.append(p)
        
        print(f"   ✅ {len(new_participants)} new participants to export")
        
        return new_participants
    
    def format_as_nodes(self, participants):
        """Format participants as Landscape node objects"""
        print(f"\n📝 Formatting {len(participants)} participants as nodes...")
        
        nodes = []
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        for p in participants:
            node = {
                'id': f"person::{p['name']}",
                'label': p['name'],
                'type': 'person',
                'url': '',
                'notes': p['affiliation'] or '',
                'member': 'true' if p['era_member'] else '',
                'origin': 'fathom_export',
                'hidden': 'false',
                'created_at': timestamp,
                'updated_at': timestamp
            }
            nodes.append(node)
            print(f"   ✓ {node['id']}")
        
        print(f"   ✅ Formatted {len(nodes)} nodes")
        return nodes
    
    def append_to_sheet(self, nodes):
        """Append nodes to Google Sheet"""
        if not nodes:
            print("\n⚠️  No nodes to export")
            return True
        
        print(f"\n📤 Appending {len(nodes)} nodes to Google Sheet...")
        
        try:
            # Get current data to merge with
            existing_nodes = self.read_sheet_tab('nodes')
            
            # Combine existing + new
            all_nodes = existing_nodes + nodes
            
            # Prepare data for writing
            if not all_nodes:
                print("   ⚠️  No data to write")
                return False
            
            headers = list(all_nodes[0].keys())
            rows = [headers] + [[node.get(h, '') for h in headers] for node in all_nodes]
            
            # Clear and write
            print("   ⏳ Clearing sheet...")
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.sheet_id,
                range='nodes!A:Z'
            ).execute()
            
            print("   ⏳ Writing data...")
            self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range='nodes!A1',
                valueInputOption='RAW',
                body={'values': rows}
            ).execute()
            
            self.stats['exported'] = len(nodes)
            print(f"   ✅ Successfully exported {len(nodes)} nodes")
            return True
        
        except HttpError as e:
            error_msg = f"Error writing to sheet: {e}"
            print(f"   ❌ {error_msg}")
            self.stats['errors'].append(error_msg)
            return False
    
    def update_database(self, participants, nodes):
        """Update landscape_node_id in FathomInventory DB"""
        if not nodes:
            return
        
        print(f"\n💾 Updating landscape_node_id in database...")
        
        cursor = self.conn.cursor()
        
        for p, node in zip(participants, nodes):
            try:
                cursor.execute(
                    "UPDATE participants SET landscape_node_id = ? WHERE id = ?",
                    (node['id'], p['id'])
                )
                self.stats['updated_db'] += 1
                print(f"   ✓ Updated DB: {p['name']} → {node['id']}")
            
            except Exception as e:
                error_msg = f"Error updating {p['name']}: {e}"
                print(f"   ❌ {error_msg}")
                self.stats['errors'].append(error_msg)
        
        self.conn.commit()
        print(f"   ✅ Updated {self.stats['updated_db']} records in database")
    
    def generate_report(self):
        """Generate validation report"""
        print("\n" + "="*70)
        print("EXPORT SUMMARY")
        print("="*70)
        print(f"\n📊 Statistics:")
        print(f"   - Queried from DB:        {self.stats['queried']}")
        print(f"   - Already in Landscape:   {self.stats['already_in_landscape']}")
        print(f"   - Exported to sheet:      {self.stats['exported']}")
        print(f"   - Updated in DB:          {self.stats['updated_db']}")
        
        if self.stats['errors']:
            print(f"\n⚠️  Errors ({len(self.stats['errors'])}):")
            for error in self.stats['errors']:
                print(f"   - {error}")
        else:
            print(f"\n✅ No errors")
        
        print(f"\n🔗 View in Landscape:")
        print(f"   - Live site: https://jonschull.github.io/ERA_Landscape_Static/")
        print(f"   - Google Sheet: https://docs.google.com/spreadsheets/d/{self.sheet_id}")
        
        print("\n" + "="*70)
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def run(self):
        """Run the export process"""
        try:
            # Connect
            if not self.connect():
                return False
            
            # Query participants
            participants = self.query_participants()
            if not participants:
                print("\n⚠️  No participants found to export")
                return True
            
            # Check duplicates
            new_participants = self.check_duplicates(participants)
            if not new_participants:
                print("\n✅ All participants already in Landscape")
                return True
            
            # Format as nodes
            nodes = self.format_as_nodes(new_participants)
            
            # Export to sheet
            if not self.append_to_sheet(nodes):
                return False
            
            # Update database
            self.update_database(new_participants, nodes)
            
            # Report
            self.generate_report()
            
            return True
        
        finally:
            self.close()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Export Fathom participants to Landscape (prototype)')
    parser.add_argument('--limit', type=int, default=10, help='Max participants to export (default: 10)')
    parser.add_argument('--dry-run', action='store_true', help='Query and format, but don\'t write')
    args = parser.parse_args()
    
    exporter = LandscapeExporter(
        sheet_id=SHEET_ID,
        db_path=DB_PATH,
        token_path=TOKEN_PATH,
        limit=args.limit
    )
    
    if args.dry_run:
        print("\n⚠️  DRY RUN MODE - Will not write to sheet or database\n")
    
    success = exporter.run()
    
    if not args.dry_run:
        print("\n🎯 Next Steps:")
        print("   1. Visit live site and verify nodes appear")
        print("   2. Check for duplicates or data quality issues")
        print("   3. If successful, increase --limit and re-run")
        print("   4. Once validated, create full Town Hall export script")
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
