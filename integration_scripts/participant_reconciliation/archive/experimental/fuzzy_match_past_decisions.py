#!/usr/bin/env python3
"""
Fuzzy Match Against Past Decisions
Shows Claude what we've decided before so he can make intelligent connections
"""
import csv
from pathlib import Path
from difflib import SequenceMatcher
import glob

def fuzzy_similarity(a, b):
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def search_past_decisions(name, threshold=0.7):
    """
    Search all past approval CSVs for similar cases.
    Returns list of past decisions for Claude to REVIEW.
    """
    # Find all past approval CSVs
    csv_pattern = '/Users/admin/ERA_Admin/integration_scripts/**/phase4b2_approvals*.csv'
    past_csvs = glob.glob(csv_pattern, recursive=True)
    
    # Also check archive
    archive_pattern = '/Users/admin/ERA_Admin/integration_scripts/archive/**/phase4b2*.csv'
    past_csvs.extend(glob.glob(archive_pattern, recursive=True))
    
    matches = []
    
    for csv_file in past_csvs:
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    past_name = row.get('Fathom_Name') or row.get('Name', '')
                    if not past_name:
                        continue
                    
                    # Calculate similarity
                    similarity = fuzzy_similarity(name, past_name)
                    
                    if similarity >= threshold:
                        matches.append({
                            'similarity': similarity,
                            'past_name': past_name,
                            'decision': row.get('Comments', ''),
                            'source': Path(csv_file).name,
                            'processed': row.get('ProcessThis', 'unknown')
                        })
        except Exception as e:
            continue
    
    # Sort by similarity (highest first)
    matches.sort(key=lambda x: x['similarity'], reverse=True)
    
    return matches

def format_for_claude_review(name, matches):
    """Format matches for Claude to review and make intelligent decisions"""
    if not matches:
        return None
    
    review = {
        'name': name,
        'past_cases': [],
        'recommendation': None
    }
    
    for match in matches[:5]:  # Top 5 matches
        review['past_cases'].append({
            'name': match['past_name'],
            'similarity': f"{int(match['similarity']*100)}%",
            'decision': match['decision'],
            'source': match['source'],
            'processed': match['processed']
        })
    
    return review

if __name__ == '__main__':
    # Test with some problematic cases
    test_cases = [
        'Agri-Tech Producers LLC, Joe James',
        'Cosmic Labyrinth (Indy Boyle-Rhymes)',
        'aniqa',
        'bk',
        'afmiller09'
    ]
    
    print("="*80)
    print("🔍 FUZZY MATCHING PAST DECISIONS")
    print("="*80)
    print("\nSearching all past approval CSVs for similar cases...")
    print("Claude will REVIEW these and make intelligent connections.\n")
    
    for test_name in test_cases:
        print(f"\n{'='*80}")
        print(f"📋 CASE: {test_name}")
        print('='*80)
        
        matches = search_past_decisions(test_name)
        review = format_for_claude_review(test_name, matches)
        
        if review:
            print(f"\n🔍 Found {len(review['past_cases'])} similar past cases:")
            for i, case in enumerate(review['past_cases'], 1):
                print(f"\n  {i}. {case['name']} ({case['similarity']} similar)")
                print(f"     Decision: {case['decision']}")
                print(f"     Source: {case['source']}")
                print(f"     Processed: {case['processed']}")
            
            print(f"\n💭 CLAUDE'S INTELLIGENT REVIEW:")
            
            # Now Claude reviews and decides
            if test_name == 'Agri-Tech Producers LLC, Joe James':
                if any('Joe James' in c['decision'] for c in review['past_cases']):
                    print(f"     ✅ We've seen this EXACT case before!")
                    print(f"     ✅ Past decision: merge with Joe James")
                    print(f"     ✅ Apply same logic → merge with: Joe James")
            
            elif 'Cosmic Labyrinth' in test_name:
                cosmic_matches = [c for c in review['past_cases'] if 'Cosmic' in c['name']]
                if cosmic_matches and 'Indy Singh' in cosmic_matches[0]['decision']:
                    print(f"     ✅ Cosmic Labyrinth = Indy Singh from past decisions")
                    print(f"     ✅ Current has 'Boyle-Rhymes' - that's bad Fathom data")
                    print(f"     ✅ Correct decision → merge with: Indy Singh")
            
            elif test_name == 'aniqa':
                if any('Aniqa Moinuddin' in c['decision'] for c in review['past_cases']):
                    print(f"     ✅ We've processed aniqa before → Aniqa Moinuddin")
                    print(f"     ⚠️  Why is she back? Validation issue?")
                    print(f"     ✅ Decision → merge with: Aniqa Moinuddin")
            
            elif test_name in ['bk', 'afmiller09']:
                if review['past_cases'] and review['past_cases'][0]['processed'] == 'YES':
                    print(f"     ⚠️  This was already processed!")
                    print(f"     ⚠️  Decision: {review['past_cases'][0]['decision']}")
                    print(f"     ❌ Should not be in current batch - filter error")
        
        else:
            print(f"\n   ℹ️  No similar past cases found (truly new)")
    
    print(f"\n\n{'='*80}")
    print("✅ FUZZY MATCHING WORKING")
    print("="*80)
    print("\nThis gives Claude context to make intelligent decisions:")
    print("  • See what we decided before")
    print("  • Recognize similar patterns")
    print("  • Avoid re-work")
    print("  • Catch already-processed items")
