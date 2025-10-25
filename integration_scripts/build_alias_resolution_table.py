#!/usr/bin/env python3
"""
Build Fathom Alias Resolution Table

PURPOSE:
    Extract alias-to-person resolutions from Phase 4B-2 decisions and create
    a database table that preserves meeting context. Enables queries like
    "show me all of Brian Kravitz's sessions" which returns meetings where
    he appeared as "Brian Kravitz", "bk", "brian", etc.

CONTEXT:
    During Phase 4B-2, we resolved ambiguous Fathom names to real people.
    These resolutions are context-dependent: "bk" might be Brian Kravitz in
    one meeting and Bob King in another. We need to preserve this context.

INPUT:
    - integration_scripts/past_decisions/phase4b2_approvals_*.csv
    - integration_scripts/past_batches/BATCH*.html (for meeting URLs)

OUTPUT:
    - FathomInventory/fathom_emails.db with new table:
      * fathom_alias_resolutions
    - View: participant_meetings (for easy querying)

USAGE:
    python build_alias_resolution_table.py
    
AUTHOR: ERA Admin / Cascade AI
DATE: 2025-10-25
"""

import sqlite3
import csv
import re
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

DB_PATH = Path("../FathomInventory/fathom_emails.db")
CSV_DIR = Path("past_decisions")
HTML_DIR = Path("past_batches")

