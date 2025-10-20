"""Database I/O utilities for the calls table.

Provides an interface matching tsv_io.py for easy drop-in replacement.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import List, Dict

DEFAULT_DB_FILE = "fathom_emails.db"


def read_calls_from_db(db_path: str = DEFAULT_DB_FILE) -> List[Dict[str, str]]:
    """Read all calls from the database.
    
    Returns a list of dictionaries with keys matching TSV format:
    - Title, Date, Duration, Hyperlink, shareStatus, sharedWith, shareTimestamp
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='calls'
    """)
    if not cursor.fetchone():
        conn.close()
        return []
    
    cursor.execute("""
        SELECT 
            title, 
            date, 
            duration, 
            hyperlink, 
            share_status, 
            shared_with, 
            share_timestamp
        FROM calls
        ORDER BY created_at DESC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to TSV-compatible format (match keys exactly)
    return [
        {
            'Title': row['title'] or '',
            'Date': row['date'] or '',
            'Duration': row['duration'] or '',
            'Hyperlink': row['hyperlink'] or '',
            'shareStatus': row['share_status'] or '',
            'sharedWith': row['shared_with'] or '',
            'shareTimestamp': row['share_timestamp'] or ''
        }
        for row in rows
    ]


def write_calls_to_db(records: List[Dict[str, str]], db_path: str = DEFAULT_DB_FILE) -> None:
    """Write/update calls in the database.
    
    Accepts dictionaries with TSV-format keys:
    - Title, Date, Duration, Hyperlink, shareStatus, sharedWith, shareTimestamp
    
    Uses UPSERT (INSERT OR REPLACE) based on hyperlink as primary key.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ensure table exists (safe due to IF NOT EXISTS)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calls (
            hyperlink TEXT PRIMARY KEY,
            title TEXT,
            date TEXT,
            duration TEXT,
            share_status TEXT DEFAULT '',
            shared_with TEXT,
            share_timestamp TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Upsert each record
    for record in records:
        cursor.execute("""
            INSERT OR REPLACE INTO calls 
            (hyperlink, title, date, duration, share_status, shared_with, share_timestamp, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, COALESCE(
                (SELECT created_at FROM calls WHERE hyperlink = ?),
                ?
            ))
        """, (
            record.get('Hyperlink', ''),
            record.get('Title', ''),
            record.get('Date', ''),
            record.get('Duration', ''),
            record.get('shareStatus', ''),
            record.get('sharedWith', ''),
            record.get('shareTimestamp', ''),
            record.get('Hyperlink', ''),  # for COALESCE subquery
            datetime.now().isoformat()  # fallback if new record
        ))
    
    conn.commit()
    conn.close()


def get_existing_hyperlinks(db_path: str = DEFAULT_DB_FILE) -> set:
    """Return set of all hyperlinks in the database.
    
    Used for deduplication during scraping.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='calls'")
    if not cursor.fetchone():
        conn.close()
        return set()
    
    cursor.execute("SELECT hyperlink FROM calls WHERE hyperlink IS NOT NULL AND hyperlink != ''")
    hyperlinks = {row[0] for row in cursor.fetchall()}
    conn.close()
    
    return hyperlinks
