#!/usr/bin/env python3
"""
Analyze bios in Airtable vs Fathom DB.
Generate CSV report for review and action planning.
"""

import sqlite3
import csv
import re
from pathlib import Path
from difflib import SequenceMatcher

# Paths
FATHOM_DB = Path(__file__).parent.parent.parent / "FathomInventory" / "fathom_emails.db"
AIRTABLE_CSV = Path(__file__).parent.parent.parent / "airtable" / "people_export.csv"
OUTPUT_CSV = Path(__file__).parent / "airtable_bio_audit.csv"

def assess_bio_quality(bio):
    """Assess bio quality: GOOD, BAD, or MISSING."""
    if not bio or not bio.strip():
        return "MISSING"
    
    bio = bio.strip()
    word_count = len(bio.split())
    
    # Check for first person indicators
    first_person = bool(re.search(r'\b(I\'m|I am|My |We |Our |me |us )', bio, re.IGNORECASE))
    
    # Check for age references
    age_ref = bool(re.search(r'\b\d{2}\s*year[s]?\s*old\b', bio, re.IGNORECASE))
    
    # Check sentence count (rough estimate)
    sentence_count = len(re.findall(r'[.!?]+', bio))
    
    # Determine quality
    issues = []
    if first_person:
        issues.append("first_person")
    if age_ref:
        issues.append("age_ref")
    if word_count < 20:
        issues.append("too_short")
    if word_count > 200:
        issues.append("too_long")
    
    if not issues and sentence_count >= 2:
        return "GOOD"
    elif len(issues) <= 1:
        return "OK"
    else:
        return "BAD"

