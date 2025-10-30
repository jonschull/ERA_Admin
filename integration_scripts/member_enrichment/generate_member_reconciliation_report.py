#!/usr/bin/env python3
"""
Generate Member Reconciliation Report

Purpose: Create a comprehensive CSV listing all Airtable members with bios,
cross-referenced against:
- Fathom Database (fuzzy matched)
- Google Groups membership
- Zeffy donations

Columns:
- name_airtable: Name from Airtable
- name_database: Fuzzy matched name from Fathom DB
- match_quality: Fuzzy match score (0-100)
- bio_quality_airtable: Quality assessment of Airtable bio
- bio_quality_database: Quality assessment of Fathom DB bio
- in_google_groups_members: Yes/No
- in_google_groups_update: Yes/No
- last_donation_zeffy: Date of last donation
- total_donations_zeffy: Total donation amount
- comments: Empty column for manual notes

Stage 1: Data Loading & Exploration
"""

import sqlite3
import pandas as pd
import openpyxl
from pathlib import Path
from thefuzz import fuzz
import sys

# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
AIRTABLE_CSV = PROJECT_ROOT / "airtable" / "people_export.csv"
FATHOM_DB = PROJECT_ROOT / "FathomInventory" / "fathom_emails.db"
GGROUPS_MEMBERS = PROJECT_ROOT / "Other_Data_Sources" / "GGroups" / "members_20251029_113641.csv"
GGROUPS_UPDATE = PROJECT_ROOT / "Other_Data_Sources" / "GGroups" / "ecorestoration-alliance-update (5).csv"
ZEFFY_XLSX = PROJECT_ROOT / "Other_Data_Sources" / "Zeffy" / "zeffy_payments_20251029_194720.xlsx"

def load_airtable_data():
    """Load Airtable people with non-empty bios."""
    print("=" * 80)
    print("LOADING AIRTABLE DATA")
    print("=" * 80)
    print()
    
    if not AIRTABLE_CSV.exists():
        print(f"❌ Airtable CSV not found: {AIRTABLE_CSV}")
        sys.exit(1)
    
    df = pd.read_csv(AIRTABLE_CSV)
    print(f"✅ Loaded {len(df)} total people from Airtable")
    print(f"   Columns: {list(df.columns)}")
    print()
    
    # Filter to people with non-empty bios
    # Check what the bio column is called
    bio_columns = [col for col in df.columns if 'bio' in col.lower()]
    print(f"   Bio-related columns: {bio_columns}")
    
    if not bio_columns:
        print("⚠️  No bio column found in Airtable CSV")
        print("   Available columns:")
        for col in df.columns:
            print(f"      - {col}")
        sys.exit(1)
    
    # Use the first bio column found
    bio_col = bio_columns[0]
    print(f"   Using bio column: '{bio_col}'")
    print()
    
    # Filter to non-empty bios
    df_with_bios = df[df[bio_col].notna() & (df[bio_col].str.strip() != '')]
    print(f"✅ Found {len(df_with_bios)} people with non-empty bios")
    print()
    
    # Show sample
    print("Sample data (first 3 rows):")
    for idx, row in df_with_bios.head(3).iterrows():
        name = row.get('Name', row.get('name', 'Unknown'))
        bio = row[bio_col][:100] + "..." if len(str(row[bio_col])) > 100 else row[bio_col]
        print(f"   - {name}")
        print(f"     Bio: {bio}")
        print()
    
    return df_with_bios, bio_col

