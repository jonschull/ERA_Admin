#!/usr/bin/env python3
"""
Add people to Airtable CSV from Fathom database.

This allows automated addition of verified ERA participants to Airtable.
"""

import csv
import sqlite3
from pathlib import Path
from datetime import datetime
import shutil

# Paths
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent / "FathomInventory" / "fathom_emails.db"
AIRTABLE_CSV = SCRIPT_DIR.parent / "airtable" / "people_export.csv"
BACKUP_DIR = SCRIPT_DIR.parent / "airtable" / "backups"


def backup_airtable_csv():
    """Backup Airtable CSV before modifying."""
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    backup_path = BACKUP_DIR / f"people_export.backup_{timestamp}.csv"
    shutil.copy2(AIRTABLE_CSV, backup_path)
    print(f"💾 Airtable backup: {backup_path.name}")
    return backup_path


def get_fathom_person_data(name, conn):
    """Get person's data from Fathom database."""
    cursor = conn.cursor()
    
    # Get best/most complete record for this person
    cursor.execute("""
        SELECT 
            name,
            email,
            location,
            affiliation,
            source_call_title,
            source_call_url
        FROM participants 
        WHERE name = ?
        ORDER BY 
            CASE WHEN location != 'Unknown' THEN 1 ELSE 0 END DESC,
            CASE WHEN affiliation NOT LIKE '%not listed%' THEN 1 ELSE 0 END DESC,
            CASE WHEN email IS NOT NULL THEN 1 ELSE 0 END DESC
        LIMIT 1
    """, (name,))
    
    row = cursor.fetchone()
    if not row:
        return None
    
    return {
        'name': row[0],
        'email': row[1],
        'location': row[2] if row[2] and row[2] != 'Unknown' else '',
        'affiliation': row[3] if row[3] and 'not listed' not in row[3] else '',
        'source_call_title': row[4] if row[4] else '',
        'source_call_url': row[5] if row[5] else '',
    }


def parse_name_parts(full_name):
    """Parse full name into first and last name."""
    parts = full_name.strip().split()
    if len(parts) == 0:
        return '', ''
    elif len(parts) == 1:
        return parts[0], ''
    else:
        return parts[0], ' '.join(parts[1:])


def create_airtable_row(person_data, is_member=True, notes=''):
    """Create Airtable CSV row from person data."""
    
    first_name, last_name = parse_name_parts(person_data['name'])
    
    # Parse location into country/city if possible
    location = person_data.get('location', '')
    country = ''
    city = ''
    
    if location:
        # Common patterns: "City, Country" or "Country"
        parts = [p.strip() for p in location.split(',')]
        if len(parts) >= 2:
            city = parts[0]
            country = parts[-1]
        elif len(parts) == 1:
            # Could be country or city - make a guess
            if any(word in parts[0].lower() for word in ['ghana', 'uganda', 'kenya', 'california', 'africa']):
                country = parts[0]
            else:
                city = parts[0]
    
    # Detect ERA Africa membership from notes
    is_era_africa = 'era africa' in notes.lower()
    
    # Create minimal but complete row
    now = datetime.now().isoformat() + 'Z'
    
    row = {
        'airtable_id': '',  # Will be assigned by Airtable
        'created_time': now,
        'last_modified': now,
        'Name': person_data['name'],
        'First Name': first_name,
        'Last Name': last_name,
        'Email': person_data.get('email', ''),
        'Country': country,
        'City Town': city,
        'Location': location,
        'Affiliated Orgs': person_data.get('affiliation', ''),
        'Bio': '',  # Leave empty - Bio is for biographical info, not provenance
        'era Member': 'True' if is_member else '',
        'ERA Africa': 'True' if is_era_africa else '',  # NEW: ERA Africa flag
        'Provenance': f"Fathom AI → Phase 4B-2 ({datetime.now().strftime('%Y-%m-%d')})",
        'PubURL': person_data.get('source_call_url', ''),
        'Comments': f"Source: {person_data.get('source_call_title', '')}",
        'Publish': 'True',  # Make visible in public directory
    }
    
    return row


