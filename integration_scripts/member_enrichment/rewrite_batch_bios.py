#!/usr/bin/env python3
"""
Rewrite Bios for Batch

Purpose: Read CSV comments, rewrite bios marked "rewrite bio", generate batch HTML
"""

import pandas as pd
import sqlite3
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CSV_FILE = SCRIPT_DIR / "member_reconciliation_report.csv"
AIRTABLE_CSV = PROJECT_ROOT / "airtable" / "people_export.csv"
FATHOM_DB = PROJECT_ROOT / "FathomInventory" / "fathom_emails.db"

def load_data():
    """Load CSV and bio data."""
    df = pd.read_csv(CSV_FILE)
    airtable_df = pd.read_csv(AIRTABLE_CSV)
    
    conn = sqlite3.connect(FATHOM_DB)
    fathom_df = pd.read_sql_query("SELECT name, bio FROM participants WHERE bio IS NOT NULL", conn)
    conn.close()
    
    return df, airtable_df, fathom_df

def get_bios_to_rewrite(df, batch_start, batch_end):
    """Get list of bios marked for rewriting in this batch."""
    batch_df = df.iloc[batch_start:batch_end]
    to_rewrite = batch_df[batch_df['comments'].str.contains('rewrite bio', case=False, na=False)]
    return to_rewrite

def rewrite_bio(name, original_bio, airtable_df, fathom_df):
    """
    Intelligently rewrite a bio to ERA standards.
    
    Returns: proposed_bio (string)
    """
    # Get additional context from Airtable
    person = airtable_df[airtable_df['Name'] == name]
    if len(person) == 0:
        return original_bio
    
    person = person.iloc[0]
    
    # Extract available information
    affiliated_orgs = person.get('Affiliated Orgs', '')
    location = person.get('Location', person.get('City Town', ''))
    country = person.get('Country', '')
    role = person.get('Role(s)', '')
    
    # Build location string
    location_str = ''
    if pd.notna(location) and location:
        location_str = f" based in {location}"
        if pd.notna(country) and country and country not in str(location):
            location_str += f", {country}"
    elif pd.notna(country) and country:
        location_str = f" based in {country}"
    
    # This is a placeholder - in practice, you (the AI) will write these intelligently
    # For now, return a template that you'll fill in manually
    return f"[NEEDS INTELLIGENT REWRITE: {name}{location_str}. Original: {original_bio[:100]}...]"

def main():
    """Process batch rewrites."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python rewrite_batch_bios.py <batch_number>")
        print("Example: python rewrite_batch_bios.py 1")
        sys.exit(1)
    
    batch_num = int(sys.argv[1])
    batch_start = (batch_num - 1) * 10
    batch_end = batch_start + 10
    
    print(f"Processing Batch {batch_num} (rows {batch_start}-{batch_end-1})")
    print()
    
    # Load data
    df, airtable_df, fathom_df = load_data()
    
    # Get bios to rewrite
    to_rewrite = get_bios_to_rewrite(df, batch_start, batch_end)
    
    if len(to_rewrite) == 0:
        print("No bios marked for rewriting in this batch.")
        return
    
    print(f"Found {len(to_rewrite)} bios to rewrite:")
    for idx, row in to_rewrite.iterrows():
        print(f"  - {row['name_airtable']}")
    print()
    
    # For each bio to rewrite, show original and prompt for rewrite
    for idx, row in to_rewrite.iterrows():
        name = row['name_airtable']
        print("=" * 80)
        print(f"REWRITING: {name}")
        print("=" * 80)
        
        # Get original bio
        original_bio = airtable_df[airtable_df['Name'] == name]['Bio'].iloc[0]
        print(f"\nOriginal bio:\n{original_bio}\n")
        
        # Get additional context
        person = airtable_df[airtable_df['Name'] == name].iloc[0]
        print("Available context:")
        print(f"  Affiliated Orgs: {person.get('Affiliated Orgs', 'N/A')}")
        print(f"  Location: {person.get('Location', 'N/A')}")
        print(f"  Country: {person.get('Country', 'N/A')}")
        print(f"  Role(s): {person.get('Role(s)', 'N/A')}")
        print()
        
        # Check if in Fathom
        fathom_name = row['name_database']
        if pd.notna(fathom_name) and fathom_name:
            fathom_bio = fathom_df[fathom_df['name'] == fathom_name]['bio'].iloc[0]
            print(f"Fathom bio:\n{fathom_bio}\n")
        
        print("Please provide rewritten bio (or press Enter to skip):")
        print()

if __name__ == "__main__":
    main()
