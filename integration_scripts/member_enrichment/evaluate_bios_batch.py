#!/usr/bin/env python3
"""
Intelligent Bio Evaluation - Batch Processing

Purpose: Read and evaluate bio quality for Airtable and Fathom bios
Process in batches of 10 with user feedback between batches

Scoring Rubric (0-100):
- 90-100: Excellent - All criteria met, ERA relevance clear, professional, concise
- 70-89: Good - Most criteria met, minor improvements possible
- 50-69: Adequate - Has basics but missing ERA relevance or too generic
- 30-49: Poor - Generic, promotional, or missing key information
- 0-29: Inadequate - Needs complete rewrite

Good ERA Bio Characteristics:
1. ✅ ERA relevance clearly stated - Why this person matters to ERA
2. ✅ Current role & organization - What they do now, where
3. ✅ Third-person, professional tone - Not "I am...", not promotional
4. ✅ Concise and focused - 2-4 sentences typical, but can be shorter if complete
5. ❌ Avoids promotional language - No "world-leading", "innovative solutions"
6. ❌ Avoids generic LinkedIn speak - Not copy-paste career summaries
"""

import pandas as pd
import sqlite3
from pathlib import Path
import sys

# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CSV_FILE = SCRIPT_DIR / "member_reconciliation_report.csv"
FATHOM_DB = PROJECT_ROOT / "FathomInventory" / "fathom_emails.db"
AIRTABLE_CSV = PROJECT_ROOT / "airtable" / "people_export.csv"
HTML_NOTES = SCRIPT_DIR / "bio_evaluation_notes.html"
CONTEXT_DOC = SCRIPT_DIR / "Oct_29_Context_Recovery.md"

BATCH_SIZE = 10

def read_context_document():
    """Re-read context document to refresh understanding."""
    print("=" * 80)
    print("RE-READING CONTEXT DOCUMENT")
    print("=" * 80)
    print()
    
    if not CONTEXT_DOC.exists():
        print(f"⚠️  Context document not found: {CONTEXT_DOC}")
        return
    
    with open(CONTEXT_DOC, 'r') as f:
        content = f.read()
    
    # Extract key sections
    lines = content.split('\n')
    in_rubric = False
    rubric_lines = []
    
    for line in lines:
        if 'Scoring Rubric' in line:
            in_rubric = True
        elif in_rubric and line.startswith('**'):
            rubric_lines.append(line)
        elif in_rubric and line.startswith('##'):
            break
    
    print("Scoring Rubric refreshed:")
    for line in rubric_lines[:5]:
        print(f"   {line}")
    print()
    print("✅ Context refreshed - ready to evaluate next batch")
    print()

def load_data():
    """Load CSV and bio data."""
    print("=" * 80)
    print("LOADING DATA")
    print("=" * 80)
    print()
    
    # Load CSV
    df = pd.read_csv(CSV_FILE)
    print(f"✅ Loaded {len(df)} rows from CSV")
    
    # Load Airtable bios
    airtable_df = pd.read_csv(AIRTABLE_CSV)
    print(f"✅ Loaded {len(airtable_df)} Airtable records")
    
    # Load Fathom bios
    conn = sqlite3.connect(FATHOM_DB)
    fathom_df = pd.read_sql_query("SELECT name, bio FROM participants WHERE bio IS NOT NULL", conn)
    conn.close()
    print(f"✅ Loaded {len(fathom_df)} Fathom bios")
    print()
    
    return df, airtable_df, fathom_df

def create_anchor(name):
    """Create HTML anchor from name."""
    return name.lower().replace(' ', '-').replace('.', '').replace(',', '')

