#!/usr/bin/env python3
"""
Validate Fathom AI participant extraction against Airtable manual attendance tracking.
Compares TH column checkboxes (manual) with Fathom participant database (AI-extracted).
"""

import csv
import sqlite3
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Paths
AIRTABLE_CSV = "/Users/admin/Library/CloudStorage/Dropbox-EcoRestorationAllianceLLC/Jon Schull/CascadeProjects/ERA_Admin/airtable/people_export.csv"
FATHOM_DB = "../fathom_emails.db"

def parse_th_column_date(th_col):
    """Parse TH column name to date."""
    # Handle formats like "TH 1-08-2025", "TH 2-05-25", "Th 10-1-25"
    match = re.search(r'(\d+)-(\d+)-(\d+)', th_col)
    if not match:
        return None
    
    month, day, year = match.groups()
    
    # Handle 2-digit years
    if len(year) == 2:
        year = f"20{year}"
    
    try:
        date = datetime(int(year), int(month), int(day))
        return date.strftime('%Y-%m-%d')
    except:
        return None

def load_airtable_attendance():
    """Load Airtable TH attendance data."""
    print("📥 Loading Airtable attendance data...")
    
    attendance = defaultdict(lambda: defaultdict(bool))
    th_columns = []
    th_dates = {}
    
    with open(AIRTABLE_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Find all TH columns
        th_columns = [col for col in reader.fieldnames if col.upper().startswith('TH ')]
        
        print(f"   Found {len(th_columns)} TH columns")
        
        # Parse dates for each TH column
        for th_col in th_columns:
            date = parse_th_column_date(th_col)
            if date:
                th_dates[th_col] = date
                print(f"   {th_col} → {date}")
        
        # Load attendance data
        for row in reader:
            name = row.get('Name', '').strip()
            if not name:
                continue
            
            for th_col in th_columns:
                if row.get(th_col) == 'True':
                    if th_col in th_dates:
                        attendance[th_dates[th_col]][name] = True
    
    print(f"✅ Loaded attendance for {len(attendance)} meetings from Airtable")
    return attendance, th_dates

def load_fathom_attendance():
    """Load Fathom participant data from database."""
    print("📥 Loading Fathom participant data...")
    
    conn = sqlite3.connect(FATHOM_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get Town Hall meetings with participants
    cursor.execute("""
        SELECT c.date, c.title, p.name
        FROM participants p
        JOIN calls c ON p.call_hyperlink = c.hyperlink
        WHERE c.title LIKE '%Town Hall%'
        ORDER BY c.date, p.name
    """)
    
    attendance = defaultdict(lambda: defaultdict(bool))
    for row in cursor.fetchall():
        date = row['date']
        name = row['name'].strip()
        attendance[date][name] = True
    
    conn.close()
    
    print(f"✅ Loaded attendance for {len(attendance)} meetings from Fathom")
    return attendance

def fuzzy_name_match(name1, name2):
    """Simple fuzzy name matching."""
    name1 = name1.lower().strip()
    name2 = name2.lower().strip()
    
    # Exact match
    if name1 == name2:
        return True
    
    # Last name match
    parts1 = name1.split()
    parts2 = name2.split()
    if parts1 and parts2 and parts1[-1] == parts2[-1]:
        return True
    
    # Contains match
    if name1 in name2 or name2 in name1:
        return True
    
    return False

def compare_attendance(airtable_attendance, fathom_attendance, th_dates):
    """Compare attendance between Airtable and Fathom."""
    print("\n🔍 Comparing attendance...")
    
    results = []
    
    for th_col, date in sorted(th_dates.items(), key=lambda x: x[1]):
        if date not in airtable_attendance:
            continue
        
        airtable_names = set(airtable_attendance[date].keys())
        fathom_names = set(fathom_attendance.get(date, {}).keys())
        
        # Find matches
        matched = set()
        airtable_only = set()
        fathom_only = set()
        
        # Try to match names
        for at_name in airtable_names:
            found_match = False
            for fathom_name in fathom_names:
                if fuzzy_name_match(at_name, fathom_name):
                    matched.add((at_name, fathom_name))
                    found_match = True
                    break
            if not found_match:
                airtable_only.add(at_name)
        
        # Find Fathom names not matched
        matched_fathom = {m[1] for m in matched}
        fathom_only = fathom_names - matched_fathom
        
        match_rate = len(matched) / len(airtable_names) * 100 if airtable_names else 0
        
        results.append({
            'date': date,
            'th_column': th_col,
            'airtable_count': len(airtable_names),
            'fathom_count': len(fathom_names),
            'matched': len(matched),
            'airtable_only': list(airtable_only),
            'fathom_only': list(fathom_only),
            'match_rate': match_rate
        })
    
    return results

def generate_validation_report(results):
    """Generate detailed validation report."""
    report_file = "townhall_validation_report.md"
    
    with open(report_file, 'w') as f:
        f.write("# Town Hall Attendance Validation Report\n\n")
        f.write("**Comparing:** Airtable Manual Tracking ↔ Fathom AI Extraction\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("---\n\n")
        
        # Summary statistics
        total_airtable = sum(r['airtable_count'] for r in results)
        total_fathom = sum(r['fathom_count'] for r in results)
        total_matched = sum(r['matched'] for r in results)
        avg_match_rate = sum(r['match_rate'] for r in results) / len(results) if results else 0
        
        f.write("## Summary Statistics\n\n")
        f.write(f"- **Meetings compared:** {len(results)}\n")
        f.write(f"- **Total Airtable attendance records:** {total_airtable}\n")
        f.write(f"- **Total Fathom attendance records:** {total_fathom}\n")
        f.write(f"- **Successfully matched:** {total_matched}\n")
        f.write(f"- **Average match rate:** {avg_match_rate:.1f}%\n\n")
        
        f.write("---\n\n")
        
        # Meeting-by-meeting breakdown
        f.write("## Meeting-by-Meeting Comparison\n\n")
        
        for result in sorted(results, key=lambda x: x['date'], reverse=True):
            f.write(f"### {result['date']} ({result['th_column']})\n\n")
            f.write(f"- **Airtable:** {result['airtable_count']} attendees\n")
            f.write(f"- **Fathom:** {result['fathom_count']} participants\n")
            f.write(f"- **Matched:** {result['matched']} ({result['match_rate']:.1f}%)\n\n")
            
            if result['airtable_only']:
                f.write(f"**In Airtable but NOT in Fathom** ({len(result['airtable_only'])}):\n")
                for name in sorted(result['airtable_only']):
                    f.write(f"- {name}\n")
                f.write("\n")
            
            if result['fathom_only']:
                f.write(f"**In Fathom but NOT in Airtable** ({len(result['fathom_only'])}):\n")
                for name in sorted(result['fathom_only'][:20]):  # Limit to 20
                    f.write(f"- {name}\n")
                if len(result['fathom_only']) > 20:
                    f.write(f"- ... and {len(result['fathom_only']) - 20} more\n")
                f.write("\n")
            
            f.write("---\n\n")
        
        # Insights section
        f.write("## Insights & Recommendations\n\n")
        
        high_match = [r for r in results if r['match_rate'] >= 70]
        low_match = [r for r in results if r['match_rate'] < 50]
        
        f.write(f"### High Match Rate Meetings (≥70%)\n")
        f.write(f"{len(high_match)} meetings with strong agreement between systems\n\n")
        
        if low_match:
            f.write(f"### Low Match Rate Meetings (<50%)\n")
            f.write(f"{len(low_match)} meetings need investigation:\n")
            for r in low_match:
                f.write(f"- {r['date']}: {r['match_rate']:.1f}% match rate\n")
            f.write("\n")
        
        f.write("### Common Patterns\n\n")
        f.write("**Fathom extracts more participants:**\n")
        f.write("- Fathom may capture names from video/audio that weren't manually tracked\n")
        f.write("- Some participants may join briefly or appear in discussion\n\n")
        
        f.write("**Airtable has names Fathom missed:**\n")
        f.write("- Name variations (nicknames, initials)\n")
        f.write("- Silent participants not verbally identified\n")
        f.write("- Camera-off participants\n\n")
    
    print(f"📊 Validation report written to {report_file}")
    return report_file

def main():
    """Main execution."""
    print("="*60)
    print("TOWN HALL ATTENDANCE VALIDATION")
    print("Airtable (Manual) ↔ Fathom (AI Extracted)")
    print("="*60)
    print()
    
    # Load data
    airtable_attendance, th_dates = load_airtable_attendance()
    fathom_attendance = load_fathom_attendance()
    
    # Compare
    results = compare_attendance(airtable_attendance, fathom_attendance, th_dates)
    
    # Generate report
    report_file = generate_validation_report(results)
    
    # Print summary
    print("\n" + "="*60)
    print("✅ VALIDATION COMPLETE")
    print("="*60)
    print(f"Meetings compared: {len(results)}")
    
    if results:
        avg_match = sum(r['match_rate'] for r in results) / len(results)
        print(f"Average match rate: {avg_match:.1f}%")
    
    print(f"\n📄 Full report: {report_file}")

if __name__ == "__main__":
    main()