def create_alias_table(conn):
    """Create the alias resolution table and helper view"""
    
    # Drop existing if present
    conn.execute("DROP TABLE IF EXISTS fathom_alias_resolutions")
    conn.execute("DROP VIEW IF EXISTS participant_meetings")
    
    # Create main table
    conn.execute("""
        CREATE TABLE fathom_alias_resolutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fathom_name TEXT NOT NULL,           -- What Fathom displayed: "bk"
            meeting_url TEXT,                    -- In which meeting (NULL if unknown)
            resolved_to TEXT,                    -- Who it actually was: "Brian Kravitz"
            decision_type TEXT,                  -- "merge", "add", "drop"
            decision_source TEXT,                -- Which batch CSV
            resolved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indexes
    conn.execute("CREATE INDEX idx_alias_fathom_name ON fathom_alias_resolutions(fathom_name)")
    conn.execute("CREATE INDEX idx_alias_resolved_to ON fathom_alias_resolutions(resolved_to)")
    conn.execute("CREATE INDEX idx_alias_meeting ON fathom_alias_resolutions(meeting_url)")
    
    # Create helper view for easy querying
    conn.execute("""
        CREATE VIEW participant_meetings AS
        SELECT DISTINCT
            far.resolved_to AS participant_name,
            far.meeting_url,
            far.fathom_name AS appeared_as,
            c.title AS meeting_title,
            c.date AS meeting_date,
            far.decision_type
        FROM fathom_alias_resolutions far
        LEFT JOIN calls c ON far.meeting_url = c.hyperlink
        WHERE far.resolved_to IS NOT NULL
        ORDER BY c.date DESC
    """)
    
    conn.commit()
    print("✅ Created fathom_alias_resolutions table and participant_meetings view")


def extract_html_meeting_urls(batch_name):
    """Extract Fathom URLs from batch HTML file"""
    
    # Find the HTML file
    html_files = list(HTML_DIR.glob(f"*{batch_name}*.html"))
    if not html_files:
        print(f"  ⚠️  No HTML file found for {batch_name}")
        return {}
    
    html_file = html_files[0]  # Take first match
    
    try:
        soup = BeautifulSoup(html_file.read_text(), 'html.parser')
        name_to_urls = {}
        
        # Each row has name in <strong> and Fathom URLs in evidence links
        for row in soup.find_all('tr'):
            # Find the name
            name_elem = row.find('strong')
            if not name_elem:
                continue
            name = name_elem.text.strip()
            
            # Find Fathom call URLs (🎥 links)
            evidence_cell = row.find('td', style=lambda x: x and 'font-size:11px' in x)
            if not evidence_cell:
                continue
            
            # Extract all fathom.video URLs
            fathom_urls = []
            for link in evidence_cell.find_all('a', href=True):
                href = link['href']
                if 'fathom.video/calls/' in href:
                    # May be comma-separated
                    urls = [u.strip() for u in href.split(',')]
                    fathom_urls.extend(urls)
            
            if fathom_urls:
                name_to_urls[name] = fathom_urls
        
        print(f"  📄 Extracted {len(name_to_urls)} names with URLs from {html_file.name}")
        return name_to_urls
        
    except Exception as e:
        print(f"  ⚠️  Error parsing {html_file.name}: {e}")
        return {}


def parse_decision(comment):
    """Parse decision from Comments field"""
    comment = comment.strip()
    
    if comment.lower() == 'drop':
        return 'drop', None
    
    # "merge with: Brian Kravitz"
    merge_match = re.match(r'merge with:\s*(.+)', comment, re.IGNORECASE)
    if merge_match:
        return 'merge', merge_match.group(1).strip()
    
    # "add to airtable as Andrea Miller (...)"
    add_as_match = re.match(r'add to airtable as\s*([^(]+)', comment, re.IGNORECASE)
    if add_as_match:
        return 'add', add_as_match.group(1).strip()
    
    # "add to airtable"
    if 'add to airtable' in comment.lower():
        return 'add', None  # Name is same as Fathom name
    
    return 'unknown', None


def process_batch_csv(csv_file, conn):
    """Process one batch CSV file"""
    
    batch_name = csv_file.stem  # e.g., "phase4b2_approvals_batch3_20251023"
    print(f"\n📋 Processing {csv_file.name}...")
    
    # Extract meeting URLs from HTML
    html_urls = extract_html_meeting_urls(batch_name)
    
    # Read CSV
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    inserted = 0
    skipped = 0
    
    for row in rows:
        fathom_name = row.get('Fathom_Name', '').strip()
        comments = row.get('Comments', '').strip()
        process = row.get('ProcessThis', '').strip()
        
        if not fathom_name or process.upper() != 'YES':
            continue
        
        # Parse decision
        decision_type, resolved_to = parse_decision(comments)
        
        # If no explicit resolved_to and it's "add", use fathom_name
        if decision_type == 'add' and not resolved_to:
            resolved_to = fathom_name
        
        # Get meeting URLs for this name
        meeting_urls = html_urls.get(fathom_name, [])
        
        if not meeting_urls:
            # Still record it without URL (might be from calls outside Town Halls)
            meeting_urls = [None]
        
        # Insert one row per meeting URL
        for url in meeting_urls:
            try:
                conn.execute("""
                    INSERT INTO fathom_alias_resolutions
                    (fathom_name, meeting_url, resolved_to, decision_type, decision_source)
                    VALUES (?, ?, ?, ?, ?)
                """, (fathom_name, url, resolved_to, decision_type, csv_file.name))
                inserted += 1
            except sqlite3.IntegrityError:
                # Duplicate - update if needed
                conn.execute("""
                    UPDATE fathom_alias_resolutions
                    SET resolved_to = ?, decision_type = ?, decision_source = ?
                    WHERE fathom_name = ? AND (meeting_url = ? OR (meeting_url IS NULL AND ? IS NULL))
                """, (resolved_to, decision_type, csv_file.name, fathom_name, url, url))
                inserted += 1
            except Exception as e:
                print(f"    ⚠️  Error inserting {fathom_name}: {e}")
                skipped += 1
    
    conn.commit()
    print(f"  ✅ Inserted {inserted} resolutions, skipped {skipped}")


def generate_report(conn):
    """Generate summary report"""
    
    print("\n" + "="*60)
    print("📊 ALIAS RESOLUTION TABLE SUMMARY")
    print("="*60)
    
    # Total resolutions
    total = conn.execute("SELECT COUNT(*) FROM fathom_alias_resolutions").fetchone()[0]
    print(f"\n✅ Total resolutions: {total}")
    
    # By decision type
    print("\n📈 By decision type:")
    for row in conn.execute("""
        SELECT decision_type, COUNT(*) as count
        FROM fathom_alias_resolutions
        GROUP BY decision_type
        ORDER BY count DESC
    """):
        print(f"   {row[0]:12} {row[1]:5} resolutions")
    
    # People with most aliases
    print("\n👥 People with most aliases:")
    for row in conn.execute("""
        SELECT resolved_to, COUNT(DISTINCT fathom_name) as alias_count
        FROM fathom_alias_resolutions
        WHERE resolved_to IS NOT NULL
        GROUP BY resolved_to
        ORDER BY alias_count DESC
        LIMIT 10
    """):
        print(f"   {row[0]:30} {row[1]:3} aliases")
    
    # Most ambiguous aliases (same alias → multiple people)
    print("\n🔀 Most ambiguous aliases:")
    for row in conn.execute("""
        SELECT fathom_name, COUNT(DISTINCT resolved_to) as person_count
        FROM fathom_alias_resolutions
        WHERE resolved_to IS NOT NULL
        GROUP BY fathom_name
        HAVING person_count > 1
        ORDER BY person_count DESC
        LIMIT 10
    """):
        print(f"   '{row[0]}' → {row[1]} different people")
    
    print("\n" + "="*60)


def demo_queries(conn):
    """Show example queries"""
    
    print("\n📝 EXAMPLE QUERIES:")
    print("="*60)
    
    # Find Brian Kravitz's sessions
    print("\n1️⃣ Find all of Brian Kravitz's sessions:")
    print("   SELECT * FROM participant_meetings")
    print("   WHERE participant_name = 'Brian Kravitz'")
    print("   ORDER BY meeting_date;")
    
    result = conn.execute("""
        SELECT appeared_as, meeting_date, meeting_title
        FROM participant_meetings
        WHERE participant_name = 'Brian Kravitz'
        ORDER BY meeting_date
        LIMIT 5
    """).fetchall()
    
    if result:
        print(f"\n   Found {len(result)} meetings (showing first 5):")
        for row in result:
            print(f"     • {row[1] or 'Unknown date'}: appeared as '{row[0]}'")
    
    # Check if "bk" is ambiguous
    print("\n\n2️⃣ Who is 'bk' in different meetings:")
    print("   SELECT meeting_url, resolved_to")
    print("   FROM fathom_alias_resolutions")
    print("   WHERE fathom_name = 'bk';")
    
    result = conn.execute("""
        SELECT meeting_url, resolved_to
        FROM fathom_alias_resolutions
        WHERE fathom_name = 'bk'
    """).fetchall()
    
    if result:
        print(f"\n   'bk' appears in {len(result)} meetings:")
        for row in result:
            print(f"     • {row[0] or 'Unknown meeting'}: {row[1] or 'dropped'}")
    
    print("\n" + "="*60)


def main():
    """Main execution"""
    
    print("="*60)
    print("🔨 Building Fathom Alias Resolution Table")
    print("="*60)
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    
    # Create table
    create_alias_table(conn)
    
    # Process all CSV files
    csv_files = sorted(CSV_DIR.glob("phase4b2_approvals_*.csv"))
    print(f"\n📁 Found {len(csv_files)} CSV files to process")
    
    for csv_file in csv_files:
        process_batch_csv(csv_file, conn)
    
    # Generate report
    generate_report(conn)
    
    # Show example queries
    demo_queries(conn)
    
    conn.close()
    
    print("\n✅ Done! Database updated at:")
    print(f"   {DB_PATH.absolute()}")


if __name__ == '__main__':
    main()