def get_fathom_data():
    """Get all participants from Fathom DB with member status and bios."""
    conn = sqlite3.connect(FATHOM_DB)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name, era_member, bio
        FROM participants
    """)
    
    fathom_data = {}
    for row in cursor.fetchall():
        name = row[0]
        fathom_data[name.lower().strip()] = {
            'name': name,
            'era_member': row[1],
            'bio': row[2] if row[2] else ''
        }
    
    conn.close()
    return fathom_data

def normalize_name(name):
    """Normalize name for better matching - remove suffixes, parentheticals."""
    name = name.strip()
    # Remove common suffixes in parentheses
    name = re.sub(r'\s*\([^)]*\)\s*$', '', name)  # Remove (FTA), (PhD), etc.
    # Remove common title suffixes
    name = re.sub(r',?\s*(PhD|Jr\.?|Sr\.?|III|IV|MD)\s*$', '', name, flags=re.IGNORECASE)
    return name.strip()

def similarity_ratio(a, b):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def fuzzy_match(name, fathom_data):
    """Try to find a match in Fathom DB (exact or fuzzy)."""
    # Normalize the Airtable name
    normalized_name = normalize_name(name)
    name_lower = normalized_name.lower().strip()
    
    # Exact match
    if name_lower in fathom_data:
        return fathom_data[name_lower]
    
    # Try variations (remove middle names, initials, etc.)
    parts = name_lower.split()
    if len(parts) >= 2:
        # Try first + last
        first_last = f"{parts[0]} {parts[-1]}"
        if first_last in fathom_data:
            return fathom_data[first_last]
    
    # Fuzzy match - find best match above threshold
    best_match = None
    best_ratio = 0.82  # Slightly lower threshold to catch "de Carvalho" vs "Carvalho"
    
    for fathom_name_lower, fathom_person in fathom_data.items():
        ratio = similarity_ratio(normalized_name, fathom_name_lower)
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = fathom_person
    
    return best_match

def determine_action(fathom_match, airtable_quality, fathom_bio_quality):
    """Determine recommended action."""
    if not fathom_match:
        return "NOT_IN_FATHOM_DB"
    
    era_member = fathom_match.get('era_member', 0)
    
    if era_member != 1:
        return "VERIFY_MEMBER_STATUS"
    
    # Member in DB
    if fathom_bio_quality == "MISSING":
        if airtable_quality in ["GOOD", "OK"]:
            return "COPY_FROM_AIRTABLE"
        else:
            return "WRITE_NEW_BIO"
    elif fathom_bio_quality == "BAD":
        if airtable_quality == "GOOD":
            return "REPLACE_WITH_AIRTABLE"
        else:
            return "REWRITE_BIO"
    elif fathom_bio_quality in ["GOOD", "OK"]:
        if airtable_quality == "BAD":
            return "FATHOM_GOOD_KEEP"
        else:
            return "BOTH_GOOD_REVIEW"
    
    return "REVIEW"

def main():
    print("Loading Fathom DB data...")
    fathom_data = get_fathom_data()
    print(f"  Found {len(fathom_data)} participants in Fathom DB")
    
    print("\nLoading Airtable data...")
    airtable_people = []
    with open(AIRTABLE_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            bio = row.get('Bio', '').strip()
            if bio:  # Only people with bios in Airtable
                airtable_people.append({
                    'name': row.get('Name', ''),
                    'bio': bio,
                    'publish': row.get('Publish', '').strip()
                })
    
    print(f"  Found {len(airtable_people)} people with bios in Airtable")
    
    print("\nAnalyzing and generating report...")
    results = []
    
    for person in airtable_people:
        name = person['name']
        airtable_bio = person['bio']
        
        # Find in Fathom DB
        fathom_match = fuzzy_match(name, fathom_data)
        
        # Assess qualities
        airtable_quality = assess_bio_quality(airtable_bio)
        
        if fathom_match:
            fathom_bio = fathom_match.get('bio', '')
            fathom_bio_quality = assess_bio_quality(fathom_bio)
            era_member = "YES" if fathom_match.get('era_member') == 1 else "NO"
            fathom_bio_status = "EXISTS" if fathom_bio else "MISSING"
        else:
            era_member = "NOT_IN_DB"
            fathom_bio_status = "N/A"
            fathom_bio_quality = "N/A"
        
        action = determine_action(fathom_match, airtable_quality, fathom_bio_quality)
        
        results.append({
            'Name': name,
            'era_member_flag': era_member,
            'Fathom_Bio_Status': fathom_bio_status,
            'Fathom_Bio_Quality': fathom_bio_quality,
            'Airtable_Bio_Quality': airtable_quality,
            'Airtable_Publish': person.get('publish', ''),
            'Action_Needed': action,
            'Your_Comments': ''
        })
    
    # Sort by action priority
    action_priority = {
        'VERIFY_MEMBER_STATUS': 1,
        'NOT_IN_FATHOM_DB': 2,
        'REWRITE_BIO': 3,
        'WRITE_NEW_BIO': 4,
        'REPLACE_WITH_AIRTABLE': 5,
        'COPY_FROM_AIRTABLE': 6,
        'BOTH_GOOD_REVIEW': 7,
        'FATHOM_GOOD_KEEP': 8,
        'REVIEW': 9
    }
    results.sort(key=lambda x: action_priority.get(x['Action_Needed'], 99))
    
    # Write CSV
    with open(OUTPUT_CSV, 'w', newline='') as f:
        fieldnames = ['Name', 'era_member_flag', 'Fathom_Bio_Status', 'Fathom_Bio_Quality', 
                      'Airtable_Bio_Quality', 'Airtable_Publish', 'Action_Needed', 'Your_Comments']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n✅ Report generated: {OUTPUT_CSV}")
    print(f"   Total people analyzed: {len(results)}")
    
    # Summary stats
    action_counts = {}
    for result in results:
        action = result['Action_Needed']
        action_counts[action] = action_counts.get(action, 0) + 1
    
    print("\n📊 Action Summary:")
    for action, count in sorted(action_counts.items(), key=lambda x: action_priority.get(x[0], 99)):
        print(f"   {action}: {count}")

if __name__ == '__main__':
    main()
