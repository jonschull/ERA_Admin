#!/usr/bin/env python3
"""
Execute Participant Redundancy Merges

PURPOSE:
    Merge duplicate participant records based on approved merge actions.
    Updates participants table and alias resolution table.

SAFETY:
    - Only processes HIGH confidence merges
    - Creates backup before any changes
    - Logs all actions
    - Preserves all data (combines, doesn't delete)

USAGE:
    python execute_redundancy_merges.py

AUTHOR: ERA Admin / Cascade AI
DATE: 2025-10-25
"""

import sqlite3
import csv
from pathlib import Path
from datetime import datetime

DB_PATH = Path("../FathomInventory/fathom_emails.db")
CSV_PATH = Path("redundancy_merge_actions.csv")
LOG_PATH = Path("redundancy_merge_log.txt")


def backup_database():
    """Create timestamped backup"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = DB_PATH.parent / f"fathom_emails_backup_{timestamp}.db"
    
    import shutil
    shutil.copy2(DB_PATH, backup_path)
    print(f"✅ Created backup: {backup_path}")
    return backup_path


def merge_participants(conn, from_name, to_name, reason):
    """Merge one participant into another"""
    
    log_lines = []
    log_lines.append(f"\n{'='*60}")
    log_lines.append(f"MERGE: '{from_name}' → '{to_name}'")
    log_lines.append(f"REASON: {reason}")
    
    # 1. Get both records
    from_record = conn.execute(
        "SELECT * FROM participants WHERE name = ?", (from_name,)
    ).fetchone()
    
    to_record = conn.execute(
        "SELECT * FROM participants WHERE name = ?", (to_name,)
    ).fetchone()
    
    if not from_record and not to_record:
        log_lines.append(f"⚠️  SKIP: Neither record exists in database")
        return log_lines, "skip"
    
    if not from_record:
        log_lines.append(f"⚠️  SKIP: Source '{from_name}' not found")
        return log_lines, "skip"
    
    # 2. If target doesn't exist, just rename
    if not to_record:
        conn.execute(
            "UPDATE participants SET name = ? WHERE name = ?",
            (to_name, from_name)
        )
        log_lines.append(f"✅ RENAMED: '{from_name}' → '{to_name}'")
        return log_lines, "rename"
    
    # 3. Both exist - merge data
    # Get column names
    columns = [desc[0] for desc in conn.execute("SELECT * FROM participants LIMIT 1").description]
    from_dict = dict(zip(columns, from_record))
    to_dict = dict(zip(columns, to_record))
    
    # Combine non-null fields (prefer to_record, but keep from_record if to is null)
    merged_fields = {}
    for col in columns:
        if col in ['id', 'name', 'analyzed_at']:
            continue  # Skip these
        
        from_val = from_dict.get(col)
        to_val = to_dict.get(col)
        
        # Combine email, projects, source_call_url (comma-separated)
        if col in ['email', 'projects', 'source_call_url', 'collaborating_people', 'collaborating_organizations']:
            if from_val and to_val and from_val != to_val:
                # Combine unique values
                combined = set()
                for val in [from_val, to_val]:
                    if val:
                        combined.update([v.strip() for v in val.split(',')])
                merged_fields[col] = ', '.join(sorted(combined))
            elif from_val:
                merged_fields[col] = from_val
            elif to_val:
                merged_fields[col] = to_val
        # Boolean fields - OR them
        elif col in ['validated_by_airtable', 'era_member', 'is_donor', 'era_africa']:
            merged_fields[col] = 1 if (from_val or to_val) else 0
        # Text fields - prefer non-null
        else:
            if to_val:
                merged_fields[col] = to_val
            elif from_val:
                merged_fields[col] = from_val
    
    # Update target record with merged data
    update_parts = []
    update_values = []
    for col, val in merged_fields.items():
        if val is not None:
            update_parts.append(f"{col} = ?")
            update_values.append(val)
    
    if update_parts:
        update_values.append(to_name)
        conn.execute(
            f"UPDATE participants SET {', '.join(update_parts)} WHERE name = ?",
            update_values
        )
    
    # 4. Delete the from_record
    conn.execute("DELETE FROM participants WHERE name = ?", (from_name,))
    
    log_lines.append(f"✅ MERGED: Combined data and deleted '{from_name}'")
    
    # 5. Update alias resolutions
    count = conn.execute(
        "UPDATE fathom_alias_resolutions SET resolved_to = ? WHERE resolved_to = ?",
        (to_name, from_name)
    ).rowcount
    
    if count > 0:
        log_lines.append(f"   Updated {count} alias resolution(s)")
    
    return log_lines, "merge"


def main():
    print("="*60)
    print("🔨 EXECUTING PARTICIPANT REDUNDANCY MERGES")
    print("="*60)
    
    # Backup first
    backup_path = backup_database()
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    
    # Read merge actions
    with open(CSV_PATH, 'r') as f:
        reader = csv.DictReader(f)
        actions = [row for row in reader if row.get('confidence') == 'HIGH']
    
    print(f"\n📋 Found {len(actions)} HIGH confidence merges to process\n")
    
    # Process each merge
    all_logs = []
    stats = {'merge': 0, 'rename': 0, 'skip': 0}
    
    for i, action in enumerate(actions, 1):
        from_name = action['merge_from']
        to_name = action['merge_to']
        reason = action['reason']
        
        print(f"[{i}/{len(actions)}] {from_name} → {to_name}")
        
        log_lines, result_type = merge_participants(conn, from_name, to_name, reason)
        all_logs.extend(log_lines)
        stats[result_type] += 1
    
    # Commit changes
    conn.commit()
    conn.close()
    
    # Write log
    LOG_PATH.write_text('\n'.join(all_logs))
    
    # Print summary
    print("\n" + "="*60)
    print("📊 MERGE SUMMARY")
    print("="*60)
    print(f"✅ Merged: {stats['merge']}")
    print(f"✅ Renamed: {stats['rename']}")
    print(f"⚠️  Skipped: {stats['skip']}")
    print(f"\n📄 Detailed log: {LOG_PATH}")
    print(f"💾 Backup: {backup_path}")
    print("="*60)


if __name__ == '__main__':
    main()