def evaluate_bio(name, bio, source):
    """
    Intelligently evaluate a bio.
    
    Returns: (score, reasoning, issues)
    """
    if pd.isna(bio) or str(bio).strip() == '':
        return 0, "No bio provided", ["Missing bio"]
    
    bio_str = str(bio).strip()
    score = 50  # Start at adequate
    reasoning = []
    issues = []
    
    # Check 1: ERA relevance
    era_keywords = ['restoration', 'ecosystem', 'climate', 'regenerative', 'biodiversity', 
                    'conservation', 'soil', 'water', 'forest', 'agriculture', 'ERA']
    has_era_relevance = any(keyword.lower() in bio_str.lower() for keyword in era_keywords)
    
    if has_era_relevance:
        score += 15
        reasoning.append("✅ ERA-relevant keywords present")
    else:
        issues.append("❌ No clear ERA relevance")
    
    # Check 2: Current role/organization mentioned
    role_indicators = ['is a', 'is an', 'serves as', 'works as', 'director', 'founder', 
                       'president', 'coordinator', 'consultant', 'researcher']
    has_role = any(indicator.lower() in bio_str.lower() for indicator in role_indicators)
    
    if has_role:
        score += 15
        reasoning.append("✅ Current role/organization mentioned")
    else:
        issues.append("❌ Current role unclear")
    
    # Check 3: Third person (not first person)
    first_person = ['I am', 'I have', 'I work', 'My ', 'I\'m', 'I focus']
    is_first_person = any(fp.lower() in bio_str.lower() for fp in first_person)
    
    if not is_first_person:
        score += 10
        reasoning.append("✅ Third-person tone")
    else:
        score -= 10
        issues.append("❌ First-person language (should be third-person)")
    
    # Check 4: Concise (not rambling)
    word_count = len(bio_str.split())
    if word_count < 20:
        reasoning.append(f"⚠️  Very short ({word_count} words) - may lack detail")
        if not has_era_relevance or not has_role:
            score -= 10
            issues.append("❌ Too brief without key information")
    elif 20 <= word_count <= 100:
        score += 10
        reasoning.append(f"✅ Concise length ({word_count} words)")
    elif 100 < word_count <= 200:
        reasoning.append(f"✅ Good length ({word_count} words)")
    else:
        reasoning.append(f"⚠️  Long ({word_count} words) - may be rambling")
        score -= 5
    
    # Check 5: Avoid promotional language
    promotional = ['world-leading', 'innovative', 'cutting-edge', 'revolutionary', 
                   'groundbreaking', 'award-winning', 'premier', 'leading expert']
    has_promotional = any(promo.lower() in bio_str.lower() for promo in promotional)
    
    if has_promotional:
        score -= 15
        issues.append("❌ Promotional language detected")
    else:
        reasoning.append("✅ No promotional language")
    
    # Check 6: Avoid generic LinkedIn speak
    generic_phrases = ['passionate about', 'dedicated to', 'committed to excellence',
                       'results-oriented', 'team player', 'think outside the box']
    has_generic = any(generic.lower() in bio_str.lower() for generic in generic_phrases)
    
    if has_generic:
        score -= 10
        issues.append("❌ Generic LinkedIn phrases")
    else:
        reasoning.append("✅ Avoids generic language")
    
    # Cap score at 0-100
    score = max(0, min(100, score))
    
    return score, reasoning, issues

def evaluate_batch(df, airtable_df, fathom_df, start_idx, batch_num):
    """Evaluate a batch of 10 bios."""
    print("=" * 80)
    print(f"BATCH {batch_num}: Evaluating rows {start_idx} to {start_idx + BATCH_SIZE - 1}")
    print("=" * 80)
    print()
    
    batch_results = []
    end_idx = min(start_idx + BATCH_SIZE, len(df))
    
    for idx in range(start_idx, end_idx):
        row = df.iloc[idx]
        name = row['name_airtable']
        
        print(f"📝 {idx + 1}/{len(df)}: {name}")
        
        # Get Airtable bio
        airtable_bio = airtable_df[airtable_df['Name'] == name]['Bio'].iloc[0] if len(airtable_df[airtable_df['Name'] == name]) > 0 else None
        
        # Get Fathom bio if matched
        fathom_bio = None
        fathom_name = row['name_database']
        if pd.notna(fathom_name) and fathom_name != '':
            fathom_matches = fathom_df[fathom_df['name'] == fathom_name]
            if len(fathom_matches) > 0:
                fathom_bio = fathom_matches['bio'].iloc[0]
        
        # Evaluate Airtable bio
        at_score, at_reasoning, at_issues = evaluate_bio(name, airtable_bio, 'Airtable')
        
        # Evaluate Fathom bio if exists
        if fathom_bio:
            fathom_score, fathom_reasoning, fathom_issues = evaluate_bio(name, fathom_bio, 'Fathom')
        else:
            fathom_score, fathom_reasoning, fathom_issues = None, None, None
        
        # Store results
        batch_results.append({
            'idx': idx,
            'name': name,
            'airtable_bio': airtable_bio,
            'airtable_score': at_score,
            'airtable_reasoning': at_reasoning,
            'airtable_issues': at_issues,
            'fathom_bio': fathom_bio,
            'fathom_score': fathom_score,
            'fathom_reasoning': fathom_reasoning,
            'fathom_issues': fathom_issues
        })
        
        print(f"   Airtable: {at_score}/100")
        if fathom_score:
            print(f"   Fathom:   {fathom_score}/100")
        print()
    
    return batch_results

