#!/usr/bin/env python3
"""
Town Hall Agenda Search System

Searches Town Hall agendas for participant names.
Now uses local database cache for instant searches (no Google Drive API calls).

To populate cache: python3 download_town_hall_agendas.py
"""

import json
import re
import sqlite3
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

DB_PATH = '../FathomInventory/fathom_emails.db'

class TownHallSearch:
    def __init__(self, use_local_db=True):
        """
        Initialize Town Hall search.
        
        Args:
            use_local_db: If True, search local database (fast, no API calls).
                         If False, download from Google Drive each time (slow).
        """
        self.use_local_db = use_local_db
        
        if use_local_db:
            # Connect to local database
            self.db_conn = sqlite3.connect(DB_PATH)
        else:
            # Load Google Drive credentials (legacy mode)
            self.creds = Credentials.from_authorized_user_file('token_jschull_drive.json')
            self.service = build('drive', 'v3', credentials=self.creds)
            
            # Load agenda index
            with open('town_hall_agenda_index.json', 'r') as f:
                self.agenda_index = json.load(f)
    
    def search_agendas_for_name(self, name, max_results=5):
        """
        Search Town Hall agendas for a person's name.
        Returns list of agendas where name appears.
        """
        if self.use_local_db:
            return self._search_local_db(name, max_results)
        else:
            return self._search_google_drive(name, max_results)
    
    def _search_local_db(self, name, max_results=5):
        """Search local database using full-text search."""
        cursor = self.db_conn.cursor()
        
        # Try different name variations
        search_terms = self._get_name_variations(name)
        
        results = []
        for term in search_terms:
            # FTS5 full-text search - quote term to handle special chars like hyphens
            # FTS5 treats hyphens as NOT operators, so wrap in quotes
            quoted_term = f'"{term}"'
            
            cursor.execute("""
                SELECT 
                    a.agenda_id,
                    a.meeting_title,
                    a.meeting_date,
                    snippet(agenda_search, 2, '**', '**', '...', 60) as snippet
                FROM agenda_search s
                JOIN town_hall_agendas a ON s.agenda_id = a.agenda_id
                WHERE agenda_search MATCH ?
                LIMIT ?
            """, (quoted_term, max_results))
            
            for row in cursor.fetchall():
                results.append({
                    'id': row[0],
                    'title': row[1],
                    'date': row[2],
                    'snippet': row[3],
                    'source': 'local_db'
                })
            
            if results:
                break  # Found matches with this variation
        
        return results[:max_results]
    
    def _get_name_variations(self, name):
        """Generate search term variations for a name."""
        search_name = name.lower()
        name_parts = search_name.split()
        search_terms = [search_name]
        
        if len(name_parts) >= 2:
            # Try first + last name
            search_terms.append(f"{name_parts[0]} {name_parts[-1]}")
            # Try just last name
            search_terms.append(name_parts[-1])
        
        return search_terms
    
    def _search_google_drive(self, name, max_results=5):
        """Legacy: Search by downloading from Google Drive (slow)."""
        results = []
        search_name = name.lower()
        
        # Try different name variations
        search_terms = self._get_name_variations(name)
        
        for agenda in self.agenda_index:
            # Can only search title without downloading
            if any(term in agenda['name'].lower() for term in search_terms):
                results.append(agenda)
                if len(results) >= max_results:
                    break
        
        return results
    
    def get_agenda_by_date(self, date_str):
        """
        Get agenda for a specific date (YYYY-MM-DD format).
        Returns agenda info or None if not found.
        """
        for agenda in self.agenda_index:
            if agenda['date'] == date_str:
                return agenda
        return None
    
    def get_recent_agendas(self, count=10):
        """
        Get the most recent Town Hall agendas.
        """
        return self.agenda_index[:count]
    
    def download_agenda_text(self, agenda_id, as_markdown=True):
        """
        Download agenda text from Google Drive.
        
        Args:
            agenda_id: Google Drive file ID
            as_markdown: If True, export as Markdown (preserves formatting)
                        If False, export as plain text
        
        Returns the text content of the agenda.
        """
        try:
            # Export as markdown (preserves structure) or plain text
            mime_type = 'text/markdown' if as_markdown else 'text/plain'
            request = self.service.files().export_media(
                fileId=agenda_id,
                mimeType=mime_type
            )
            
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            
            while not done:
                status, done = downloader.next_chunk()
            
            text = fh.getvalue().decode('utf-8')
            return text
        except Exception as e:
            print(f"Error downloading agenda {agenda_id}: {e}")
            return None
    
    def search_agenda_text_for_name(self, agenda_id, name):
        """
        Download agenda and search for name in text.
        Returns True if found, False otherwise.
        """
        text = self.download_agenda_text(agenda_id)
        if not text:
            return False
        
        # Search for name (case insensitive)
        return name.lower() in text.lower()


def search_for_participant(name):
    """
    Helper function: Search Town Hall agendas for a participant name.
    Returns formatted results for display.
    """
    searcher = TownHallSearch()
    
    # Get recent agendas (within last 2 years)
    recent_agendas = searcher.get_recent_agendas(count=20)
    
    results = []
    for agenda in recent_agendas:
        # Download and search each agenda
        if searcher.search_agenda_text_for_name(agenda['id'], name):
            results.append({
                'date': agenda['date'],
                'name': agenda['name'],
                'link': agenda['link']
            })
    
    return results


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python town_hall_search.py <name>")
        sys.exit(1)
    
    name = ' '.join(sys.argv[1:])
    print(f"🔍 Searching Town Hall agendas for: {name}\n")
    
    results = search_for_participant(name)
    
    if results:
        print(f"✅ Found {len(results)} agendas mentioning '{name}':\n")
        for r in results:
            print(f"  • {r['date']}: {r['name']}")
            print(f"    {r['link']}\n")
    else:
        print(f"❌ No agendas found mentioning '{name}'")
