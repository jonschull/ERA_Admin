#!/usr/bin/env python3
"""
Test navigation integrity in generated documentation tree.
"""

import os
import re
from pathlib import Path
from typing import Set, Dict, List

def find_all_links(file_path: Path, content: str) -> List[str]:
    """Extract all markdown links from content."""
    # Pattern: [text](path)
    pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    matches = re.findall(pattern, content)
    
    links = []
    for text, link in matches:
        # Skip external links, anchors, data URIs
        if link.startswith('http') or link.startswith('#') or link.startswith('data:'):
            continue
        links.append(link)
    
    return links


def resolve_link(from_file: Path, link: str, base_dir: Path) -> Path:
    """Resolve relative link to target path within base_dir."""
    # Strip fragment anchors (#section)
    if '#' in link:
        link = link.split('#')[0]
    
    # If empty after stripping anchor, it's a self-reference
    if not link:
        return from_file
    
    # Resolve relative to the file's directory
    from_dir = from_file.parent
    target = (from_dir / link)
    
    # Normalize the path (resolve .. and .)
    # Use os.path.normpath to avoid resolve() issues with relative paths
    target_str = os.path.normpath(str(target))
    target = Path(target_str)
    
    return target


def test_navigation(docs_dir: str = 'docs_generated'):
    """Test navigation integrity."""
    base_path = Path(docs_dir)
    
    if not base_path.exists():
        print(f"❌ Directory not found: {docs_dir}")
        return False
    
    # Find all markdown files
    md_files = set(base_path.rglob('*.md'))
    print(f"📁 Found {len(md_files)} markdown files\n")
    
    # Track links
    all_files = set()
    linked_files = set()
    links_to_root = {}
    broken_links = []
    
    for md_file in md_files:
        rel_path = md_file.relative_to(base_path)
        all_files.add(rel_path)
        
        # Read content
        content = md_file.read_text()
        
        # Find links
        links = find_all_links(md_file, content)
        
        # Check if this file links back to root
        has_root_link = False
        
        for link in links:
            try:
                # Resolve link relative to this file's location
                target = resolve_link(rel_path, link, base_path)
                
                # Make target relative to base_path for comparison
                if target.is_absolute():
                    # Skip absolute paths outside our tree
                    continue
                    
                # Normalize target path
                target_normalized = Path(os.path.normpath(str(target)))
                
                # Check if target exists
                target_full = base_path / target_normalized
                if target_full.exists():
                    linked_files.add(target_normalized)
                else:
                    broken_links.append((rel_path, link, f"File not found: {target_normalized}"))
                
                # Check if it's README.md in root
                if target_normalized == Path('README.md'):
                    has_root_link = True
                    
            except Exception as e:
                broken_links.append((rel_path, link, str(e)))
        
        links_to_root[rel_path] = has_root_link
    
    # Find orphans (files not linked to)
    orphans = all_files - linked_files
    
    # Find files without path to root (exclude .github files - they're templates)
    no_root_path = [f for f, has_link in links_to_root.items() 
                    if not has_link 
                    and f != Path('README.md')
                    and not str(f).startswith('.github/')]
    
    print("=" * 60)
    print("NAVIGATION TEST RESULTS")
    print("=" * 60)
    print()
    
    # Report orphans
    if orphans:
        print(f"⚠️  ORPHANS ({len(orphans)} files not linked to):")
        for orphan in sorted(orphans):
            print(f"   - {orphan}")
        print()
    else:
        print("✅ No orphans - all files are linked to")
        print()
    
    # Report files without root path
    if no_root_path:
        print(f"⚠️  NO PATH TO ROOT ({len(no_root_path)} files):")
        for file in sorted(no_root_path):
            print(f"   - {file}")
        print()
    else:
        print("✅ All files have path back to /README.md")
        print()
    
    # Report broken links
    if broken_links:
        print(f"❌ BROKEN LINKS ({len(broken_links)}):")
        for from_file, link, error in broken_links:
            print(f"   {from_file} -> {link}")
            print(f"      Error: {error}")
        print()
    else:
        print("✅ No broken links detected")
        print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total files: {len(all_files)}")
    print(f"Orphans: {len(orphans)}")
    print(f"No root path: {len(no_root_path)}")
    print(f"Broken links: {len(broken_links)}")
    print()
    
    if not orphans and not no_root_path and not broken_links:
        print("🎉 NAVIGATION INTEGRITY: PERFECT")
        return True
    else:
        print("⚠️  NAVIGATION ISSUES DETECTED")
        return False


if __name__ == '__main__':
    import sys
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else 'docs_generated'
    success = test_navigation(docs_dir)
    sys.exit(0 if success else 1)
