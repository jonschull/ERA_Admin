#!/usr/bin/env python3
"""
DIAGNOSTIC REPORT: Analyze all past decisions vs current database state.

No changes - just comprehensive analysis to inform fix strategy.
"""

import sqlite3
import csv
from pathlib import Path
from collections import defaultdict

DB_PATH = Path('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')
PAST_DECISIONS_DIR = Path('/Users/admin/ERA_Admin/integration_scripts/past_decisions')

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

def classify_decision(comment):
    """Determine action type and target."""
    comment_lower = comment.lower()
    
    if comment_lower in ['drop', 'drop it', 'duplicate']:
        return 'DROP', None
    elif comment.startswith('merge with:'):
        target = comment[len('merge with:'):].strip()
        return 'MERGE', target
    elif 'add to airtable as' in comment_lower:
        parts = comment.split(' as ', 1)
        if len(parts) == 2:
            target = parts[1].strip()
            return 'ADD_AS', target
    
    return 'OTHER', None

def check_variant_vs_target(conn, variant, target):
    """
    Analyze relationship between variant and target.
    
    Returns dict with:
    - variant_exists: bool
    - target_exists: bool
    - variant_urls: list
    - target_urls: list
    - unique_in_variant: list (URLs variant has that target doesn't)
    - status: classification string
    """
    cursor = conn.cursor()
    result = {
        'variant_exists': False,
        'target_exists': False,
        'variant_urls': [],
        'target_urls': [],
        'unique_in_variant': [],
        'status': 'UNKNOWN'
    }
    
    # Check variant
    cursor.execute("SELECT source_call_url FROM participants WHERE name = ?", (variant,))
    row = cursor.fetchone()
    if row:
        result['variant_exists'] = True
        result['variant_urls'] = [u.strip() for u in row[0].split(',') if u.strip()]
    
    # Check target
    if target:
        cursor.execute("SELECT source_call_url FROM participants WHERE name = ?", (target,))
        row = cursor.fetchone()
        if row:
            result['target_exists'] = True
            result['target_urls'] = [u.strip() for u in row[0].split(',') if u.strip()]
    
    # Determine status
    if not result['variant_exists']:
        result['status'] = 'ALREADY_DONE'
    elif target and not result['target_exists']:
        result['status'] = 'TARGET_MISSING'
    elif target and result['target_exists']:
        # Check for unique URLs
        variant_set = set(result['variant_urls'])
        target_set = set(result['target_urls'])
        result['unique_in_variant'] = list(variant_set - target_set)
        
        if result['unique_in_variant']:
            result['status'] = 'NEEDS_URL_MERGE'
        else:
            result['status'] = 'PURE_DUPLICATE'
    else:
        result['status'] = 'SIMPLE_DELETE'
    
    return result

