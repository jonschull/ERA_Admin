#!/usr/bin/env python3
"""
Merge Mahangi Munanse with Muhangi Musinga (same person, duplicate records).

Actions:
1. Delete Mahangi Munanse from Airtable
2. Update database: Mahangi Munanse → Muhangi Musinga
3. Verify merge
"""

import sys
import sqlite3
from pathlib import Path

# Add airtable module
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'airtable'))

from pyairtable import Api
from config import AIRTABLE_CONFIG

# Initialize Airtable
api = Api(AIRTABLE_CONFIG['api_key'])
table = api.table(AIRTABLE_CONFIG['base_id'], AIRTABLE_CONFIG['tables']['people'])

# Database path
DB_PATH = Path(__file__).parent.parent.parent / 'FathomInventory' / 'fathom_emails.db'

MAHANGI_ID = 'recjmTo1C7JGqdZYs'
MUHANGI_ID = 'reckJ82HydeOio4eV'

def main():
    print("=" * 80)
    print("MERGING DUPLICATE: Mahangi Munanse → Muhangi Musinga")
    print("=" * 80)
    print()
    
    print("Records:")
    print("  - Mahangi Munanse (recjmTo1C7JGqdZYs) - iptowncrush@gmail.com - NO bio")
    print("  - Muhangi Musinga (reckJ82HydeOio4eV) - mmusinga32@gmail.com - HAS bio, published")
    print()
    print("Keeping: Muhangi Musinga (has bio)")
    print()
    
    # Step 1: Delete Mahangi Munanse from Airtable
    print("1. Deleting Mahangi Munanse from Airtable...")
    try:
        table.delete(MAHANGI_ID)
        print("   ✅ Deleted from Airtable")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 1
    
    print()
    
    # Step 2: Update database
    print("2. Updating database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check current state
    cursor.execute("SELECT name, email, bio FROM participants WHERE name IN ('Mahangi Munanse', 'Muhangi Musinga')")
    results = cursor.fetchall()
    
    print("   Current database records:")
    for name, email, bio in results:
        has_bio = "has bio" if bio else "no bio"
        print(f"     - {name} ({email}) - {has_bio}")
    print()
    
    # Update Mahangi Munanse → Muhangi Musinga
    print("   Renaming 'Mahangi Munanse' → 'Muhangi Musinga' in database...")
    try:
        cursor.execute("""
            UPDATE participants 
            SET name = 'Muhangi Musinga',
                email = 'mmusinga32@gmail.com',
                airtable_id = ?
            WHERE name = 'Mahangi Munanse'
        """, (MUHANGI_ID,))
        
        rows_updated = cursor.rowcount
        conn.commit()
        
        print(f"   ✅ Updated {rows_updated} database record(s)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        conn.rollback()
        return 1
    
    print()
    
    # Step 3: Verify
    print("3. Verifying merge...")
    
    # Check Airtable record count
    cursor.execute("SELECT COUNT(*) FROM participants WHERE name = 'Mahangi Munanse'")
    mahangi_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM participants WHERE name = 'Muhangi Musinga'")
    muhangi_count = cursor.fetchone()[0]
    
    print(f"   Database records:")
    print(f"     - Mahangi Munanse: {mahangi_count} (should be 0)")
    print(f"     - Muhangi Musinga: {muhangi_count}")
    
    conn.close()
    
    print()
    
    if mahangi_count == 0:
        print("=" * 80)
        print("✅ MERGE COMPLETE")
        print("=" * 80)
        print()
        print("Muhangi Musinga now has:")
        print("  - All Town Hall attendance records")
        print("  - Bio (already existed)")
        print("  - Published status in Airtable")
        return 0
    else:
        print("⚠️  Warning: Mahangi Munanse still exists in database")
        return 1


if __name__ == '__main__':
    sys.exit(main())