def load_fathom_database():
    """Load Fathom database participants."""
    print("=" * 80)
    print("LOADING FATHOM DATABASE")
    print("=" * 80)
    print()
    
    if not FATHOM_DB.exists():
        print(f"❌ Fathom database not found: {FATHOM_DB}")
        sys.exit(1)
    
    conn = sqlite3.connect(FATHOM_DB)
    
    # Get table schema
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='participants'")
    schema = cursor.fetchone()
    print(f"Participants table schema:")
    print(f"   {schema[0] if schema else 'Table not found'}")
    print()
    
    # Load participants
    query = """
    SELECT 
        name,
        email,
        bio,
        era_member,
        era_africa,
        is_donor,
        affiliation,
        location,
        source_call_title
    FROM participants
    WHERE era_member = 1 OR bio IS NOT NULL
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    print(f"✅ Loaded {len(df)} participants from Fathom DB")
    print(f"   With era_member=1: {len(df[df['era_member'] == 1])}")
    print(f"   With non-empty bio: {len(df[df['bio'].notna() & (df['bio'] != '')])}")
    print()
    
    # Show sample
    print("Sample data (first 3 rows):")
    for idx, row in df.head(3).iterrows():
        print(f"   - {row['name']}")
        print(f"     Email: {row['email']}")
        print(f"     Bio: {str(row['bio'])[:80]}..." if pd.notna(row['bio']) else "     Bio: None")
        print()
    
    return df

def load_google_groups():
    """Load Google Groups membership lists."""
    print("=" * 80)
    print("LOADING GOOGLE GROUPS DATA")
    print("=" * 80)
    print()
    
    # Load members list (skip first row which is group name)
    if not GGROUPS_MEMBERS.exists():
        print(f"❌ Google Groups members CSV not found: {GGROUPS_MEMBERS}")
        members_emails = set()
    else:
        members_df = pd.read_csv(GGROUPS_MEMBERS, skiprows=1)
        # Extract email addresses from first column
        members_emails = set(members_df.iloc[:, 0].str.lower().str.strip())
        print(f"✅ Loaded {len(members_emails)} members from Google Groups")
        print(f"   Sample emails: {list(members_emails)[:3]}")
        print()
    
    # Load update group (skip first row which is group name)
    if not GGROUPS_UPDATE.exists():
        print(f"❌ Google Groups update CSV not found: {GGROUPS_UPDATE}")
        update_emails = set()
    else:
        update_df = pd.read_csv(GGROUPS_UPDATE, skiprows=1)
        # Extract email addresses from first column
        update_emails = set(update_df.iloc[:, 0].str.lower().str.strip())
        print(f"✅ Loaded {len(update_emails)} members from Update group")
        print(f"   Sample emails: {list(update_emails)[:3]}")
        print()
    
    return members_emails, update_emails

def load_zeffy_donations():
    """Load Zeffy donation data."""
    print("=" * 80)
    print("LOADING ZEFFY DONATIONS")
    print("=" * 80)
    print()
    
    if not ZEFFY_XLSX.exists():
        print(f"❌ Zeffy Excel file not found: {ZEFFY_XLSX}")
        return pd.DataFrame()
    
    # Load Excel file
    df = pd.read_excel(ZEFFY_XLSX)
    print(f"✅ Loaded {len(df)} donation records from Zeffy")
    print(f"   Columns: {list(df.columns)}")
    print()
    
    # Show sample
    print("Sample data (first 3 rows):")
    for idx, row in df.head(3).iterrows():
        print(f"   Row {idx}:")
        for col in df.columns[:5]:  # Show first 5 columns
            print(f"      {col}: {row[col]}")
        print()
    
    return df

def fuzzy_match_name(airtable_name, fathom_df, threshold=80):
    """
    Find best fuzzy match for an Airtable name in Fathom database.
    
    Returns: (matched_name, match_score) or (None, 0) if no good match
    """
    if pd.isna(airtable_name) or airtable_name.strip() == '':
        return None, 0
    
    best_match = None
    best_score = 0
    
    for fathom_name in fathom_df['name']:
        if pd.isna(fathom_name):
            continue
        
        # Use token_sort_ratio for better matching (handles word order)
        score = fuzz.token_sort_ratio(airtable_name.lower(), fathom_name.lower())
        
        if score > best_score:
            best_score = score
            best_match = fathom_name
    
    # Only return match if above threshold
    if best_score >= threshold:
        return best_match, best_score
    else:
        return None, best_score

def test_fuzzy_matching(airtable_df, fathom_df):
    """Test fuzzy matching on a sample of names."""
    print("=" * 80)
    print("STAGE 2: FUZZY MATCHING TEST")
    print("=" * 80)
    print()
    
    print("Testing fuzzy matching on first 10 Airtable names:")
    print()
    
    for idx, row in airtable_df.head(10).iterrows():
        airtable_name = row['Name']
        matched_name, score = fuzzy_match_name(airtable_name, fathom_df)
        
        status = "✅" if matched_name else "❌"
        print(f"{status} {airtable_name}")
        if matched_name:
            print(f"   → Matched: {matched_name} (score: {score})")
        else:
            print(f"   → No match found (best score: {score})")
        print()
    
    print("=" * 80)
    print("STAGE 2 TEST COMPLETE")
    print("=" * 80)
    print()
    
    # Ask user if threshold is good
    print("Does this matching quality look good?")
    print("- Threshold is currently 80")
    print("- Higher threshold = fewer false positives, more missed matches")
    print("- Lower threshold = more matches, but some may be incorrect")
    print()

def assess_bio_quality(bio_text):
    """
    Assess quality of a bio.
    Returns: (score, category)
    - score: 0-100
    - category: "empty", "minimal", "good", "excellent"
    """
    if pd.isna(bio_text) or str(bio_text).strip() == '':
        return 0, "empty"
    
    bio_str = str(bio_text).strip()
    length = len(bio_str)
    
    # Simple heuristic based on length and content
    if length < 50:
        return 25, "minimal"
    elif length < 150:
        return 50, "good"
    else:
        return 75, "excellent"

def main():
    """Full pipeline: Load, match, cross-reference, generate CSV."""
    print()
    print("=" * 80)
    print("MEMBER RECONCILIATION REPORT - FULL PIPELINE")
    print("=" * 80)
    print()
    
    # Stage 1: Load all data sources
    print("Stage 1: Loading data sources...")
    airtable_df, bio_col = load_airtable_data()
    fathom_df = load_fathom_database()
    members_df, update_df = load_google_groups()
    zeffy_df = load_zeffy_donations()
    
    print("=" * 80)
    print("BUILDING RECONCILIATION REPORT")
    print("=" * 80)
    print()
    print(f"Processing {len(airtable_df)} Airtable members with bios...")
    print()
    
    # Build the report
    results = []
    
    for idx, row in airtable_df.iterrows():
        if idx % 50 == 0:
            print(f"   Processing {idx}/{len(airtable_df)}...")
        
        airtable_name = row['Name']
        airtable_email = row.get('Email', '')
        airtable_bio = row[bio_col]
        
        # Get publish status from Airtable
        publish_status = row.get('Publish', '')
        
        # Fuzzy match to Fathom DB
        matched_name, match_score = fuzzy_match_name(airtable_name, fathom_df)
        
        # Get Fathom bio and check Town Hall attendance if matched
        fathom_bio = ''
        appeared_in = ''
        if matched_name:
            fathom_row = fathom_df[fathom_df['name'] == matched_name].iloc[0]
            fathom_bio = fathom_row['bio'] if pd.notna(fathom_row['bio']) else ''
            
            # Check if appeared in Town Hall or other calls
            source_title = str(fathom_row.get('source_call_title', ''))
            if 'Town Hall' in source_title or 'town hall' in source_title.lower():
                appeared_in = 'TH'
            elif source_title and source_title != 'nan':
                appeared_in = 'Other'
        
        # Assess bio quality (placeholder - will be replaced with intelligent evaluation)
        airtable_bio_score, airtable_bio_cat = assess_bio_quality(airtable_bio)
        fathom_bio_score, fathom_bio_cat = assess_bio_quality(fathom_bio)
        
        # Check Google Groups membership (by email)
        in_members = 'No'
        in_update = 'No'
        if pd.notna(airtable_email) and airtable_email.strip() != '':
            email_lower = airtable_email.lower().strip()
            if email_lower in members_df:  # members_df is now a set of emails
                in_members = 'Yes'
            if email_lower in update_df:  # update_df is now a set of emails
                in_update = 'Yes'
        
        # Check Zeffy donations (by email or name)
        last_donation = ''
        total_donations = 0.0
        
        if pd.notna(airtable_email) and airtable_email.strip() != '':
            donor_records = zeffy_df[zeffy_df['Email'].str.lower() == airtable_email.lower()]
            if len(donor_records) > 0:
                # Get last donation date
                donor_records_sorted = donor_records.sort_values('Payment Date (America/New_York)', ascending=False)
                last_donation = str(donor_records_sorted.iloc[0]['Payment Date (America/New_York)'])
                # Sum total donations
                total_donations = donor_records['Total Amount'].sum()
        
        # Build result row
        results.append({
            'name_airtable': airtable_name,
            'name_database': matched_name if matched_name else '',
            'match_quality': match_score,
            'bio_quality_airtable': f"{airtable_bio_cat} ({airtable_bio_score})",
            'bio_quality_database': f"{fathom_bio_cat} ({fathom_bio_score})" if matched_name else 'N/A',
            'in_google_groups_members': in_members,
            'in_google_groups_update': in_update,
            'last_donation_zeffy': last_donation,
            'total_donations_zeffy': f"${total_donations:.2f}" if total_donations > 0 else '',
            'publish_status': publish_status,
            'appeared_in_town_hall': appeared_in,
            'bio_evaluation_link': '',  # Will be filled in during intelligent evaluation
            'comments': ''
        })
    
    # Create DataFrame
    results_df = pd.DataFrame(results)
    
    # Save to CSV
    output_file = SCRIPT_DIR / "member_reconciliation_report.csv"
    results_df.to_csv(output_file, index=False)
    
    print()
    print("=" * 80)
    print("REPORT COMPLETE")
    print("=" * 80)
    print()
    print(f"✅ Processed {len(results_df)} members")
    print(f"✅ Saved to: {output_file}")
    print()
    
    # Summary statistics
    matched_count = len(results_df[results_df['name_database'] != ''])
    in_members_count = len(results_df[results_df['in_google_groups_members'] == 'Yes'])
    in_update_count = len(results_df[results_df['in_google_groups_update'] == 'Yes'])
    donors_count = len(results_df[results_df['total_donations_zeffy'] != ''])
    th_count = len(results_df[results_df['appeared_in_town_hall'] == 'TH'])
    other_count = len(results_df[results_df['appeared_in_town_hall'] == 'Other'])
    published_count = len(results_df[results_df['publish_status'].notna() & (results_df['publish_status'] != '')])
    
    print("Summary:")
    print(f"   - Matched to Fathom DB: {matched_count}/{len(results_df)} ({matched_count/len(results_df)*100:.1f}%)")
    print(f"   - Appeared in Town Hall: {th_count}")
    print(f"   - Appeared in other calls: {other_count}")
    print(f"   - In Google Groups (members): {in_members_count}")
    print(f"   - In Google Groups (update): {in_update_count}")
    print(f"   - Zeffy donors: {donors_count}")
    print(f"   - Published in Airtable: {published_count}")
    print()
    print(f"📄 CSV saved: {output_file}")
    print()
    print("Next step: Intelligent bio evaluation (batches of 10)")
    print()

if __name__ == "__main__":
    main()
