#!/usr/bin/env python3
"""
Analyze editorial feedback by comparing AI-generated and human-edited bio files.

Usage:
    python3 analyze_bio_feedback.py batch4_review.AI.md batch4_review.JS.md
"""

import sys
import re
import difflib
from pathlib import Path

def extract_bios(content):
    """Extract individual bio sections from markdown."""
    bios = {}
    
    # Split by ## headers (e.g., "## 1. Alex Carlin")
    sections = re.split(r'^## \d+\. (.+?)$', content, flags=re.MULTILINE)
    
    # sections[0] is header content, then alternating [name, content, name, content...]
    for i in range(1, len(sections), 2):
        if i+1 < len(sections):
            name = sections[i].strip()
            bio_content = sections[i+1].strip()
            bios[name] = bio_content
    
    return bios

def extract_bio_text(bio_section):
    """Extract just the bio paragraph from a section."""
    # Find text between "### Bio" and "### Contact Info"
    match = re.search(r'### Bio.*?\n\n(.+?)\n\n### Contact Info', bio_section, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def compare_texts(ai_text, js_text):
    """Generate word-level diff."""
    ai_words = ai_text.split()
    js_words = js_text.split()
    
    differ = difflib.Differ()
    diff = list(differ.compare(ai_words, js_words))
    
    changes = {
        'removed': [],
        'added': [],
        'unchanged': []
    }
    
    for item in diff:
        if item.startswith('- '):
            changes['removed'].append(item[2:])
        elif item.startswith('+ '):
            changes['added'].append(item[2:])
        elif item.startswith('  '):
            changes['unchanged'].append(item[2:])
    
    return changes

def analyze_verb_changes(removed, added):
    """Identify verb replacements."""
    verb_changes = []
    
    # Simple heuristic: look for action verbs
    action_verbs = ['leads', 'promotes', 'works', 'focuses', 'creates', 'establishes', 
                    'demonstrates', 'shows', 'brings', 'combines']
    
    removed_verbs = [w for w in removed if w in action_verbs]
    added_verbs = [w for w in added if w in action_verbs]
    
    if removed_verbs and added_verbs:
        for rv in removed_verbs:
            for av in added_verbs:
                verb_changes.append(f"{rv} → {av}")
    
    return verb_changes

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 analyze_bio_feedback.py <AI.md> <JS.md>")
        sys.exit(1)
    
    ai_file = Path(sys.argv[1])
    js_file = Path(sys.argv[2])
    
    if not ai_file.exists():
        print(f"Error: {ai_file} not found")
        sys.exit(1)
    
    if not js_file.exists():
        print(f"Error: {js_file} not found")
        sys.exit(1)
    
    print("=" * 80)
    print("BIO FEEDBACK ANALYSIS")
    print("=" * 80)
    print()
    print(f"AI version: {ai_file.name}")
    print(f"Human edit: {js_file.name}")
    print()
    
    with open(ai_file) as f:
        ai_content = f.read()
    with open(js_file) as f:
        js_content = f.read()
    
    ai_bios = extract_bios(ai_content)
    js_bios = extract_bios(js_content)
    
    print(f"Found {len(ai_bios)} bios in AI version")
    print(f"Found {len(js_bios)} bios in human version")
    print()
    
    all_verb_changes = []
    all_patterns = []
    
    for name in ai_bios:
        if name not in js_bios:
            print(f"⚠️  {name}: Not found in human version (deleted?)")
            print()
            continue
        
        ai_bio = extract_bio_text(ai_bios[name])
        js_bio = extract_bio_text(js_bios[name])
        
        if ai_bio == js_bio:
            print(f"✅ {name}: No changes")
            print()
            continue
        
        print(f"📝 {name}: Changes detected")
        print("-" * 80)
        
        changes = compare_texts(ai_bio, js_bio)
        
        if changes['removed']:
            print(f"\n**Removed words ({len(changes['removed'])}):**")
            print(" ".join(changes['removed'][:20]))
            if len(changes['removed']) > 20:
                print(f"... and {len(changes['removed']) - 20} more")
        
        if changes['added']:
            print(f"\n**Added words ({len(changes['added'])}):**")
            print(" ".join(changes['added'][:20]))
            if len(changes['added']) > 20:
                print(f"... and {len(changes['added']) - 20} more")
        
        # Analyze verb changes
        verb_changes = analyze_verb_changes(changes['removed'], changes['added'])
        if verb_changes:
            all_verb_changes.extend(verb_changes)
            print(f"\n**Verb changes:**")
            for vc in verb_changes:
                print(f"  - {vc}")
        
        # Check for bracketing
        if '[' in js_bio and '[' not in ai_bio:
            print(f"\n**Bracketing detected:** Section marked for review/removal")
            all_patterns.append(f"{name}: Text bracketed")
        
        print()
    
    # Summary
    print("=" * 80)
    print("PATTERN SUMMARY")
    print("=" * 80)
    print()
    
    if all_verb_changes:
        print("**Verb Changes Across All Bios:**")
        for vc in set(all_verb_changes):
            count = all_verb_changes.count(vc)
            print(f"  - {vc} ({count}x)")
        print()
    
    if all_patterns:
        print("**Other Patterns:**")
        for p in all_patterns:
            print(f"  - {p}")
        print()
    
    print("**Next Steps:**")
    print("1. Discuss patterns with human")
    print("2. Update CONTEXT_RECOVERY.md with learned rules")
    print("3. Apply to next batch")
    print()

if __name__ == "__main__":
    main()
