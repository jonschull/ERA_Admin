#!/usr/bin/env python3
"""
Validate NAVIGATION_WIREFRAME.md against actual filesystem.

Tests:
1. Every ## FILE: path in wireframe exists on disk
2. Reports important files NOT in wireframe
3. Validates wireframe-documented paths are accurate
"""

import re
from pathlib import Path
from typing import Set, List, Tuple

def extract_wireframe_files(wireframe_path: str) -> Set[str]:
    """Extract all ## FILE: paths from wireframe."""
    with open(wireframe_path, 'r') as f:
        content = f.read()
    
    # Pattern: ## FILE: path/to/file.md
    pattern = r'^## FILE: (.+\.md)$'
    matches = re.findall(pattern, content, re.MULTILINE)
    
    return set(matches)

def find_actual_markdown_files(repo_root: str, exclude_dirs: Set[str] = None) -> Set[str]:
    """Find all markdown files in repo, excluding certain directories."""
    if exclude_dirs is None:
        exclude_dirs = {
            'venv', 'node_modules', '__pycache__', 
            '.git', 'docs_generated', 'historical'
        }
    
    repo_path = Path(repo_root)
    md_files = set()
    
    for md_file in repo_path.rglob('*.md'):
        # Check if any excluded dir in path
        if any(excluded in md_file.parts for excluded in exclude_dirs):
            continue
        
        # Get relative path from repo root
        try:
            rel_path = md_file.relative_to(repo_path)
            md_files.add(str(rel_path))
        except ValueError:
            continue
    
    return md_files

def categorize_undocumented(files: Set[str]) -> dict:
    """Categorize undocumented files by type."""
    categories = {
        'root_strategic': [],
        'planning': [],
        'session_notes': [],
        'working_files': [],
        'other': []
    }
    
    planning_patterns = ['PLAN', 'ECOSYSTEM', 'CONSOLIDATION', 'PROTOTYPE']
    session_patterns = ['SESSION', 'SUMMARY', 'RETROSPECTIVE', 'DIFF']
    strategic_patterns = ['INTELLIGENT_ASSISTANT', 'WORKING_PRINCIPLES', 'AI_HANDOFF']
    working_patterns = ['PAST_LEARNINGS', 'REDUNDANCY', 'CLEANUP', 'TODO']
    
    for file in files:
        file_upper = file.upper()
        
        if any(p in file_upper for p in strategic_patterns):
            categories['root_strategic'].append(file)
        elif any(p in file_upper for p in planning_patterns):
            categories['planning'].append(file)
        elif any(p in file_upper for p in session_patterns):
            categories['session_notes'].append(file)
        elif any(p in file_upper for p in working_patterns):
            categories['working_files'].append(file)
        else:
            categories['other'].append(file)
    
    return categories

def main():
    """Main validation."""
    wireframe_path = 'NAVIGATION_WIREFRAME.md'
    repo_root = '..'  # Run from docs/ directory
    
    print("=" * 70)
    print("WIREFRAME VS FILESYSTEM VALIDATION")
    print("=" * 70)
    print()
    
    # Extract wireframe files
    print("📖 Reading NAVIGATION_WIREFRAME.md...")
    wireframe_files = extract_wireframe_files(wireframe_path)
    print(f"   Found {len(wireframe_files)} documented files")
    print()
    
    # Find actual files
    print("📁 Scanning filesystem...")
    actual_files = find_actual_markdown_files(repo_root)
    print(f"   Found {len(actual_files)} total markdown files")
    print()
    
    # Test 1: Files in wireframe exist on disk?
    print("=" * 70)
    print("TEST 1: Wireframe Files Exist on Disk")
    print("=" * 70)
    print()
    
    missing_on_disk = wireframe_files - actual_files
    if missing_on_disk:
        print(f"❌ {len(missing_on_disk)} files documented but NOT on disk:")
        for file in sorted(missing_on_disk):
            print(f"   - {file}")
    else:
        print("✅ All wireframe-documented files exist on disk")
    print()
    
    # Test 2: Important files not in wireframe?
    print("=" * 70)
    print("TEST 2: Files on Disk NOT in Wireframe")
    print("=" * 70)
    print()
    
    undocumented = actual_files - wireframe_files
    categorized = categorize_undocumented(undocumented)
    
    print(f"📊 Total undocumented: {len(undocumented)} files")
    print()
    
    if categorized['root_strategic']:
        print("⚠️  ROOT STRATEGIC DOCS (Should be in wireframe?):")
        for file in sorted(categorized['root_strategic']):
            print(f"   - {file}")
        print()
    
    if categorized['working_files']:
        print("📝 WORKING FILES (Mentioned in READMEs, not wireframe?):")
        for file in sorted(categorized['working_files']):
            print(f"   - {file}")
        print()
    
    if categorized['planning']:
        print("📋 PLANNING DOCUMENTS (Expected to be undocumented):")
        for file in sorted(categorized['planning'])[:10]:  # First 10
            print(f"   - {file}")
        if len(categorized['planning']) > 10:
            print(f"   ... and {len(categorized['planning']) - 10} more")
        print()
    
    if categorized['session_notes']:
        print("📓 SESSION NOTES (Expected to be undocumented):")
        for file in sorted(categorized['session_notes'])[:10]:
            print(f"   - {file}")
        if len(categorized['session_notes']) > 10:
            print(f"   ... and {len(categorized['session_notes']) - 10} more")
        print()
    
    if categorized['other']:
        print("📄 OTHER FILES:")
        for file in sorted(categorized['other'])[:10]:
            print(f"   - {file}")
        if len(categorized['other']) > 10:
            print(f"   ... and {len(categorized['other']) - 10} more")
        print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Documented in wireframe: {len(wireframe_files)}")
    print(f"Exist on filesystem: {len(actual_files)}")
    print(f"Missing from disk: {len(missing_on_disk)}")
    print(f"Undocumented: {len(undocumented)}")
    print()
    print(f"  - Root strategic: {len(categorized['root_strategic'])} ⚠️")
    print(f"  - Working files: {len(categorized['working_files'])} 📝")
    print(f"  - Planning docs: {len(categorized['planning'])}")
    print(f"  - Session notes: {len(categorized['session_notes'])}")
    print(f"  - Other: {len(categorized['other'])}")
    print()
    
    if missing_on_disk:
        print("❌ ISSUES: Some wireframe files don't exist")
    elif categorized['root_strategic']:
        print("⚠️  ATTENTION: Strategic docs not in wireframe")
    else:
        print("✅ VALIDATION PASSED")
    print()

if __name__ == '__main__':
    main()
