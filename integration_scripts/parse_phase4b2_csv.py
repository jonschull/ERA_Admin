#!/usr/bin/env python3
"""
Phase 4B-2 CSV Parser - Single Source of Truth
===============================================

This module parses the Phase 4B-2 approval CSV and categorizes actions.
DO NOT create ad-hoc parsing logic elsewhere - USE THIS.

Purpose:
- Prevent logic degradation across different scripts
- Ensure consistent handling of ProcessThis/Probe flags
- Properly detect custom comments that need human discussion
- Provide clear AI guidance when custom comments are found

Usage:
    from parse_phase4b2_csv import parse_csv
    result = parse_csv('path/to/csv')
    
    # Check for issues first
    if result['custom_comments']:
        print("⚠️  Custom comments need discussion!")
        for item in result['custom_comments']:
            print(f"  • {item['name']}: {item['comment']}")
    
    # Then process standard actions
    for merge in result['merges']:
        execute_merge(merge['fathom_name'], merge['target_name'])
"""

import csv
from pathlib import Path
from typing import Dict, List, Any


def is_standard_comment(comment: str) -> bool:
    """
    Check if comment follows standard action format.
    
    Standard formats:
    - "merge with: Name"
    - "add to airtable"
    - "drop"
    - "ignore"
    - Empty/whitespace only
    
    Returns:
        True if standard format, False if custom
    """
    if not comment or not comment.strip():
        return True
    
    comment_lower = comment.lower().strip()
    
    standard_patterns = [
        'merge with:',
        'add to airtable',
        'drop',
        'ignore',
    ]
    
    return any(comment_lower.startswith(pattern) for pattern in standard_patterns)


def parse_csv(csv_path: str) -> Dict[str, Any]:
    """
    Parse Phase 4B-2 approval CSV into categorized actions.
    
    This is the SINGLE SOURCE OF TRUTH for CSV parsing.
    Do not create ad-hoc parsing logic elsewhere.
    
    Args:
        csv_path: Path to the CSV file
    
    Returns:
        Dictionary with:
        - merges: List of {fathom_name, target_name, record_count}
        - drops: List of {fathom_name, reason}
        - adds: List of {fathom_name}
        - custom_comments: List of {name, comment, process_this, probe}
        - probe_items: List of items with Probe=YES
        - warnings: List of warning messages for AI
    
    Key behavior:
        - Custom comments BLOCK execution until discussed
        - Probe=YES items are flagged for AI review
        - ProcessThis=YES determines if action should execute
    """
    
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Initialize result structure
    result = {
        'merges': [],
        'drops': [],
        'adds': [],
        'custom_comments': [],
        'probe_items': [],
        'warnings': [],
        'total_rows': len(rows),
        'csv_path': str(csv_path),
    }
    
    # Process each row
    for row in rows:
        name = row['Fathom_Name']
        comment = row.get('Comments', '').strip()
        process_this = row.get('ProcessThis', '').upper() == 'YES'
        probe = row.get('Probe', '').upper() == 'YES'
        
        # Detect custom comments - IMPORTANT: Check BOTH flags!
        if comment and not is_standard_comment(comment):
            result['custom_comments'].append({
                'name': name,
                'comment': comment,
                'process_this': process_this,
                'probe': probe,
            })
        
        # Flag probe items
        if probe:
            result['probe_items'].append({
                'name': name,
                'comment': comment,
                'process_this': process_this,
            })
        
        # Only process items marked ProcessThis=YES
        if not process_this:
            continue
        
        # Categorize standard actions
        comment_lower = comment.lower()
        
        if comment_lower.startswith('merge with:'):
            target = comment.split('merge with:', 1)[1].strip()
            result['merges'].append({
                'fathom_name': name,
                'target_name': target,
            })
        
        elif comment_lower.startswith('drop'):
            result['drops'].append({
                'fathom_name': name,
                'reason': comment,
            })
        
        elif comment_lower.startswith('add to airtable'):
            result['adds'].append({
                'fathom_name': name,
            })
    
    # Generate AI warnings
    if result['custom_comments']:
        result['warnings'].append(
            f"⚠️  CRITICAL: {len(result['custom_comments'])} custom comments detected. "
            "DO NOT AUTO-EXECUTE. Discuss with user first."
        )
    
    if result['probe_items']:
        result['warnings'].append(
            f"🔍 {len(result['probe_items'])} items marked for probing. Review before executing."
        )
    
    return result


def print_summary(result: Dict[str, Any]) -> None:
    """
    Print a human-readable summary of the parsed CSV.
    Use this to show the user what will be executed.
    """
    print("\n" + "=" * 80)
    print("📋 PHASE 4B-2 CSV PARSE SUMMARY")
    print("=" * 80)
    print(f"CSV: {result['csv_path']}")
    print(f"Total rows: {result['total_rows']}")
    print()
    
    print("📊 ACTIONS TO EXECUTE:")
    print(f"   🔀 Merges: {len(result['merges'])}")
    print(f"   🗑️  Drops: {len(result['drops'])}")
    print(f"   ➕ Adds: {len(result['adds'])}")
    print()
    
    print("🔍 NEEDS ATTENTION:")
    print(f"   💬 Custom comments: {len(result['custom_comments'])}")
    print(f"   🔍 Probe items: {len(result['probe_items'])}")
    print()
    
    # Show warnings
    if result['warnings']:
        print("⚠️  WARNINGS FOR AI:")
        for warning in result['warnings']:
            print(f"   {warning}")
        print()
    
    # Show custom comments (blocking issue)
    if result['custom_comments']:
        print("=" * 80)
        print("💬 CUSTOM COMMENTS - REQUIRES DISCUSSION")
        print("=" * 80)
        print()
        print("AI: DO NOT execute actions until these are discussed with user.")
        print("These comments don't match standard patterns and need clarification.")
        print()
        for item in result['custom_comments']:
            print(f"• {item['name']}")
            print(f"  Comment: {item['comment']}")
            print(f"  ProcessThis: {'YES' if item['process_this'] else 'NO'}")
            print(f"  Probe: {'YES' if item['probe'] else 'NO'}")
            print()
    
    # Show sample merges
    if result['merges']:
        print("=" * 80)
        print("🔀 SAMPLE MERGES (first 10)")
        print("=" * 80)
        for merge in result['merges'][:10]:
            print(f"   • {merge['fathom_name']} → {merge['target_name']}")
        if len(result['merges']) > 10:
            print(f"   ... and {len(result['merges'])-10} more")


def has_blocking_issues(result: Dict[str, Any]) -> bool:
    """
    Check if there are issues that should block execution.
    
    Returns:
        True if execution should be blocked, False otherwise
    """
    return len(result['custom_comments']) > 0


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python parse_phase4b2_csv.py <csv_file>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    result = parse_csv(csv_path)
    print_summary(result)
    
    if has_blocking_issues(result):
        print("\n" + "=" * 80)
        print("🛑 EXECUTION BLOCKED")
        print("=" * 80)
        print("Custom comments must be discussed with user before proceeding.")
        sys.exit(1)
    else:
        print("\n✅ Ready to execute - no blocking issues")
        sys.exit(0)
