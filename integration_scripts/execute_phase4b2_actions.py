#!/usr/bin/env python3
"""
Execute Phase 4B-2 actions from CSV decisions + probe results.

Actions:
- MERGE: Update Fathom email to match Airtable person
  * UNIQUE constraint aware: Deletes duplicate variant if target already exists
  * Otherwise updates name to target
- DROP: Delete from Fathom database  
- ADD: Add to Airtable automatically

IMPORTANT: Database has UNIQUE constraint on participants.name (added PR #17)
This affects merge logic - see execute_merge() function for details.

See EXECUTION_WORKFLOW.md for full documentation.
"""

import sqlite3
import csv
import re
from pathlib import Path
from datetime import datetime
import shutil
import sys

# Import add_to_airtable module
sys.path.insert(0, str(Path(__file__).parent))
from add_to_airtable import add_people_to_airtable, update_fathom_validated

# Paths
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent / "FathomInventory" / "fathom_emails.db"
BACKUP_DIR = SCRIPT_DIR.parent / "FathomInventory" / "backups"
AIRTABLE_CSV = SCRIPT_DIR.parent / "airtable" / "people_export.csv"

# Load Airtable people for matching
airtable_people = {}

def load_airtable():
    """Load Airtable people into memory."""
    print("\n📖 Loading Airtable people...")
    with open(AIRTABLE_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            if name:
                airtable_people[name] = {
                    'name': name,
                    'email': row.get('Email', '').strip(),
                    'member': 'True' in row.get('Member', ''),
                    'donor': 'True' in row.get('Donor', '')
                }
    print(f"   ✅ Loaded {len(airtable_people)} people")


def backup_database():
    """Create backup before making changes."""
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    backup_path = BACKUP_DIR / f"fathom_emails.backup_{timestamp}.db"
    shutil.copy2(DB_PATH, backup_path)
    print(f"\n💾 Backup created: {backup_path.name}")
    return backup_path


def parse_merge_target(comment):
    """Extract merge target name from comment and map to actual Airtable names."""
    # Patterns: "merge with: Name" or "Merge with Name"
    patterns = [
        r'merge with:?\s+([^,\n]+)',
        r'Merge with:?\s+([^,\n]+)'
    ]
    
    target = None
    for pattern in patterns:
        match = re.search(pattern, comment, re.IGNORECASE)
        if match:
            target = match.group(1).strip()
            break
    
    if not target:
        return None
    
    # Map comment targets to actual Airtable names
    target_mapping = {
        'Frederic Jennings': 'Fred Jennings',
        'Charlie Shore': 'Charles Shore',
        'aniqa Locations: Bangladesh': 'Aniqa Moinuddin',
        'Caroline Petruzzi': 'Caroline Petruzzi',
        'Moses Ujunjo': 'Moses Ojunju',  # Fix spelling
    }
    
    return target_mapping.get(target, target)


def execute_merge(conn, fathom_name, target_name):
    """Merge Fathom participant with Airtable person."""
    
    # Find target in Airtable
    if target_name not in airtable_people:
        print(f"   ⚠️  Target '{target_name}' not in Airtable - skipping")
        return 'skipped_target'  # Special return value
    
    target = airtable_people[target_name]
    cursor = conn.cursor()
    
    # Check if target_name already exists in database (UNIQUE constraint)
    cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (target_name,))
    target_exists = cursor.fetchone()[0] > 0
    
    if target_exists and fathom_name != target_name:
        # Target already exists - just delete the duplicate variant
        cursor.execute("DELETE FROM participants WHERE name = ?", (fathom_name,))
        if cursor.rowcount > 0:
            print(f"   ✅ Deleted duplicate '{fathom_name}' (target '{target_name}' already exists)")
            return True
        else:
            print(f"   ⚠️  No records found for '{fathom_name}'")
            return False
    else:
        # Target doesn't exist or same name - safe to UPDATE
        cursor.execute("""
            UPDATE participants
            SET name = ?,
                email = ?,
                era_member = ?,
                is_donor = ?,
                validated_by_airtable = 1,
                airtable_id = ?
            WHERE name = ?
        """, (
            target['name'],
            target['email'] if target['email'] else None,
            1 if target['member'] else 0,
            1 if target['donor'] else 0,
            target.get('airtable_id'),  # Add airtable_id if available
            fathom_name
        ))
        
        if cursor.rowcount > 0:
            print(f"   ✅ Merged '{fathom_name}' → '{target_name}' ({cursor.rowcount} records)")
            return True
        else:
            print(f"   ⚠️  No records found for '{fathom_name}'")
            return False


def execute_drop(conn, fathom_name):
    """Delete participant from Fathom database."""
    cursor = conn.cursor()
    
    # Delete from participants table (match by name)
    cursor.execute("DELETE FROM participants WHERE name = ?", (fathom_name,))
    deleted = cursor.rowcount
    
    if deleted > 0:
        print(f"   ✅ Dropped '{fathom_name}' ({deleted} records)")
        return True
    else:
        print(f"   ⚠️  No records found for '{fathom_name}'")
        return False


