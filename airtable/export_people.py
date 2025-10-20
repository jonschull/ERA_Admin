#!/usr/bin/env python3
"""
Export People table from Airtable to CSV with all available fields.
Provides fresh, complete data export for analysis and cross-correlation.
"""

import csv
import sys
from datetime import datetime
from pathlib import Path
from pyairtable import Api
from config import AIRTABLE_CONFIG, EXPORT_CONFIG
import time

def export_people_table():
    """Export the complete People table to CSV."""
    print("🔄 Connecting to Airtable...")
    
    try:
        # Initialize Airtable API
        api = Api(AIRTABLE_CONFIG['api_key'])
        table = api.table(AIRTABLE_CONFIG['base_id'], AIRTABLE_CONFIG['tables']['people'])
        
        print("📥 Fetching all records...")
        records = table.all()
        
        if not records:
            print("❌ No records found in People table")
            return False
        
        print(f"✅ Retrieved {len(records)} records")
        
        # Collect all unique field names across all records
        all_fields = set()
        for record in records:
            all_fields.update(record['fields'].keys())
        
        all_fields = sorted(list(all_fields))
        print(f"📊 Found {len(all_fields)} unique fields: {', '.join(all_fields[:10])}{'...' if len(all_fields) > 10 else ''}")
        
        # Export to CSV
        csv_file = EXPORT_CONFIG['people_csv']
        print(f"📝 Writing to {csv_file}...")
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            # Add metadata columns
            fieldnames = ['airtable_id', 'created_time', 'last_modified'] + all_fields
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for record in records:
                row = {
                    'airtable_id': record['id'],
                    'created_time': record.get('createdTime', ''),
                    'last_modified': record.get('lastModifiedTime', '')
                }
                
                # Add all field data
                for field in all_fields:
                    value = record['fields'].get(field, '')
                    
                    # Handle list fields (convert to semicolon-separated)
                    if isinstance(value, list):
                        if all(isinstance(item, str) for item in value):
                            value = '; '.join(value)
                        else:
                            value = str(value)
                    
                    row[field] = value
                
                writer.writerow(row)
        
        print(f"✅ Export completed: {csv_file}")
        
        # Generate summary
        generate_export_summary(records, all_fields)
        
        return True
        
    except Exception as e:
        print(f"❌ Error exporting People table: {e}")
        return False

def generate_export_summary(records, fields):
    """Generate a summary of the export."""
    summary_file = EXPORT_CONFIG['summary_file']
    
    with open(summary_file, 'w') as f:
        f.write(f"ERA Airtable Export Summary\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"=" * 50 + "\n\n")
        
        f.write(f"Records exported: {len(records)}\n")
        f.write(f"Fields available: {len(fields)}\n\n")
        
        f.write("Field List:\n")
        for field in fields:
            f.write(f"  - {field}\n")
        
        f.write("\nField Usage Analysis:\n")
        field_usage = {}
        for record in records:
            for field in fields:
                if field in record['fields'] and record['fields'][field]:
                    field_usage[field] = field_usage.get(field, 0) + 1
        
        for field, count in sorted(field_usage.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(records)) * 100
            f.write(f"  {field}: {count}/{len(records)} ({percentage:.1f}%)\n")
        
        # Key statistics
        f.write(f"\nKey Statistics:\n")
        names_with_data = sum(1 for r in records if r['fields'].get('Name'))
        emails_with_data = sum(1 for r in records if r['fields'].get('Email'))
        donors = sum(1 for r in records if r['fields'].get('Donor Flag'))
        
        f.write(f"  Records with names: {names_with_data}\n")
        f.write(f"  Records with emails: {emails_with_data}\n")
        f.write(f"  Records marked as donors: {donors}\n")
    
    print(f"📊 Summary written to {summary_file}")

def main():
    """Main execution function."""
    print("🚀 ERA Airtable People Export")
    print("=" * 40)
    
    # Create backup directory if it doesn't exist
    Path(EXPORT_CONFIG['backup_dir']).mkdir(exist_ok=True)
    
    # Backup existing export if it exists
    csv_file = Path(EXPORT_CONFIG['people_csv'])
    if csv_file.exists():
        backup_name = f"{EXPORT_CONFIG['backup_dir']}/people_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        csv_file.rename(backup_name)
        print(f"📦 Backed up previous export to {backup_name}")
    
    # Run export
    success = export_people_table()
    
    if success:
        print("\n🎉 Export completed successfully!")
        print(f"📁 Files created:")
        print(f"   - {EXPORT_CONFIG['people_csv']}")
        print(f"   - {EXPORT_CONFIG['summary_file']}")
    else:
        print("\n❌ Export failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
