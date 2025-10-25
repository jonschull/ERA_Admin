#!/usr/bin/env python3
"""
DIAGNOSTIC REPORT V2: Use PAST_LEARNINGS as primary source of truth.

When CSV says "drop" but PAST_LEARNINGS has a mapping, trust PAST_LEARNINGS.
"""

import sqlite3
import csv
import re
from pathlib import Path
from collections import defaultdict

DB_PATH = Path('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')
PAST_DECISIONS_DIR = Path('/Users/admin/ERA_Admin/integration_scripts/past_decisions')
PAST_LEARNINGS_PATH = Path('/Users/admin/ERA_Admin/integration_scripts/PAST_LEARNINGS.md')

def load_past_learnings_mappings():
    """
    Extract name mappings from PAST_LEARNINGS.md.
    
    Returns dict: {variant_name: target_name}
    """
    mappings = {}
    
    with open(PAST_LEARNINGS_PATH, 'r') as f:
        content = f.read()
    
    # Pattern 1: Table format | variant | target | ...
    table_pattern = r'\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|'
    
    for match in re.finditer(table_pattern, content):
        variant = match.group(1).strip()
        target = match.group(2).strip()
        
        # Skip header rows
        if variant in ['Fathom Name', 'Phone', 'Organization', 'Name', '---']:
            continue
        
        # Skip if it looks like a pattern description
        if any(x in variant.lower() for x in ['pattern', 'example', 'format']):
            continue
        
        # Valid mapping
        if variant and target and variant != target:
            mappings[variant] = target
    
    # Pattern 2: Narrative format "variant → target" or "variant → ...as target"
    arrow_pattern = r'["\']?([^"\'\n]+?)["\']?\s*→\s*(?:Already processed as |merge with: ?)?([^"\'\n,\.]+)'
    
    for match in re.finditer(arrow_pattern, content):
        variant = match.group(1).strip()
        target = match.group(2).strip()
        
        # Skip if looks like a description
        if any(x in variant.lower() for x in ['pattern', 'example', 'note']):
            continue
        
        # Valid mapping
        if variant and target and variant != target and len(variant) < 50:
            # Don't override table mappings (table is more authoritative)
            if variant not in mappings:
                mappings[variant] = target
    
    return mappings

def load_all_decisions():
    """Load every decision with ProcessThis=YES."""
    decisions = []
    
    for csv_file in sorted(PAST_DECISIONS_DIR.glob('phase4b2_approvals_batch*.csv')):
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                fathom_name = row.get('Fathom_Name', '').strip().split('🔁')[0].strip()
                comment = row.get('Comments', '').strip()
                process_this = row.get('ProcessThis', '').upper() == 'YES'
                
                if process_this and fathom_name:
                    decisions.append({
                        'variant': fathom_name,
                        'comment': comment,
                        'csv_file': csv_file.name
                    })
    
    return decisions

def get_target_from_comment(comment):
    """Extract target from CSV comment."""
    comment_lower = comment.lower()
    
    if comment_lower in ['drop', 'drop it', 'duplicate']:
        return None
    elif comment.startswith('merge with:'):
        return comment[len('merge with:'):].strip()
    elif 'add to airtable as' in comment_lower:
        parts = comment.split(' as ', 1)
        if len(parts) == 2:
            return parts[1].strip()
    
    return None

def check_variant_vs_target(conn, variant, target):
    """
    Analyze relationship between variant and target.
    Returns detailed analysis dict.
    """
    cursor = conn.cursor()
    result = {
        'variant_exists': False,
        'target_exists': False,
        'variant_urls': [],
        'target_urls': [],
        'unique_in_variant': [],
        'variant_record_count': 0,
        'target_record_count': 0,
        'status': 'UNKNOWN'
    }
    
    # Check variant
    cursor.execute("SELECT source_call_url FROM participants WHERE name = ?", (variant,))
    row = cursor.fetchone()
    if row:
        result['variant_exists'] = True
        result['variant_urls'] = [u.strip() for u in row[0].split(',') if u.strip()]
        cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (variant,))
        result['variant_record_count'] = cursor.fetchone()[0]
    
    # Check target
    if target:
        cursor.execute("SELECT source_call_url FROM participants WHERE name = ?", (target,))
        row = cursor.fetchone()
        if row:
            result['target_exists'] = True
            result['target_urls'] = [u.strip() for u in row[0].split(',') if u.strip()]
            cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (target,))
            result['target_record_count'] = cursor.fetchone()[0]
    
    # Determine status
    if not result['variant_exists']:
        result['status'] = 'ALREADY_DONE'
    elif not target:
        result['status'] = 'TRUE_DROP'
    elif not result['target_exists']:
        result['status'] = 'TARGET_MISSING'
    else:
        # Both exist - check URLs
        variant_set = set(result['variant_urls'])
        target_set = set(result['target_urls'])
        result['unique_in_variant'] = list(variant_set - target_set)
        
        if result['unique_in_variant']:
            result['status'] = 'NEEDS_URL_MERGE'
        else:
            result['status'] = 'PURE_DUPLICATE'
    
    return result

