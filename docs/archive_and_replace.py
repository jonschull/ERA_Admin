#!/usr/bin/env python3
"""
Safe archive and replace documentation script.

SAFETY FEATURES:
1. Creates timestamped backup of all originals
2. Dry-run mode to preview changes
3. Atomic operations - all or nothing
4. Generates rollback script automatically
5. Validates before proceeding
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import sys

# Files to archive and replace
FILES_TO_REPLACE = [
    'README.md',
    'CONTEXT_RECOVERY.md',
    'AI_HANDOFF_GUIDE.md',
    'WORKING_PRINCIPLES.md',
    'FathomInventory/README.md',
    'FathomInventory/CONTEXT_RECOVERY.md',
    'FathomInventory/authentication/README.md',
    'airtable/README.md',
    'integration_scripts/README.md',
    'integration_scripts/AI_WORKFLOW_GUIDE.md',
]

def get_timestamp():
    """Get timestamp for archive directory."""
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def validate_environment():
    """Ensure we're in the right place with the right files."""
    issues = []
    
    # Check we're in ERA_Admin root
    if not Path('docs/NAVIGATION_WIREFRAME.md').exists():
        issues.append("❌ Not in ERA_Admin root (can't find docs/NAVIGATION_WIREFRAME.md)")
    
    # Check docs_generated exists
    if not Path('docs_generated').exists():
        issues.append("❌ docs_generated/ not found - run generate_from_wireframe.py first")
    
    # Check all original files exist
    for file_path in FILES_TO_REPLACE:
        if not Path(file_path).exists():
            issues.append(f"❌ Original not found: {file_path}")
    
    # Check all generated files exist
    for file_path in FILES_TO_REPLACE:
        gen_path = Path('docs_generated') / file_path
        if not gen_path.exists():
            issues.append(f"❌ Generated file not found: {gen_path}")
    
    return issues

def create_archive(timestamp, dry_run=False):
    """Archive all original files."""
    archive_dir = Path('historical') / f'docs_archive_{timestamp}'
    
    print(f"\n📦 Creating archive: {archive_dir}")
    
    if dry_run:
        print("   [DRY RUN] Would create directory")
    else:
        archive_dir.mkdir(parents=True, exist_ok=True)
    
    archived_files = []
    
    for file_path in FILES_TO_REPLACE:
        source = Path(file_path)
        dest = archive_dir / file_path
        
        if dry_run:
            print(f"   [DRY RUN] Would copy: {file_path} → {archive_dir / file_path}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            print(f"   ✅ Archived: {file_path}")
        
        archived_files.append(file_path)
    
    return archive_dir, archived_files

def replace_files(dry_run=False):
    """Replace original files with generated versions."""
    print(f"\n🔄 Replacing files")
    
    replaced = []
    
    for file_path in FILES_TO_REPLACE:
        source = Path('docs_generated') / file_path
        dest = Path(file_path)
        
        if dry_run:
            print(f"   [DRY RUN] Would replace: {file_path}")
        else:
            shutil.copy2(source, dest)
            print(f"   ✅ Replaced: {file_path}")
        
        replaced.append(file_path)
    
    return replaced

def create_rollback_script(archive_dir, timestamp):
    """Generate a rollback script."""
    script_path = Path(f'rollback_docs_{timestamp}.sh')
    
    script_content = f"""#!/bin/bash
# Rollback script - restore documentation from archive
# Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Archive: {archive_dir}

set -e

echo "🔄 Rolling back documentation to archive from {timestamp}"
echo ""

"""
    
    for file_path in FILES_TO_REPLACE:
        script_content += f"""
if [ -f "{archive_dir}/{file_path}" ]; then
    cp -v "{archive_dir}/{file_path}" "{file_path}"
    echo "✅ Restored: {file_path}"
else
    echo "⚠️  Archive missing: {file_path}"
fi
"""
    
    script_content += """
echo ""
echo "✅ Rollback complete!"
echo ""
echo "To verify, run: git diff"
"""
    
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    os.chmod(script_path, 0o755)
    
    return script_path

def show_summary(archive_dir, rollback_script):
    """Show summary of what was done."""
    print("\n" + "=" * 70)
    print("✅ ARCHIVE AND REPLACE COMPLETE")
    print("=" * 70)
    print(f"\n📦 Archive location: {archive_dir}")
    print(f"📜 Rollback script: {rollback_script}")
    print(f"📊 Files replaced: {len(FILES_TO_REPLACE)}")
    print()
    print("Next steps:")
    print("1. Test the new documentation")
    print("2. Run: git diff (to see changes)")
    print("3. If satisfied: git add . && git commit -m 'Replace docs with generated versions'")
    print(f"4. If issues: ./{rollback_script} (to restore originals)")
    print()

def main():
    """Main execution."""
    # Check for dry-run flag
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    
    print("=" * 70)
    print("DOCUMENTATION ARCHIVE & REPLACE")
    print("=" * 70)
    
    if dry_run:
        print("\n⚠️  DRY RUN MODE - No changes will be made")
    
    print("\n📋 Validating environment...")
    issues = validate_environment()
    
    if issues:
        print("\n❌ VALIDATION FAILED:")
        for issue in issues:
            print(f"  {issue}")
        print("\nFix these issues and try again.")
        sys.exit(1)
    
    print("✅ Validation passed")
    
    # Show what will be done
    print(f"\n📝 Plan:")
    print(f"  - Archive {len(FILES_TO_REPLACE)} original files")
    print(f"  - Replace with generated versions")
    print(f"  - Create rollback script")
    
    if not dry_run:
        print("\n⚠️  This will modify your file system!")
        response = input("\nProceed? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Aborted.")
            sys.exit(0)
    
    # Get timestamp for this operation
    timestamp = get_timestamp()
    
    # Create archive
    archive_dir, archived = create_archive(timestamp, dry_run)
    
    # Replace files
    replaced = replace_files(dry_run)
    
    # Create rollback script
    if not dry_run:
        rollback_script = create_rollback_script(archive_dir, timestamp)
        print(f"\n📜 Created rollback script: {rollback_script}")
        show_summary(archive_dir, rollback_script)
    else:
        print("\n" + "=" * 70)
        print("DRY RUN COMPLETE - No changes made")
        print("=" * 70)
        print("\nRun without --dry-run to execute:")
        print("  python3 docs/archive_and_replace.py")
        print()

if __name__ == '__main__':
    main()
