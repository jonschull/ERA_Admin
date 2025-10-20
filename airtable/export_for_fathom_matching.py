#!/usr/bin/env python3
"""
Export Airtable People data optimized for cross-correlation with Fathom participants.
Focuses on name standardization and matching-relevant fields.
"""

import csv
import re
from datetime import datetime
from pathlib import Path
from pyairtable import Api
from config import AIRTABLE_CONFIG, EXPORT_CONFIG, MATCHING_CONFIG

def clean_name(name):
    """Clean and standardize name for matching."""
    if not name:
        return ""
    
    # Remove extra whitespace and normalize
    name = re.sub(r'\s+', ' ', name.strip())
    
    # Handle common variations
    for standard, variations in MATCHING_CONFIG['common_name_variations'].items():
        for variation in variations:
            # Replace whole word variations
            pattern = r'\b' + re.escape(variation) + r'\b'
            name = re.sub(pattern, standard, name, flags=re.IGNORECASE)
    
    return name

def extract_name_parts(full_name):
    """Extract first and last name from full name."""
    if not full_name:
        return "", ""
    
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0], ""
    elif len(parts) == 2:
        return parts[0], parts[1]
    else:
        # More than 2 parts - first name is first part, last name is last part
        return parts[0], parts[-1]

def export_for_matching():
    """Export People data optimized for name matching with Fathom data."""
    print("🔄 Connecting to Airtable for matching export...")
    
    try:
        # Initialize Airtable API
        api = Api(AIRTABLE_CONFIG['api_key'])
        table = api.table(AIRTABLE_CONFIG['base_id'], AIRTABLE_CONFIG['tables']['people'])
        
        print("📥 Fetching records for matching...")
        records = table.all()
        
        if not records:
            print("❌ No records found")
            return False
        
        print(f"✅ Processing {len(records)} records for matching...")
        
        # Process records for matching
        matching_data = []
        stats = {
            'total_records': len(records),
            'records_with_names': 0,
            'records_with_emails': 0,
            'donors': 0,
            'name_variations_applied': 0
        }
        
        for record in records:
            fields = record['fields']
            
            # Get primary name field
            name = fields.get('Name', '')
            if not name:
                continue
            
            stats['records_with_names'] += 1
            
            # Clean and standardize name
            original_name = name
            cleaned_name = clean_name(name)
            if cleaned_name != original_name:
                stats['name_variations_applied'] += 1
            
            # Extract name parts
            first_name, last_name = extract_name_parts(cleaned_name)
            
            # Collect other relevant fields
            email = fields.get('Email', '')
            if email:
                stats['records_with_emails'] += 1
            
            is_donor = bool(fields.get('Donor Flag', False))
            if is_donor:
                stats['donors'] += 1
            
            # Create matching record
            matching_record = {
                'airtable_id': record['id'],
                'original_name': original_name,
                'cleaned_name': cleaned_name,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'is_donor': is_donor,
                'member_status': fields.get('Member Status', ''),
                'organization': fields.get('Organization', ''),
                'location': fields.get('Location', ''),
                'phone': fields.get('Phone', ''),
                'notes': fields.get('Notes', ''),
                'created_time': record.get('createdTime', ''),
                'last_modified': record.get('lastModifiedTime', '')
            }
            
            matching_data.append(matching_record)
        
        # Write to CSV
        csv_file = EXPORT_CONFIG['people_matching_csv']
        print(f"📝 Writing {len(matching_data)} records to {csv_file}...")
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'airtable_id', 'original_name', 'cleaned_name', 'first_name', 'last_name',
                'email', 'is_donor', 'member_status', 'organization', 'location', 
                'phone', 'notes', 'created_time', 'last_modified'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(matching_data)
        
        # Generate matching summary
        generate_matching_summary(stats, matching_data)
        
        print(f"✅ Matching export completed: {csv_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error in matching export: {e}")
        return False

def generate_matching_summary(stats, data):
    """Generate summary of matching export."""
    summary_file = "matching_export_summary.txt"
    
    with open(summary_file, 'w') as f:
        f.write("ERA Airtable Matching Export Summary\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("Export Statistics:\n")
        f.write(f"  Total records processed: {stats['total_records']}\n")
        f.write(f"  Records with names: {stats['records_with_names']}\n")
        f.write(f"  Records with emails: {stats['records_with_emails']}\n")
        f.write(f"  Donor records: {stats['donors']}\n")
        f.write(f"  Names with variations applied: {stats['name_variations_applied']}\n\n")
        
        f.write("Name Cleaning Examples:\n")
        examples = 0
        for record in data:
            if record['original_name'] != record['cleaned_name'] and examples < 10:
                f.write(f"  '{record['original_name']}' → '{record['cleaned_name']}'\n")
                examples += 1
        
        f.write(f"\nReady for cross-correlation with Fathom participant data.\n")
        f.write(f"Use this file for name matching algorithms.\n")
    
    print(f"📊 Matching summary written to {summary_file}")

def main():
    """Main execution function."""
    print("🎯 ERA Airtable → Fathom Matching Export")
    print("=" * 45)
    
    success = export_for_matching()
    
    if success:
        print("\n🎉 Matching export completed successfully!")
        print(f"📁 Ready for cross-correlation with:")
        print(f"   - {EXPORT_CONFIG['people_matching_csv']}")
        print(f"   - ../FathomInventory/analysis/participants.csv")
    else:
        print("\n❌ Matching export failed!")

if __name__ == "__main__":
    main()