def process_csv_decisions(csv_path):
    """Process all actions from CSV."""
    
    print("\n" + "=" * 80)
    print("📋 PROCESSING CSV DECISIONS")
    print("=" * 80)
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Categorize actions
    merges = []
    drops = []
    adds = []
    needs_discussion = []
    
    for row in rows:
        fathom_name = row['Fathom_Name']
        # Strip emoji badges added by HTML generation (🔁 markers)
        fathom_name = fathom_name.split('🔁')[0].strip()
        comment = row.get('Comments', '').strip()
        process_this = row.get('ProcessThis', '').upper() == 'YES'
        probe = row.get('Probe', '').upper() == 'YES'
        
        # If there's a comment, treat as probe checked (user wants attention)
        if comment:
            probe = True
        
        # Auto-process standard format decisions even if ProcessThis=NO
        # User may forget to check box but decision is clear
        if comment and not process_this:
            is_standard = (comment.startswith('merge with:') or 
                          comment.startswith('drop') or 
                          comment.startswith('ignore') or
                          comment.startswith('add to airtable'))
            if is_standard:
                process_this = True
                # Silent auto-enable for standard formats
        
        # Check if comment is custom (not auto-generated)
        is_custom_comment = (comment and 
                            not comment.startswith('merge with:') and
                            not comment.startswith('add to airtable') and
                            not comment.startswith('drop') and
                            not comment.startswith('ignore'))
        
        # Flag custom comments for discussion
        if is_custom_comment and (process_this or probe):
            needs_discussion.append((fathom_name, comment, process_this, probe))
        
        if not process_this:
            continue
        
        # Parse action from comment
        if 'drop' in comment.lower():
            drops.append((fathom_name, comment))
        elif 'merge' in comment.lower():
            target = parse_merge_target(comment)
            if target:
                merges.append((fathom_name, target, comment))
        elif 'add to airtable' in comment.lower():
            adds.append((fathom_name, comment))
    
    print(f"\n📊 Actions to execute:")
    print(f"   🔀 Merges: {len(merges)}")
    print(f"   🗑️  Drops: {len(drops)}")
    print(f"   ➕ Adds: {len(adds)}")
    
    if needs_discussion:
        print(f"\n⚠️  CUSTOM COMMENTS NEED DISCUSSION:")
        print(f"   💬 {len(needs_discussion)} items with non-standard comments")
    
    return merges, drops, adds, needs_discussion


def process_probe_results():
    """Add probe recommendations to processing queue."""
    print("\n" + "=" * 80)
    print("🔍 ADDING PROBE RESULTS")
    print("=" * 80)
    
    probe_merges = [
        ("MOSES, GFCCA", "Moses Ojunju"),
        ("MOSES, GFCCA (2)", "Moses Ojunju"),
        ("MOSES, GFCCA (5)", "Moses Ojunju"),
    ]
    
    probe_drops = [
        ("Duane Norris", "Deceased per Gmail"),
    ]
    
    print(f"\n📊 Probe actions:")
    print(f"   🔀 Merges: {len(probe_merges)}")
    print(f"   🗑️  Drops: {len(probe_drops)}")
    
    return probe_merges, probe_drops


