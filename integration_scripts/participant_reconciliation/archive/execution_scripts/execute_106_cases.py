#!/usr/bin/env python3
"""
Execute 106 remaining categorizations with comprehensive testing and verification.
Adapted from execute_206_categorizations.py

Usage:
    python3 execute_106_cases.py --dry-run  # Test mode (safe)
    python3 execute_106_cases.py --execute  # Actual execution
"""

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime
import shutil

DB_PATH = Path('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')
CATEGORIZATIONS_FILE = Path('batch_106_approved_cases.json')

class DatabaseExecutor:
    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.conn = None
        self.backup_path = None
        self.execution_log = []
        
    def connect(self):
        """Connect to database."""
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
    
    def create_backup(self):
        """Create database backup before execution."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = DB_PATH.parent / f"fathom_emails_BACKUP_106_{timestamp}.db"
        shutil.copy2(DB_PATH, self.backup_path)
        print(f"✅ Backup created: {self.backup_path}")
        return self.backup_path
    
    def verify_variant_exists(self, variant):
        """Check if variant exists in database."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT name, source_call_url FROM participants WHERE name = ?",
            (variant,)
        )
        result = cursor.fetchone()
        return dict(result) if result else None
    
    def merge_participants(self, variant, target):
        """Merge variant into target, preserving data."""
        cursor = self.conn.cursor()
        
        # Get both records
        cursor.execute(
            "SELECT source_call_url FROM participants WHERE name = ?",
            (variant,)
        )
        variant_row = cursor.fetchone()
        
        cursor.execute(
            "SELECT source_call_url FROM participants WHERE name = ?",
            (target,)
        )
        target_row = cursor.fetchone()
        
        if not variant_row:
            return f"ERROR: Variant '{variant}' not found"
        
        # Combine URLs
        variant_urls = set(variant_row[0].split(',')) if variant_row[0] else set()
        target_urls = set(target_row[0].split(',')) if target_row and target_row[0] else set()
        combined_urls = ','.join(sorted(variant_urls | target_urls))
        
        if self.dry_run:
            return f"DRY-RUN: Would merge {len(variant_urls)} URLs from '{variant}' into '{target}'"
        
        # Execute merge
        if target_row:
            # Update existing target
            cursor.execute(
                "UPDATE participants SET source_call_url = ? WHERE name = ?",
                (combined_urls, target)
            )
        else:
            # Rename variant to target
            cursor.execute(
                "UPDATE participants SET name = ? WHERE name = ?",
                (target, variant)
            )
        
        # Delete variant
        cursor.execute("DELETE FROM participants WHERE name = ?", (variant,))
        self.conn.commit()
        
        return f"✓ Merged {len(variant_urls)} URLs from '{variant}' → '{target}'"
    
    def mark_validated(self, variant):
        """Mark participant as validated in Airtable."""
        if self.dry_run:
            return f"DRY-RUN: Would set validated_by_airtable=1 for '{variant}'"
        
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE participants SET validated_by_airtable = 1 WHERE name = ?",
            (variant,)
        )
        self.conn.commit()
        
        return f"✓ Marked '{variant}' as validated"
    
    def add_to_airtable_marker(self, variant):
        """Mark participant for Airtable addition."""
        if self.dry_run:
            return f"DRY-RUN: Would mark '{variant}' for Airtable addition"
        
        # Mark as validated since it will be added to Airtable
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE participants SET validated_by_airtable = 1 WHERE name = ?",
            (variant,)
        )
        self.conn.commit()
        
        return f"✓ Marked '{variant}' for Airtable addition"
    
    def remove_participant(self, variant):
        """Remove participant from database."""
        cursor = self.conn.cursor()
        
        # Get data that will be lost
        cursor.execute(
            "SELECT source_call_url FROM participants WHERE name = ?",
            (variant,)
        )
        row = cursor.fetchone()
        
        if not row:
            return f"WARNING: '{variant}' not found"
        
        url_count = len([u for u in row[0].split(',') if u.strip()]) if row[0] else 0
        
        if self.dry_run:
            return f"DRY-RUN: Would remove '{variant}' (losing {url_count} TH attendances)"
        
        cursor.execute("DELETE FROM participants WHERE name = ?", (variant,))
        self.conn.commit()
        
        return f"✓ Removed '{variant}' (lost {url_count} TH attendances)"
    
    def execute_case(self, case):
        """Execute a single categorization case."""
        variant = case['variant']
        target = case.get('target')
        action = case['action']
        
        # Verify variant exists
        variant_data = self.verify_variant_exists(variant)
        if not variant_data:
            msg = f"SKIP - '{variant}' not in database"
            self.execution_log.append({'variant': variant, 'status': 'SKIP', 'message': msg})
            return msg
        
        # Execute based on action
        try:
            if action == 'MERGE':
                result = self.merge_participants(variant, target)
            elif action == 'MARK_VALIDATED':
                result = self.mark_validated(variant)
            elif action == 'ADD_TO_AIRTABLE':
                result = self.add_to_airtable_marker(variant)
            elif action == 'REMOVE':
                result = self.remove_participant(variant)
            else:
                result = f"UNKNOWN ACTION: {action}"
            
            self.execution_log.append({
                'variant': variant,
                'target': target,
                'action': action,
                'status': 'SUCCESS' if not result.startswith('ERROR') else 'ERROR',
                'message': result
            })
            
            return result
            
        except Exception as e:
            msg = f"ERROR - {str(e)}"
            self.execution_log.append({'variant': variant, 'status': 'ERROR', 'message': msg})
            return msg
    
    def pre_execution_report(self, categorizations):
        """Generate report of what will happen."""
        print("\n" + "="*80)
        print("PRE-EXECUTION REPORT")
        print("="*80)
        
        action_counts = {}
        issues = []
        
        for case in categorizations:
            variant = case['variant']
            target = case.get('target')
            action = case['action']
            
            # Count actions
            action_counts[action] = action_counts.get(action, 0) + 1
            
            # Check for issues
            variant_exists = self.verify_variant_exists(variant)
            if not variant_exists:
                issues.append(f"Variant '{variant}' NOT FOUND in database")
        
        print(f"\nTotal cases: {len(categorizations)}")
        print("\nActions breakdown:")
        for action, count in sorted(action_counts.items()):
            print(f"  {action}: {count}")
        
        if issues:
            print(f"\n⚠️  Issues found: {len(issues)}")
            for issue in issues[:10]:
                print(f"  - {issue}")
            if len(issues) > 10:
                print(f"  ... and {len(issues) - 10} more")
        else:
            print("\n✅ No issues found")
        
        print("="*80)
    
    def post_execution_verification(self, categorizations):
        """Verify execution completed correctly."""
        print("\n" + "="*80)
        print("POST-EXECUTION VERIFICATION")
        print("="*80)
        
        success_count = 0
        skip_count = 0
        error_count = 0
        
        for log in self.execution_log:
            if log['status'] == 'SUCCESS':
                success_count += 1
            elif log['status'] == 'SKIP':
                skip_count += 1
            else:
                error_count += 1
        
        print(f"\nTotal cases processed: {len(self.execution_log)}")
        print(f"  ✓ Success: {success_count}")
        print(f"  ⊘ Skipped: {skip_count}")
        print(f"  ✗ Errors: {error_count}")
        
        # Check database state
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT name) as total,
                SUM(CASE WHEN validated_by_airtable = 1 THEN 1 ELSE 0 END) as validated
            FROM (SELECT DISTINCT name, validated_by_airtable FROM participants)
        """)
        total, validated = cursor.fetchone()
        unvalidated = total - validated
        
        print(f"\nDatabase state:")
        print(f"  Total participants: {total}")
        print(f"  Validated: {validated}")
        print(f"  Unvalidated: {unvalidated}")
        
        print("="*80)
        
        # Save log
        log_file = Path(f"execution_log_106_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(log_file, 'w') as f:
            json.dump(self.execution_log, f, indent=2)
        print(f"\nExecution log saved: {log_file}")

def main():
    # Parse arguments
    dry_run = '--execute' not in sys.argv
    
    if dry_run:
        print("🔍 DRY-RUN MODE (safe - no changes will be made)")
        print("To execute for real, run: python3 execute_106_cases.py --execute\n")
    else:
        print("⚠️  EXECUTION MODE - Changes WILL be made to database!")
        response = input("Type 'YES' to confirm: ")
        if response != 'YES':
            print("Aborted.")
            return
    
    # Load categorizations
    with open(CATEGORIZATIONS_FILE, 'r') as f:
        categorizations = json.load(f)
    
    print(f"Loaded {len(categorizations)} categorizations")
    
    # Initialize executor
    executor = DatabaseExecutor(dry_run=dry_run)
    executor.connect()
    
    try:
        # Pre-execution report
        executor.pre_execution_report(categorizations)
        
        if not dry_run:
            # Create backup
            backup = executor.create_backup()
            print(f"\n💾 Backup created: {backup}")
            print(f"To restore: cp {backup} {DB_PATH}\n")
        
        # Execute cases
        print(f"\nProcessing {len(categorizations)} cases...")
        for i, case in enumerate(categorizations, 1):
            result = executor.execute_case(case)
            if i % 25 == 0 or i == len(categorizations):
                print(f"  Progress: {i}/{len(categorizations)}")
        
        # Post-execution verification
        executor.post_execution_verification(categorizations)
        
    finally:
        executor.close()
    
    if dry_run:
        print("\n✅ Dry-run complete. Review output above.")
        print("To execute for real: python3 execute_106_cases.py --execute")
    else:
        print("\n✅ Execution complete!")
        print(f"Backup available at: {executor.backup_path}")

if __name__ == "__main__":
    main()