def add_people_to_airtable(people_to_add, conn):
    """
    Add multiple people to Airtable CSV.
    
    Args:
        people_to_add: List of dicts with 'name', 'is_member', 'notes'
        conn: SQLite connection to Fathom database
    """
    
    print("\n" + "=" * 80)
    print("➕ ADDING PEOPLE TO AIRTABLE")
    print("=" * 80)
    
    # Backup Airtable CSV
    backup_airtable_csv()
    
    # Read existing Airtable CSV
    with open(AIRTABLE_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        existing_rows = list(reader)
    
    existing_names = {row['Name'] for row in existing_rows if row.get('Name')}
    
    print(f"\n📊 Existing Airtable people: {len(existing_names)}")
    
    # Process each person to add
    added = []
    skipped = []
    
    for person in people_to_add:
        name = person['name']
        
        # Check if already exists
        if name in existing_names:
            print(f"   ⏭️  '{name}' - Already in Airtable, skipping")
            skipped.append(name)
            continue
        
        # Get data from Fathom
        person_data = get_fathom_person_data(name, conn)
        if not person_data:
            print(f"   ⚠️  '{name}' - Not found in Fathom database")
            skipped.append(name)
            continue
        
        # Create Airtable row
        is_member = person.get('is_member', True)
        notes = person.get('notes', '')
        
        new_row = create_airtable_row(person_data, is_member, notes)
        
        # Fill in all missing fields with empty strings
        for field in fieldnames:
            if field not in new_row:
                new_row[field] = ''
        
        existing_rows.append(new_row)
        added.append(name)
        
        print(f"   ✅ Added '{name}'")
        if person_data.get('email'):
            print(f"      Email: {person_data['email']}")
        if person_data.get('location'):
            print(f"      Location: {person_data['location']}")
    
    # Write updated CSV
    if added:
        # Filter out any fields not in fieldnames from all rows
        filtered_rows = []
        for row in existing_rows:
            filtered_row = {k: v for k, v in row.items() if k in fieldnames}
            filtered_rows.append(filtered_row)
        
        with open(AIRTABLE_CSV, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_rows)
        
    if added:
        print(f"\n✅ Added {len(added)} people to Airtable CSV")
        print(f"📄 Updated: {AIRTABLE_CSV}")
    else:
        print("\n⚠️  No people added")
    
    return added, skipped


def update_fathom_validated(names, conn):
    """Mark people as validated in Fathom database."""
    cursor = conn.cursor()
    
    for name in names:
        cursor.execute("""
            UPDATE participants
            SET validated_by_airtable = 1,
                era_member = 1
            WHERE name = ?
        """, (name,))
    
    conn.commit()
    print(f"\n✅ Marked {len(names)} people as validated in Fathom database")


def main():
    """Standalone execution for testing."""
    print("\n" + "=" * 80)
    print("ADD TO AIRTABLE - Standalone Test")
    print("=" * 80)
    
    # Example: Add the 5 people from Phase 4B-2
    test_people = [
        {'name': 'Hashim Yussif', 'is_member': True, 'notes': 'ERA Africa member'},
        {'name': 'Byamukama nyansio', 'is_member': True, 'notes': 'ERA Africa member'},
        {'name': 'Kriss Scioneaux', 'is_member': True, 'notes': 'ERA Member'},
        {'name': 'Matthew Hotsko', 'is_member': False, 'notes': 'ERA participant (not member)'},
        {'name': 'Alisa Keesey', 'is_member': True, 'notes': 'ERA Africa member'},
    ]
    
    # Connect to Fathom DB
    conn = sqlite3.connect(DB_PATH)
    
    try:
        added, skipped = add_people_to_airtable(test_people, conn)
        
        if added:
            update_fathom_validated(added, conn)
        
        print("\n" + "=" * 80)
        print("✅ COMPLETE")
        print("=" * 80)
        print(f"   Added: {len(added)}")
        print(f"   Skipped: {len(skipped)}")
        
    finally:
        conn.close()


if __name__ == "__main__":
    main()