def generate_html_batch(batch_results, batch_num, append=False):
    """Generate or append HTML notes for batch."""
    mode = 'a' if append else 'w'
    
    with open(HTML_NOTES, mode) as f:
        if not append:
            # Write header
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Bio Evaluation Notes</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .person { border: 1px solid #ccc; padding: 15px; margin: 20px 0; }
        .name { font-size: 1.5em; font-weight: bold; color: #333; }
        .score { font-size: 1.2em; margin: 10px 0; }
        .excellent { color: #0a0; }
        .good { color: #080; }
        .adequate { color: #880; }
        .poor { color: #c60; }
        .inadequate { color: #c00; }
        .bio { background: #f5f5f5; padding: 10px; margin: 10px 0; border-left: 3px solid #999; }
        .reasoning { margin: 10px 0; }
        .issue { color: #c00; }
        .batch-header { background: #e0e0e0; padding: 10px; margin: 20px 0; font-size: 1.3em; }
    </style>
</head>
<body>
<h1>Bio Evaluation Notes</h1>
<p>Generated: """ + pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
""")
        
        # Write batch header
        f.write(f'\n<div class="batch-header">Batch {batch_num}</div>\n')
        
        # Write each person
        for result in batch_results:
            anchor = create_anchor(result['name'])
            at_score = result['airtable_score']
            
            # Determine score class
            if at_score >= 90:
                score_class = 'excellent'
            elif at_score >= 70:
                score_class = 'good'
            elif at_score >= 50:
                score_class = 'adequate'
            elif at_score >= 30:
                score_class = 'poor'
            else:
                score_class = 'inadequate'
            
            f.write(f'\n<div class="person" id="{anchor}">\n')
            f.write(f'<div class="name">{result["name"]}</div>\n')
            
            # Airtable bio
            f.write(f'<h3>Airtable Bio</h3>\n')
            f.write(f'<div class="score {score_class}">Score: {at_score}/100</div>\n')
            f.write(f'<div class="bio">{result["airtable_bio"]}</div>\n')
            f.write('<div class="reasoning">\n')
            for reason in result['airtable_reasoning']:
                f.write(f'<div>{reason}</div>\n')
            for issue in result['airtable_issues']:
                f.write(f'<div class="issue">{issue}</div>\n')
            f.write('</div>\n')
            
            # Fathom bio if exists
            if result['fathom_bio']:
                fathom_score = result['fathom_score']
                if fathom_score >= 90:
                    fathom_class = 'excellent'
                elif fathom_score >= 70:
                    fathom_class = 'good'
                elif fathom_score >= 50:
                    fathom_class = 'adequate'
                elif fathom_score >= 30:
                    fathom_class = 'poor'
                else:
                    fathom_class = 'inadequate'
                
                f.write(f'<h3>Fathom DB Bio</h3>\n')
                f.write(f'<div class="score {fathom_class}">Score: {fathom_score}/100</div>\n')
                f.write(f'<div class="bio">{result["fathom_bio"]}</div>\n')
                f.write('<div class="reasoning">\n')
                for reason in result['fathom_reasoning']:
                    f.write(f'<div>{reason}</div>\n')
                for issue in result['fathom_issues']:
                    f.write(f'<div class="issue">{issue}</div>\n')
                f.write('</div>\n')
            
            f.write('</div>\n')
        
        if not append:
            f.write('\n</body>\n</html>')

def update_csv_batch(df, batch_results):
    """Update CSV with scores and links for this batch."""
    for result in batch_results:
        idx = result['idx']
        anchor = create_anchor(result['name'])
        
        # Update scores (replace placeholder with intelligent scores)
        df.at[idx, 'bio_quality_airtable'] = f"{result['airtable_score']}"
        if result['fathom_score']:
            df.at[idx, 'bio_quality_database'] = f"{result['fathom_score']}"
        
        # Add link to HTML notes
        df.at[idx, 'bio_evaluation_link'] = f"bio_evaluation_notes.html#{anchor}"
    
    return df

def main():
    """Main batch processing loop."""
    print()
    print("=" * 80)
    print("INTELLIGENT BIO EVALUATION - BATCH PROCESSING")
    print("=" * 80)
    print()
    
    # Initial context read
    read_context_document()
    
    # Load data
    df, airtable_df, fathom_df = load_data()
    
    # Determine starting batch
    print("Starting batch processing...")
    print(f"Total rows to evaluate: {len(df)}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Total batches: {(len(df) + BATCH_SIZE - 1) // BATCH_SIZE}")
    print()
    
    batch_num = 1
    start_idx = 0
    
    # Process first batch
    print(f"Processing Batch {batch_num}...")
    print()
    
    batch_results = evaluate_batch(df, airtable_df, fathom_df, start_idx, batch_num)
    generate_html_batch(batch_results, batch_num, append=False)
    df = update_csv_batch(df, batch_results)
    
    # Save CSV
    df.to_csv(CSV_FILE, index=False)
    
    print("=" * 80)
    print(f"BATCH {batch_num} COMPLETE")
    print("=" * 80)
    print()
    print(f"✅ Evaluated {len(batch_results)} bios")
    print(f"✅ Updated CSV: {CSV_FILE}")
    print(f"✅ Generated HTML: {HTML_NOTES}")
    print()
    print("Summary of scores:")
    for result in batch_results:
        print(f"   {result['name']}: Airtable={result['airtable_score']}", end='')
        if result['fathom_score']:
            print(f", Fathom={result['fathom_score']}")
        else:
            print()
    print()
    print("=" * 80)
    print("WAITING FOR USER FEEDBACK")
    print("=" * 80)
    print()
    print("Please review:")
    print(f"1. HTML notes: {HTML_NOTES}")
    print(f"2. Updated CSV: {CSV_FILE}")
    print()
    print("Provide feedback on:")
    print("- Are the scores reasonable?")
    print("- Any corrections to scoring logic?")
    print("- Should I continue to next batch?")
    print()
    print("After approval, run this script again to continue.")

if __name__ == "__main__":
    main()
