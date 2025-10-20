#!/usr/bin/env python3
"""
Backfill public_share_url in calls table from existing emails.

Matches emails to calls by title and date, then populates the public URL.
"""
import sqlite3
import argparse
from datetime import datetime

DEFAULT_DB = "fathom_emails.db"


def normalize_title(title):
    """Normalize title for matching."""
    if not title:
        return ""
    # Remove common variations
    return title.strip().lower().replace("  ", " ")


def normalize_date(date_str):
    """Try to normalize dates to comparable format."""
    if not date_str:
        return ""
    
    # Try common formats
    formats = [
        "%b %d, %Y",      # Oct 1, 2025
        "%B %d, %Y",      # October 1, 2025
        "%Y-%m-%d",       # 2025-10-01
        "%m/%d/%Y",       # 10/1/2025
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%Y-%m-%d")  # Canonical format
        except ValueError:
            continue
    
    # If parsing fails, return original for fuzzy matching
    return date_str.strip().lower()


def backfill_public_urls(db_path, dry_run=False):
    """Match emails to calls and populate public URLs."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all emails with public URLs
    cursor.execute("""
        SELECT meeting_title, meeting_date, meeting_url 
        FROM emails 
        WHERE meeting_url IS NOT NULL AND meeting_url != ''
    """)
    emails = cursor.fetchall()
    
    print(f"Found {len(emails)} emails with public URLs")
    
    # Get all calls
    cursor.execute("""
        SELECT rowid, title, date, public_share_url
        FROM calls
    """)
    calls = cursor.fetchall()
    
    print(f"Found {len(calls)} calls")
    
    matches = 0
    updates = 0
    
    # Match emails to calls
    for email in emails:
        email_title_norm = normalize_title(email['meeting_title'])
        email_date_norm = normalize_date(email['meeting_date'])
        
        for call in calls:
            call_title_norm = normalize_title(call['title'])
            call_date_norm = normalize_date(call['date'])
            
            # Match on normalized title and date
            if email_title_norm == call_title_norm and email_date_norm == call_date_norm:
                matches += 1
                
                # Only update if not already set
                if not call['public_share_url']:
                    if not dry_run:
                        cursor.execute("""
                            UPDATE calls 
                            SET public_share_url = ? 
                            WHERE rowid = ?
                        """, (email['meeting_url'], call['rowid']))
                    updates += 1
                    print(f"  ✓ Matched: {call['title'][:50]} ({call['date']})")
    
    if not dry_run:
        conn.commit()
        print(f"\n✅ Updated {updates} calls with public URLs")
    else:
        print(f"\n🔍 Dry run: Would update {updates} calls")
    
    print(f"   Total matches: {matches}")
    print(f"   Already had URLs: {matches - updates}")
    
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backfill public URLs in calls table")
    parser.add_argument("--db", default=DEFAULT_DB, help="Database file")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be updated without making changes")
    
    args = parser.parse_args()
    backfill_public_urls(args.db, dry_run=args.dry_run)