def main():
    """Main execution."""
    print()
    print("=" * 80)
    print("PHASE 4B-2: EXECUTE ACTIONS")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load Airtable
    load_airtable()
    
    # Find CSV
    csv_files = list(SCRIPT_DIR.glob("phase4b2_approvals_*.csv"))
    if not csv_files:
        print("\n❌ No CSV file found!")
        return
    
    csv_path = max(csv_files, key=lambda p: p.stat().st_mtime)
    print(f"\n📄 Using CSV: {csv_path.name}")
    
    # Parse actions
    csv_merges, csv_drops, csv_adds, needs_discussion = process_csv_decisions(csv_path)
    probe_merges, probe_drops = process_probe_results()
    
    # Show custom comments that need discussion
    if needs_discussion:
        print("\n" + "=" * 80)
        print("💬 CUSTOM COMMENTS - NEED DISCUSSION")
        print("=" * 80)
        for name, comment, process_this, probe in needs_discussion:
            print(f"\n• {name}")
            print(f"  Comment: {comment}")
            print(f"  ProcessThis: {'YES' if process_this else 'NO'}")
            print(f"  Probe: {'YES' if probe else 'NO'}")
            print(f"  ⚠️  Please discuss this case with user before processing")
        
        print("\n" + "=" * 80)
        print("⏸️  PAUSED - Custom comments detected")
        print("=" * 80)
        print("\nPlease review the custom comments above and:")
        print("1. Clarify the intended action")
        print("2. Either handle manually or update comment to standard format")
        print("3. Re-run this script after resolving")
        return  # Exit - don't process until discussed
    
    # Combine
    all_merges = csv_merges + [(name, target) for name, target in probe_merges]
    all_drops = csv_drops + probe_drops
    
    total_actions = len(all_merges) + len(all_drops) + len(csv_adds)
    
    print("\n" + "=" * 80)
    print(f"📊 TOTAL ACTIONS: {total_actions}")
    print("=" * 80)
    print(f"   🔀 Merges: {len(all_merges)}")
    print(f"   🗑️  Drops: {len(all_drops)}")
    print(f"   ➕ Adds to Airtable: {len(csv_adds)} (manual - will report)")
    
    # Backup
    backup_database()
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    conn.execute("BEGIN TRANSACTION")
    
    try:
        # Execute merges
        if all_merges:
            print("\n" + "=" * 80)
            print("🔀 EXECUTING MERGES")
            print("=" * 80)
            merged_count = 0
            skipped_targets = []  # Track targets not in Airtable
            for item in all_merges:
                if len(item) == 2:
                    fathom_name, target = item
                else:
                    fathom_name, target, _ = item
                result = execute_merge(conn, fathom_name, target)
                if result == True:
                    merged_count += 1
                elif result == 'skipped_target':
                    skipped_targets.append(target)
            print(f"\n✅ Merged: {merged_count}/{len(all_merges)}")
        
        # Execute drops
        if all_drops:
            print("\n" + "=" * 80)
            print("🗑️  EXECUTING DROPS")
            print("=" * 80)
            drop_count = 0
            for item in all_drops:
                if len(item) == 2:
                    fathom_name, reason = item
                    print(f"\n   Reason: {reason}")
                else:
                    fathom_name = item
                if execute_drop(conn, fathom_name):
                    drop_count += 1
            print(f"\n✅ Dropped: {drop_count}/{len(all_drops)}")
        
        # Commit database changes first
        conn.commit()
        print("\n" + "=" * 80)
        print("✅ DATABASE CHANGES COMMITTED")
        print("=" * 80)
        
        # Now add people to Airtable (after DB commit)
        if csv_adds:
            # Parse adds into format for add_to_airtable
            people_to_add = []
            for fathom_name, comment in csv_adds:
                # Determine if member based on comment
                is_member = 'member' in comment.lower()
                people_to_add.append({
                    'name': fathom_name,
                    'is_member': is_member,
                    'notes': comment
                })
            
            # Add to Airtable
            added, skipped = add_people_to_airtable(people_to_add, conn)
            
            # Update Fathom database to mark as validated
            if added:
                update_fathom_validated(added, conn)
        
        # Auto-add skipped merge targets to prevent them from coming back
        if skipped_targets:
            print("\n" + "=" * 80)
            print("➕ AUTO-ADDING SKIPPED MERGE TARGETS")
            print("=" * 80)
            print(f"\n📝 Found {len(skipped_targets)} targets not in Airtable")
            print("   Checking for typos/near-duplicates before adding...\n")
            
            # Deduplicate targets
            unique_targets = list(set(skipped_targets))
            targets_to_add = []
            near_duplicates = []
            
            for target in unique_targets:
                # Skip obviously bad names
                if len(target) < 3 or target in ['Ana', 'Ed', 'Huling']:
                    print(f"   ⏭️  Skipping incomplete name: '{target}'")
                    continue
                
                # Check for near-duplicates (might be typos)
                from fuzzywuzzy import fuzz
                best_match = None
                best_score = 0
                
                for existing_name in airtable_people.keys():
                    score = fuzz.ratio(target.lower(), existing_name.lower())
                    if score > best_score:
                        best_score = score
                        best_match = existing_name
                
                # If >85% similar, probably a typo - don't auto-add
                if best_score > 85:
                    print(f"   ⚠️  '{target}' looks like typo of '{best_match}' ({best_score}%) - skipping")
                    near_duplicates.append((target, best_match, best_score))
                    continue
                
                targets_to_add.append({
                    'name': target,
                    'is_member': True,  # Assume member if they were merge targets
                    'notes': 'Auto-added from skipped merge target'
                })
            
            if targets_to_add:
                try:
                    added, skipped = add_people_to_airtable(targets_to_add, conn)
                    if added:
                        update_fathom_validated(added, conn)
                        print(f"\n✅ Auto-added {len(added)} people to prevent recurrence")
                except Exception as e:
                    print(f"\n⚠️  Auto-add failed: {e}")
                    print("   These will need manual addition")
            
            if near_duplicates:
                print(f"\n⚠️  NEAR-DUPLICATES DETECTED (not auto-added):")
                for target, match, score in near_duplicates:
                    print(f"   • '{target}' → '{match}' ({score}%)")
                print("\n   Please review these manually - may be typos!")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ ERROR: {e}")
        print("   Rolling back all changes...")
        import traceback
        traceback.print_exc()
        return
    finally:
        conn.close()
    
    # Final stats
    print("\n" + "=" * 80)
    print("📊 FINAL DATABASE STATUS")
    print("=" * 80)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM participants")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM participants WHERE validated_by_airtable = 1")
    enriched = cursor.fetchone()[0]
    
    remaining = total - enriched
    
    print(f"\n   Total participants: {total}")
    print(f"   Enriched: {enriched}")
    print(f"   Remaining: {remaining}")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ PHASE 4B-2 ROUND COMPLETE")
    print("=" * 80)
    print(f"\n   Processed: {total_actions} items")
    print(f"   Remaining to review: {remaining}")
    print()


if __name__ == "__main__":
    main()
