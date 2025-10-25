#!/usr/bin/env python3
"""
Export Town Hall Meetings to ERA Landscape

Purpose: Create Town Hall meeting chain with attendees
Phase: 5T - Town Hall visualization

Creates:
- Umbrella project: "Town Hall Meetings"
- Individual meeting nodes: "ERA Town Hall - [date]"
- Person nodes for validated attendees
- Edges: person→meeting (attended), meeting→umbrella (part_of)
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.path.insert(0, str(Path(__file__).parent.parent))
from era_config import Config

SHEET_ID = Config.LANDSCAPE_SHEET_ID
DB_PATH = Config.FATHOM_DB_PATH
TOKEN_PATH = Path(__file__).parent / "token_jschull.json"

class TownHallExporter:
    """Export Town Hall meetings and attendees to Landscape"""
    
    def __init__(self, sheet_id, db_path, token_path, limit=None):
        self.sheet_id = sheet_id
        self.db_path = db_path
        self.token_path = token_path
        self.limit = limit
        self.service = None
        self.conn = None
        self.stats = {
            'meetings_found': 0,
            'meetings_exported': 0,
            'people_exported': 0,
            'edges_created': 0,
            'duplicates_skipped': 0
        }
    
    def connect(self):
        """Connect to API and database"""
        print("\n" + "="*70)
        print("TOWN HALL LANDSCAPE EXPORT")
        print("="*70)
        
        # Google Sheets
        print("\n📊 Connecting to Google Sheets API...")
        creds = Credentials.from_authorized_user_file(str(self.token_path))
        self.service = build('sheets', 'v4', credentials=creds)
        print("   ✅ Connected")
        
        # Database
        print(f"\n💾 Connecting to database...")
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        print("   ✅ Connected")
        
        return True
    
    def read_existing_nodes(self):
        """Read existing nodes from sheet"""
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range='nodes!A:Z'
        ).execute()
        
        rows = result.get('values', [])
        if not rows:
            return {}, []
        
        headers = rows[0]
        nodes = [dict(zip(headers, row + ['']*(len(headers)-len(row)))) for row in rows[1:]]
        node_ids = {n.get('id', '') for n in nodes}
        
        return node_ids, nodes
    
    def read_existing_edges(self):
        """Read existing edges from sheet"""
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range='edges!A:Z'
        ).execute()
        
        rows = result.get('values', [])
        if not rows:
            return []
        
        headers = rows[0]
        return [dict(zip(headers, row + ['']*(len(headers)-len(row)))) for row in rows[1:]]
    
    def query_town_halls(self):
        """Query Town Hall meetings and attendees"""
        print(f"\n🔍 Querying Town Hall meetings...")
        
        # Join with calls table to get dates
        query = """
        SELECT 
            p.source_call_title as meeting_title,
            p.source_call_url as meeting_url,
            c.date as meeting_date,
            COUNT(*) as total_attendees,
            COUNT(CASE WHEN p.validated_by_airtable = 1 THEN 1 END) as validated_attendees,
            COUNT(CASE WHEN p.era_member = 1 THEN 1 END) as era_members,
            GROUP_CONCAT(DISTINCT CASE WHEN p.validated_by_airtable = 1 THEN p.name END) as attendee_names
        FROM participants p
        LEFT JOIN calls c ON p.source_call_url = c.hyperlink
        WHERE p.source_call_title LIKE '%ERA%Town Hall%'
           OR p.source_call_title = 'ERA Town Hall Meeting'
        GROUP BY p.source_call_url
        ORDER BY c.date ASC
        """
        
        if self.limit:
            query += f" LIMIT {self.limit}"
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        meetings = [dict(row) for row in cursor.fetchall()]
        
        self.stats['meetings_found'] = len(meetings)
        print(f"   ✅ Found {len(meetings)} Town Hall meetings")
        
        return meetings
    
    def create_nodes_and_edges(self, meetings, existing_node_ids):
        """Create node and edge objects for export"""
        nodes = []
        edges = []
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Create umbrella project
        umbrella_id = "project::Town Hall Meetings"
        if umbrella_id not in existing_node_ids:
            nodes.append({
                'id': umbrella_id,
                'label': 'Town Hall Meetings',
                'type': 'project',
                'url': '',
                'notes': 'ERA community Town Hall meetings',
                'member': '',
                'origin': 'fathom_export',
                'hidden': 'false',
                'created_at': timestamp,
                'updated_at': timestamp
            })
            self.stats['meetings_exported'] += 1
            print(f"   ✓ Created umbrella: {umbrella_id}")
        
        # Process meetings to create linear chain
        # Track dates to handle duplicates
        date_counter = {}
        prev_meeting_id = None
        
        for idx, meeting in enumerate(meetings, 1):
            # Get date from database (YYYY-MM-DD format)
            meeting_date = meeting.get('meeting_date', '')
            
            # Convert YYYY-MM-DD to YYYY.MM.DD format
            if meeting_date and len(meeting_date) >= 10:
                date_label = meeting_date[:10].replace('-', '.')
            else:
                # Fallback to index if no date
                date_label = f"{idx:02d}"
                print(f"   ⚠️ Warning: No date for meeting, using #{date_label}")
            
            # Handle duplicate dates by adding sequence number
            if date_label in date_counter:
                date_counter[date_label] += 1
                unique_label = f"{date_label}.{date_counter[date_label]}"
            else:
                date_counter[date_label] = 1
                unique_label = date_label
            
            # Create meeting node as 'event' type with unique date in ID
            meeting_id = f"event::Town Hall {unique_label}"
            
            if meeting_id not in existing_node_ids:
                nodes.append({
                    'id': meeting_id,
                    'label': f"TH {unique_label}",
                    'type': 'event',
                    'url': meeting['meeting_url'] or '',
                    'notes': f"{meeting['validated_attendees']} validated attendees, {meeting['era_members']} ERA members",
                    'member': '',
                    'origin': 'fathom_export',
                    'hidden': 'false',
                    'created_at': timestamp,
                    'updated_at': timestamp
                })
                self.stats['meetings_exported'] += 1
            
            # Create chain: First TH connects to umbrella, subsequent THs connect to previous TH
            if idx == 1:
                # First Town Hall connects to umbrella project
                edges.append({
                    'source': meeting_id,
                    'target': umbrella_id,
                        'relationship': 'part_of',
                    'role': '',
                    'url': '',
                    'notes': '',
                    'created_at': timestamp,
                    'updated_at': timestamp
                })
            else:
                # Subsequent Town Halls connect to previous TH in chain
                edges.append({
                    'source': meeting_id,
                    'target': prev_meeting_id,
                    'relationship': 'follows',
                    'role': '',
                    'url': '',
                    'notes': '',
                    'created_at': timestamp,
                    'updated_at': timestamp
                })
            self.stats['edges_created'] += 1
            
            # Remember this meeting for next iteration's chain
            prev_meeting_id = meeting_id
            
            # Create person nodes and edges for validated attendees
            if meeting['attendee_names']:
                attendees = [name for name in meeting['attendee_names'].split(',') if name]
                
                for name in attendees:
                    person_id = f"person::{name}"
                    
                    # Create person node if doesn't exist
                    if person_id not in existing_node_ids:
                        nodes.append({
                            'id': person_id,
                            'label': name,
                            'type': 'person',
                            'url': '',
                            'notes': '',
                            'member': 'true',
                            'origin': 'fathom_export',
                            'hidden': 'false',
                            'created_at': timestamp,
                            'updated_at': timestamp
                        })
                        existing_node_ids.add(person_id)  # Track so we don't duplicate
                        self.stats['people_exported'] += 1
                    
                    # Create edge: person → meeting (attended)
                    edges.append({
                        'source': person_id,
                        'target': meeting_id,
                        'relationship': 'attended',
                        'role': '',
                        'url': '',
                        'notes': '',
                        'created_at': timestamp,
                        'updated_at': timestamp
                    })
                    self.stats['edges_created'] += 1
        
        print(f"\n   ✅ Created {len(nodes)} new nodes, {len(edges)} edges")
        return nodes, edges
    
    def write_to_sheet(self, new_nodes, new_edges, existing_nodes, existing_edges):
        """Write nodes and edges to Google Sheet"""
        print(f"\n📤 Writing to Google Sheet...")
        
        # Combine existing + new
        all_nodes = existing_nodes + new_nodes
        all_edges = existing_edges + new_edges
        
        # Write nodes
        if all_nodes:
            headers = list(all_nodes[0].keys())
            rows = [headers] + [[n.get(h, '') for h in headers] for n in all_nodes]
            
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.sheet_id,
                range='nodes!A:Z'
            ).execute()
            
            self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range='nodes!A1',
                valueInputOption='RAW',
                body={'values': rows}
            ).execute()
            print(f"   ✅ Wrote {len(all_nodes)} nodes")
        
        # Write edges
        if all_edges:
            headers = list(all_edges[0].keys())
            rows = [headers] + [[e.get(h, '') for h in headers] for e in all_edges]
            
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.sheet_id,
                range='edges!A:Z'
            ).execute()
            
            self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range='edges!A1',
                valueInputOption='RAW',
                body={'values': rows}
            ).execute()
            print(f"   ✅ Wrote {len(all_edges)} edges")
    
    def generate_report(self):
        """Generate summary report"""
        print("\n" + "="*70)
        print("EXPORT SUMMARY")
        print("="*70)
        print(f"\n📊 Statistics:")
        print(f"   - Meetings found:      {self.stats['meetings_found']}")
        print(f"   - Meetings exported:   {self.stats['meetings_exported']}")
        print(f"   - People exported:     {self.stats['people_exported']}")
        print(f"   - Edges created:       {self.stats['edges_created']}")
        
        print(f"\n🔗 View in Landscape:")
        print(f"   - Live site: https://jonschull.github.io/ERA_Landscape_Static/")
        print(f"   - Google Sheet: https://docs.google.com/spreadsheets/d/{self.sheet_id}")
        print("\n" + "="*70)
    
    def run(self):
        """Run the export"""
        try:
            self.connect()
            
            # Read existing data
            print("\n📖 Reading existing Landscape data...")
            existing_node_ids, existing_nodes = self.read_existing_nodes()
            existing_edges = self.read_existing_edges()
            print(f"   ✅ {len(existing_nodes)} nodes, {len(existing_edges)} edges")
            
            # Remove old Town Hall nodes (project:: and event:: prefix) before creating new ones
            print("\n🧹 Cleaning up old Town Hall nodes...")
            old_th_nodes = [n for n in existing_nodes if 
                           n.get('id', '').startswith('project::Town Hall') or 
                           n.get('id', '').startswith('event::Town Hall')]
            if old_th_nodes:
                print(f"   Found {len(old_th_nodes)} old Town Hall nodes to remove")
                # Remove from node list
                existing_nodes = [n for n in existing_nodes if n.get('id', '') not in [node['id'] for node in old_th_nodes]]
                # Remove edges connected to old nodes
                old_th_ids = {n['id'] for n in old_th_nodes}
                existing_edges = [e for e in existing_edges if e.get('source', '') not in old_th_ids and e.get('target', '') not in old_th_ids]
                print(f"   ✅ Removed {len(old_th_nodes)} old nodes and their edges")
            else:
                print(f"   No old Town Hall nodes found")
            
            # Update existing_node_ids set
            existing_node_ids = {n.get('id', '') for n in existing_nodes}
            
            # Query Town Halls
            meetings = self.query_town_halls()
            if not meetings:
                print("\n⚠️  No Town Hall meetings found")
                return True
            
            # Create nodes and edges
            new_nodes, new_edges = self.create_nodes_and_edges(meetings, existing_node_ids)
            
            # Write to sheet
            self.write_to_sheet(new_nodes, new_edges, existing_nodes, existing_edges)
            
            # Report
            self.generate_report()
            
            return True
        
        finally:
            if self.conn:
                self.conn.close()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Export Town Hall meetings to Landscape')
    parser.add_argument('--limit', type=int, default=2, help='Number of meetings to export (default: 2 for testing)')
    args = parser.parse_args()
    
    exporter = TownHallExporter(
        sheet_id=SHEET_ID,
        db_path=DB_PATH,
        token_path=TOKEN_PATH,
        limit=args.limit
    )
    
    success = exporter.run()
    
    print("\n🎯 Next Steps:")
    print("   1. Visit live site and search for 'Town Hall'")
    print("   2. Verify meeting chain structure")
    print("   3. Check person→meeting connections")
    print("   4. If successful, increase --limit to export more meetings")
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