def main():
    print("=" * 80)
    print("DIAGNOSTIC REPORT V2: Using PAST_LEARNINGS as Source of Truth")
    print("=" * 80)
    
    # Load PAST_LEARNINGS mappings
    print("\n📖 Loading PAST_LEARNINGS mappings...")
    learnings_mappings = load_past_learnings_mappings()
    print(f"   Found {len(learnings_mappings)} mappings in PAST_LEARNINGS")
    
    # Load CSV decisions
    print("\n📋 Loading CSV decisions...")
    decisions = load_all_decisions()
    print(f"   Found {len(decisions)} decisions with ProcessThis=YES")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    
    # Analyze each decision with PAST_LEARNINGS override
    print("\n🔍 Analyzing with PAST_LEARNINGS priority...")
    
    categories = defaultdict(list)
    csv_overrides = 0
    
    for decision in decisions:
        variant = decision['variant']
        comment = decision['comment']
        csv_file = decision['csv_file']
        
        # Get target from CSV
        csv_target = get_target_from_comment(comment)
        
        # Override with PAST_LEARNINGS if it exists
        target = learnings_mappings.get(variant, csv_target)
        
        if target and target != csv_target:
            csv_overrides += 1
        
        # Analyze
        analysis = check_variant_vs_target(conn, variant, target)
        
        categories[analysis['status']].append({
            'variant': variant,
            'target': target,
            'csv_target': csv_target,
            'analysis': analysis,
            'csv_file': csv_file,
            'comment': comment,
            'source': 'PAST_LEARNINGS' if target != csv_target else 'CSV'
        })
    
    conn.close()
    
    print(f"   ✅ PAST_LEARNINGS overrode {csv_overrides} CSV decisions")
    
    # Report by category
    print("\n" + "=" * 80)
    print("RESULTS BY CATEGORY")
    print("=" * 80)
    
    # Category 1: Already done
    already_done = categories['ALREADY_DONE']
    print(f"\n✅ ALREADY_DONE: {len(already_done)}")
    print("   (Variant no longer exists - decision was applied)")
    
    # Category 2: Pure duplicates
    pure_dupes = categories['PURE_DUPLICATE']
    print(f"\n✓ PURE_DUPLICATE: {len(pure_dupes)}")
    print("   (Target has all variant's URLs - safe to delete)")
    if pure_dupes:
        print("\n   Sample (first 10):")
        for item in pure_dupes[:10]:
            source = f"[{item['source']}]" if item['source'] == 'PAST_LEARNINGS' else ""
            print(f"   {source:18} {item['variant']:30} → {item['target']}")
    
    # Category 3: Needs URL merge
    needs_merge = categories['NEEDS_URL_MERGE']
    print(f"\n⚠️  NEEDS_URL_MERGE: {len(needs_merge)}")
    print("   (Variant has URLs target doesn't - MUST merge before deleting)")
    if needs_merge:
        print("\n   ALL cases:")
        for item in needs_merge:
            unique_count = len(item['analysis']['unique_in_variant'])
            source = f"[{item['source']}]" if item['source'] == 'PAST_LEARNINGS' else ""
            print(f"   {source:18} {item['variant']:30} → {item['target']:30} ({unique_count} unique URLs)")
    
    # Category 4: Target missing
    target_missing = categories['TARGET_MISSING']
    print(f"\n❌ TARGET_MISSING: {len(target_missing)}")
    print("   (Target doesn't exist in database)")
    if target_missing:
        print("\n   Sample (first 20):")
        for item in target_missing[:20]:
            source = f"[{item['source']}]" if item['source'] == 'PAST_LEARNINGS' else ""
            print(f"   {source:18} {item['variant']:30} → {item['target']}")
        if len(target_missing) > 20:
            print(f"\n   ... and {len(target_missing) - 20} more")
    
    # Category 5: True drops
    true_drops = categories['TRUE_DROP']
    print(f"\n🗑️  TRUE_DROP: {len(true_drops)}")
    print("   (No target specified - genuine drops)")
    if true_drops:
        print("\n   ALL cases:")
        for item in true_drops:
            print(f"   - {item['variant']}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total decisions: {len(decisions)}")
    print(f"PAST_LEARNINGS overrides: {csv_overrides}")
    print(f"")
    print(f"Already done: {len(already_done)} (✅ no action needed)")
    print(f"Pure duplicates: {len(pure_dupes)} (safe to delete)")
    print(f"Needs URL merge: {len(needs_merge)} (⚠️  preserve data first)")
    print(f"Target missing: {len(target_missing)} (❌ needs investigation)")
    print(f"True drops: {len(true_drops)} (safe to delete)")
    
    remaining = len(pure_dupes) + len(needs_merge) + len(target_missing) + len(true_drops)
    print(f"\n🎯 Remaining work: {remaining} items")
    
    # Recommended order
    print("\n" + "=" * 80)
    print("RECOMMENDED FIX ORDER")
    print("=" * 80)
    print(f"1. URL Merges ({len(needs_merge)} items) - CRITICAL, do first")
    print(f"   Preserve data by merging URL lists into targets")
    print(f"")
    print(f"2. Pure Duplicates ({len(pure_dupes)} items)")
    print(f"   Target already has all URLs - safe to delete")
    print(f"")
    print(f"3. True Drops ({len(true_drops)} items)")
    print(f"   No target - safe to delete")
    print(f"")
    print(f"4. Target Missing ({len(target_missing)} items) - INVESTIGATE")
    print(f"   Need to add to Airtable first or find correct target")
    
    # Export detailed CSV
    report_path = Path('diagnostic_report_v2_detailed.csv')
    with open(report_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Status', 'Variant', 'Target', 'CSV_Target', 'Source',
            'Unique_URLs_Count', 'CSV_File', 'Comment'
        ])
        
        for status, items in categories.items():
            for item in items:
                unique_count = len(item['analysis'].get('unique_in_variant', []))
                writer.writerow([
                    status,
                    item['variant'],
                    item.get('target', ''),
                    item.get('csv_target', ''),
                    item['source'],
                    unique_count,
                    item['csv_file'],
                    item['comment']
                ])
    
    print(f"\n📄 Detailed CSV: {report_path}")
    print("\n✅ Diagnostic V2 complete!")

if __name__ == '__main__':
    main()
