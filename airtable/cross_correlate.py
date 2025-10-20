#!/usr/bin/env python3
"""
Cross-correlate Airtable membership data with Fathom participant data.
Identifies overlaps, gaps, and opportunities for data enrichment.
"""

import csv
import sys
from pathlib import Path
from fuzzywuzzy import fuzz
from config import MATCHING_CONFIG

def load_airtable_data():
    """Load Airtable matching data."""
    csv_file = "people_for_matching.csv"
    if not Path(csv_file).exists():
        print(f"❌ Airtable data not found: {csv_file}")
        print("   Run: python export_for_fathom_matching.py")
        return None
    
    airtable_data = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        airtable_data = list(reader)
    
    print(f"📥 Loaded {len(airtable_data)} Airtable records")
    return airtable_data

def load_fathom_data():
    """Load Fathom participant data."""
    fathom_csv = "../FathomInventory/analysis/participants.csv"
    if not Path(fathom_csv).exists():
        print(f"❌ Fathom data not found: {fathom_csv}")
        print("   Run: cd FathomInventory/analysis && python parse_analysis_results.py")
        return None
    
    fathom_data = []
    with open(fathom_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fathom_data = list(reader)
    
    print(f"📥 Loaded {len(fathom_data)} Fathom participant records")
    return fathom_data

def fuzzy_match_names(name1, name2, threshold=None):
    """Check if two names match using fuzzy string matching."""
    if not name1 or not name2:
        return False, 0
    
    if threshold is None:
        threshold = MATCHING_CONFIG['name_similarity_threshold']
    
    # Normalize names
    name1 = name1.lower().strip()
    name2 = name2.lower().strip()
    
    # Calculate similarity scores
    ratio = fuzz.ratio(name1, name2)
    partial_ratio = fuzz.partial_ratio(name1, name2)
    token_sort_ratio = fuzz.token_sort_ratio(name1, name2)
    
    # Use the highest score
    best_score = max(ratio, partial_ratio, token_sort_ratio) / 100.0
    
    return best_score >= threshold, best_score

def cross_correlate(airtable_data, fathom_data):
    """Perform cross-correlation analysis."""
    print("🔍 Performing cross-correlation analysis...")
    
    matches = []
    unmatched_airtable = []
    unmatched_fathom = []
    
    # Track which Fathom records have been matched
    fathom_matched = set()
    
    # For each Airtable record, find best Fathom match
    for at_record in airtable_data:
        at_name = at_record['cleaned_name']
        best_match = None
        best_score = 0
        
        for i, fathom_record in enumerate(fathom_data):
            if i in fathom_matched:
                continue
                
            fathom_name = fathom_record['Name']
            is_match, score = fuzzy_match_names(at_name, fathom_name)
            
            if is_match and score > best_score:
                best_match = (i, fathom_record)
                best_score = score
        
        if best_match:
            fathom_matched.add(best_match[0])
            matches.append({
                'airtable_record': at_record,
                'fathom_record': best_match[1],
                'match_score': best_score,
                'airtable_name': at_name,
                'fathom_name': best_match[1]['Name']
            })
        else:
            unmatched_airtable.append(at_record)
    
    # Collect unmatched Fathom records
    for i, fathom_record in enumerate(fathom_data):
        if i not in fathom_matched:
            unmatched_fathom.append(fathom_record)
    
    return matches, unmatched_airtable, unmatched_fathom

def generate_correlation_report(matches, unmatched_airtable, unmatched_fathom):
    """Generate detailed correlation report."""
    report_file = "cross_correlation_report.txt"
    
    with open(report_file, 'w') as f:
        f.write("ERA Cross-Correlation Report: Airtable ↔ Fathom\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("SUMMARY STATISTICS\n")
        f.write("-" * 20 + "\n")
        f.write(f"Matched records: {len(matches)}\n")
        f.write(f"Unmatched Airtable members: {len(unmatched_airtable)}\n")
        f.write(f"Unmatched Fathom participants: {len(unmatched_fathom)}\n\n")
        
        total_airtable = len(matches) + len(unmatched_airtable)
        total_fathom = len(matches) + len(unmatched_fathom)
        
        f.write(f"Match rate (Airtable): {len(matches)/total_airtable*100:.1f}%\n")
        f.write(f"Match rate (Fathom): {len(matches)/total_fathom*100:.1f}%\n\n")
        
        # Donor analysis
        donor_matches = sum(1 for m in matches if m['airtable_record']['is_donor'] == 'True')
        f.write(f"Donors in matched records: {donor_matches}\n\n")
        
        f.write("TOP MATCHES (by confidence)\n")
        f.write("-" * 30 + "\n")
        sorted_matches = sorted(matches, key=lambda x: x['match_score'], reverse=True)
        for match in sorted_matches[:20]:
            f.write(f"{match['match_score']:.3f} | {match['airtable_name']} ↔ {match['fathom_name']}\n")
        
        f.write(f"\nUNMATCHED AIRTABLE MEMBERS ({len(unmatched_airtable)})\n")
        f.write("-" * 40 + "\n")
        for record in unmatched_airtable[:50]:  # Limit output
            donor_flag = " [DONOR]" if record['is_donor'] == 'True' else ""
            f.write(f"{record['cleaned_name']}{donor_flag}\n")
        
        f.write(f"\nUNMATCHED FATHOM PARTICIPANTS ({len(unmatched_fathom)})\n")
        f.write("-" * 45 + "\n")
        for record in unmatched_fathom[:50]:  # Limit output
            location = f" ({record['Location']})" if record['Location'] else ""
            f.write(f"{record['Name']}{location}\n")
    
    print(f"📊 Correlation report written to {report_file}")

def main():
    """Main execution function."""
    print("🔗 ERA Cross-Correlation: Airtable ↔ Fathom")
    print("=" * 50)
    
    # Load data
    airtable_data = load_airtable_data()
    if not airtable_data:
        sys.exit(1)
    
    fathom_data = load_fathom_data()
    if not fathom_data:
        sys.exit(1)
    
    # Perform correlation
    matches, unmatched_airtable, unmatched_fathom = cross_correlate(airtable_data, fathom_data)
    
    # Generate report
    generate_correlation_report(matches, unmatched_airtable, unmatched_fathom)
    
    # Summary output
    print(f"\n🎯 CORRELATION RESULTS:")
    print(f"   Matches found: {len(matches)}")
    print(f"   Unmatched Airtable members: {len(unmatched_airtable)}")
    print(f"   Unmatched Fathom participants: {len(unmatched_fathom)}")
    
    donor_matches = sum(1 for m in matches if m['airtable_record']['is_donor'] == 'True')
    print(f"   Donors who participate in calls: {donor_matches}")
    
    print(f"\n📄 Detailed report: cross_correlation_report.txt")

if __name__ == "__main__":
    main()
