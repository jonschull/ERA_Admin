#!/usr/bin/env python3
"""
TEMPLATE: Database Modification Script
Copy this template for any script that modifies fathom_emails.db

CRITICAL: This template enforces backup before modifications
"""

import subprocess
import sys
import sqlite3
from pathlib import Path
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
ERA_ADMIN_ROOT = SCRIPT_DIR.parent
FATHOM_DIR = ERA_ADMIN_ROOT / "FathomInventory"
DB_PATH = FATHOM_DIR / "fathom_emails.db"
BACKUP_SCRIPT = FATHOM_DIR / "scripts" / "backup_database.sh"


def require_backup():
    """
    Enforce backup before any database modifications.
    Script exits if backup fails.
    """
    print("=" * 60)
    print("🔒 BACKUP REQUIREMENT CHECK")
    print("=" * 60)
    print(f"Database: {DB_PATH}")
    print(f"Backup script: {BACKUP_SCRIPT}")
    print()
    
    if not BACKUP_SCRIPT.exists():
        print(f"❌ ERROR: Backup script not found: {BACKUP_SCRIPT}")
        print("Cannot proceed without backup capability.")
        sys.exit(1)
    
    print("Running backup script...")
    try:
        result = subprocess.run(
            [str(BACKUP_SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
            cwd=str(FATHOM_DIR)
        )
        print(result.stdout)
        
        # Verify backup was created
        backup_dir = FATHOM_DIR / "backups"
        if not backup_dir.exists():
            print("❌ ERROR: Backup directory not created")
            sys.exit(1)
            
        print("✅ Backup verified - proceeding with database modifications")
        print("=" * 60)
        print()
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ BACKUP FAILED: {e}")
        print(e.stderr)
        print()
        print("Cannot proceed without successful backup.")
        print("Fix backup issues and try again.")
        sys.exit(1)


def get_db_connection():
    """
    Get database connection with proper error handling.
    Uses atomic transactions.
    """
    if not DB_PATH.exists():
        print(f"❌ ERROR: Database not found: {DB_PATH}")
        sys.exit(1)
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn
    except Exception as e:
        print(f"❌ ERROR connecting to database: {e}")
        sys.exit(1)


def verify_database_integrity(conn):
    """Check database integrity before modifications."""
    print("🔍 Checking database integrity...")
    cursor = conn.cursor()
    cursor.execute("PRAGMA integrity_check;")
    result = cursor.fetchone()[0]
    
    if result != "ok":
        print(f"❌ DATABASE INTEGRITY CHECK FAILED: {result}")
        print("Database may be corrupt. Restore from backup.")
        sys.exit(1)
    
    print("✅ Database integrity OK")


def main():
    """
    Main script logic - CUSTOMIZE THIS SECTION
    """
    print()
    print("=" * 60)
    print("SCRIPT NAME: [Your Script Name Here]")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # STEP 1: ALWAYS backup first (REQUIRED)
    require_backup()
    
    # STEP 2: Connect to database
    conn = get_db_connection()
    
    # STEP 3: Verify integrity
    verify_database_integrity(conn)
    
    # STEP 4: YOUR MODIFICATION LOGIC HERE
    try:
        cursor = conn.cursor()
        
        # Begin transaction
        cursor.execute("BEGIN TRANSACTION")
        
        # Example: Add new column
        # cursor.execute("""
        #     ALTER TABLE participants 
        #     ADD COLUMN your_new_column TEXT;
        # """)
        
        # Example: Update records
        # cursor.execute("""
        #     UPDATE participants 
        #     SET your_new_column = 'value'
        #     WHERE condition;
        # """)
        
        # Example: Insert records
        # cursor.execute("""
        #     INSERT INTO participants (name, source_call_url)
        #     VALUES (?, ?);
        # """, (name, url))
        
        # Commit transaction
        conn.commit()
        
        print()
        print("✅ Database modifications completed successfully")
        print()
        
        # STEP 5: Generate report
        # Show what changed
        cursor.execute("SELECT COUNT(*) FROM participants")
        count = cursor.fetchone()[0]
        print(f"Total participants: {count}")
        
        # TODO: Generate detailed report file
        
    except Exception as e:
        # Rollback on error
        conn.rollback()
        print()
        print(f"❌ ERROR during database modification: {e}")
        print("Transaction rolled back - database unchanged")
        print()
        print("💡 Database restored to pre-modification state")
        sys.exit(1)
        
    finally:
        conn.close()
    
    print()
    print("=" * 60)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


if __name__ == "__main__":
    # Safety check: Confirm user wants to proceed
    print()
    print("⚠️  This script will modify the database.")
    print(f"   Database: {DB_PATH}")
    print()
    response = input("Continue? (yes/no): ").strip().lower()
    
    if response != "yes":
        print("Aborted by user")
        sys.exit(0)
    
    main()
