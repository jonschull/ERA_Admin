#!/usr/bin/env python3
"""
Test that all scripts/folders are referenced in documentation.

Finds all .py, .sh files and directories in components,
checks if they're mentioned in the generated docs.
"""

import os
from pathlib import Path
from typing import Set, Dict, List

def find_scripts_and_folders(component_dir: str) -> Dict[str, List[str]]:
    """Find all scripts and key folders in a component."""
    base = Path(component_dir)
    
    if not base.exists():
        return {}
    
    results = {
        'scripts': [],
        'folders': [],
        'config': []
    }
    
    # Find Python scripts
    for py_file in base.rglob('*.py'):
        # Skip __pycache__, venv, etc.
        if '__pycache__' in py_file.parts or 'venv' in py_file.parts:
            continue
        rel_path = py_file.relative_to(base)
        results['scripts'].append(str(rel_path))
    
    # Find shell scripts
    for sh_file in base.rglob('*.sh'):
        rel_path = sh_file.relative_to(base)
        results['scripts'].append(str(rel_path))
    
    # Find key directories (one level deep)
    for item in base.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            # Skip common non-relevant dirs
            if item.name in ['__pycache__', 'venv', '.git', 'node_modules']:
                continue
            results['folders'].append(item.name)
    
    # Find config files
    for pattern in ['*.json', '*.yaml', '*.yml', '*.ini', '*.toml', 'requirements.txt']:
        for config_file in base.glob(pattern):
            if config_file.is_file():
                results['config'].append(config_file.name)
    
    return results


def check_references_in_docs(item: str, docs_dir: str) -> List[str]:
    """Check which doc files mention this item."""
    found_in = []
    docs_path = Path(docs_dir)
    
    if not docs_path.exists():
        return found_in
    
    # Search all markdown files
    for md_file in docs_path.rglob('*.md'):
        try:
            content = md_file.read_text()
            # Check for mentions (filename, path, or backticked)
            item_name = Path(item).name
            if item in content or item_name in content or f"`{item}`" in content or f"`{item_name}`" in content:
                found_in.append(str(md_file.relative_to(docs_path)))
        except Exception:
            pass
    
    return found_in


def main():
    """Main execution."""
    print("=" * 70)
    print("SCRIPT/FOLDER REFERENCE TEST")
    print("=" * 70)
    print()
    
    components = {
        'FathomInventory': '../FathomInventory',
        'airtable': '../airtable',
        'integration_scripts': '../integration_scripts'
    }
    
    docs_dir = '../docs_generated'
    
    total_items = 0
    total_documented = 0
    total_undocumented = 0
    
    all_undocumented = []
    
    for component_name, component_path in components.items():
        print(f"\n{'=' * 70}")
        print(f"COMPONENT: {component_name}")
        print('=' * 70)
        
        items = find_scripts_and_folders(component_path)
        
        # Check scripts
        if items['scripts']:
            print(f"\n📜 SCRIPTS ({len(items['scripts'])} found):")
            for script in sorted(items['scripts']):
                total_items += 1
                refs = check_references_in_docs(script, docs_dir)
                if refs:
                    total_documented += 1
                    print(f"  ✅ {script}")
                    print(f"     Referenced in: {', '.join(refs)}")
                else:
                    total_undocumented += 1
                    print(f"  ❌ {script} - NOT DOCUMENTED")
                    all_undocumented.append(f"{component_name}/{script}")
        
        # Check folders
        if items['folders']:
            print(f"\n📁 DIRECTORIES ({len(items['folders'])} found):")
            for folder in sorted(items['folders']):
                total_items += 1
                refs = check_references_in_docs(folder, docs_dir)
                if refs:
                    total_documented += 1
                    print(f"  ✅ {folder}/")
                    print(f"     Referenced in: {', '.join(refs)}")
                else:
                    total_undocumented += 1
                    print(f"  ❌ {folder}/ - NOT DOCUMENTED")
                    all_undocumented.append(f"{component_name}/{folder}/")
        
        # Check config files
        if items['config']:
            print(f"\n⚙️  CONFIG FILES ({len(items['config'])} found):")
            for config in sorted(items['config']):
                total_items += 1
                refs = check_references_in_docs(config, docs_dir)
                if refs:
                    total_documented += 1
                    print(f"  ✅ {config}")
                    print(f"     Referenced in: {', '.join(refs)}")
                else:
                    total_undocumented += 1
                    print(f"  ⚠️  {config} - NOT DOCUMENTED")
                    all_undocumented.append(f"{component_name}/{config}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total items checked: {total_items}")
    print(f"Documented: {total_documented} ({total_documented/total_items*100:.1f}%)")
    print(f"Not documented: {total_undocumented} ({total_undocumented/total_items*100:.1f}%)")
    print()
    
    if all_undocumented:
        print("❌ UNDOCUMENTED ITEMS:")
        for item in all_undocumented[:20]:  # Show first 20
            print(f"  - {item}")
        if len(all_undocumented) > 20:
            print(f"  ... and {len(all_undocumented) - 20} more")
        print()
        print("⚠️  Consider adding these to documentation")
    else:
        print("🎉 All scripts and folders are documented!")
    
    print()


if __name__ == '__main__':
    main()