def main():
    print("=" * 80)
    print("DIAGNOSTIC REPORT: Past Decisions vs Database State")
    print("=" * 80)
    
    # Load decisions
    print("\n📋 Loading past decisions...")
    decisions = load_all_decisions()
    print(f"   Found {len(decisions)} decisions with ProcessThis=YES")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    
    # Analyze each decision
    print("\n🔍 Analyzing each decision...")
    
    categories = defaultdict(list)
    
    for decision in decisions:
        variant = decision['variant']
        comment = decision['comment']
        csv_file = decision['csv_file']
        
        action_type, target = classify_decision(comment)
        analysis = check_variant_vs_target(conn, variant, target)
        
        categories[analysis['status']].append({
            'variant': variant,
            'target': target,
            'action_type': action_type,
            'analysis': analysis,
            'csv_file': csv_file,
            'comment': comment
        })
    
    conn.close()
    
    # Report by category
    print("\n" + "=" * 80)
    print("RESULTS BY CATEGORY")
    print("=" * 80)
    
    # Category 1: Already done
    already_done = categories['ALREADY_DONE']
    print(f"\n✅ ALREADY_DONE: {len(already_done)}")
    print("   (Variant no longer exists - decision was applied previously)")
    
    # Category 2: Pure duplicates (safe to delete)
    pure_dupes = categories['PURE_DUPLICATE']
    print(f"\n✓ PURE_DUPLICATE: {len(pure_dupes)}")
    print("   (Target has all variant's URLs - safe to delete variant)")
    if pure_dupes:
        print("\n   Examples:")
        for item in pure_dupes[:5]:
            print(f"   - {item['variant']:35} → {item['target']}")
    
    # Category 3: Needs URL merge (DATA LOSS RISK)
    needs_merge = categories['NEEDS_URL_MERGE']
    print(f"\n⚠️  NEEDS_URL_MERGE: {len(needs_merge)}")
    print("   (Variant has URLs that target doesn't - must merge before deleting)")
    if needs_merge:
        print("\n   ALL cases:")
        for item in needs_merge:
            unique_count = len(item['analysis']['unique_in_variant'])
            print(f"   - {item['variant']:35} → {item['target']:30} ({unique_count} unique URLs)")
    
    # Category 4: Target missing (BLOCKED)
    target_missing = categories['TARGET_MISSING']
    print(f"\n❌ TARGET_MISSING: {len(target_missing)}")
    print("   (Target person doesn't exist in database - can't merge)")
    if target_missing:
        print("\n   ALL cases:")
        for item in target_missing:
            print(f"   - {item['variant']:35} → {item['target']:30} [MISSING]")
    
    # Category 5: Simple deletes (DROP commands)
    simple_delete = categories['SIMPLE_DELETE']
    print(f"\n🗑️  SIMPLE_DELETE: {len(simple_delete)}")
    print("   (DROP commands - no target, just delete)")
    if simple_delete:
        print("\n   Examples:")
        for item in simple_delete[:10]:
            print(f"   - {item['variant']}")
        if len(simple_delete) > 10:
            print(f"   ... and {len(simple_delete) - 10} more")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total decisions: {len(decisions)}")
    print(f"Already done: {len(already_done)} (✅ no action needed)")
    print(f"Pure duplicates: {len(pure_dupes)} (safe to delete)")
    print(f"Needs URL merge: {len(needs_merge)} (⚠️  must preserve data first)")
    print(f"Target missing: {len(target_missing)} (❌ blocked - needs investigation)")
    print(f"Simple deletes: {len(simple_delete)} (DROP commands)")
    
    remaining_work = len(pure_dupes) + len(needs_merge) + len(target_missing) + len(simple_delete)
    print(f"\n🎯 Remaining work: {remaining_work} items")
    
    # Recommended order of operations
    print("\n" + "=" * 80)
    print("RECOMMENDED FIX ORDER")
    print("=" * 80)
    print(f"1. Fix URL merges first ({len(needs_merge)} items)")
    print(f"   - Preserve data by merging URL lists into targets")
    print(f"   - THEN safe to delete variants")
    print(f"\n2. Delete pure duplicates ({len(pure_dupes)} items)")
    print(f"   - Target already has all URLs")
    print(f"   - Safe to delete immediately")
    print(f"\n3. Process simple deletes ({len(simple_delete)} items)")
    print(f"   - DROP commands with no target")
    print(f"   - Just delete the records")
    print(f"\n4. Investigate target missing ({len(target_missing)} items)")
    print(f"   - Need to understand why target doesn't exist")
    print(f"   - May need to add to Airtable first, or find actual target name")
    
    # Export detailed CSV
    report_path = Path('diagnostic_report_detailed.csv')
    with open(report_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Status', 'Variant', 'Target', 'Action_Type', 
            'Unique_URLs_Count', 'CSV_File', 'Comment'
        ])
        
        for status, items in categories.items():
            for item in items:
                unique_count = len(item['analysis'].get('unique_in_variant', []))
                writer.writerow([
                    status,
                    item['variant'],
                    item.get('target', ''),
                    item['action_type'],
                    unique_count,
                    item['csv_file'],
                    item['comment']
                ])
    
    print(f"\n📄 Detailed CSV: {report_path}")
    print("\n✅ Diagnostic complete - ready to plan fixes!")

if __name__ == '__main__':
    main()
