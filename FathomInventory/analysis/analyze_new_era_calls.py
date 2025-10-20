#!/usr/bin/env python3
"""
Analyze new ERA meetings for daily automation.
Designed to be called from run_all.sh after email download.

This script:
1. Syncs ERA meetings from database to TSV
2. Runs AI analysis on new ERA meetings
3. Parses results and imports to database
4. Returns summary statistics
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent
DB_FILE = SCRIPT_DIR.parent / 'fathom_emails.db'
TSV_FILE = SCRIPT_DIR / 'era connections.tsv'

def log(message):
    """Print with timestamp"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def count_participants():
    """Count current participants in database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM participants")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def run_command(cmd, description):
    """Run command and return success status"""
    log(f"{description}...")
    try:
        result = subprocess.run(
            cmd,
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        log(f"❌ Failed: {e.stderr}")
        return False, e.stderr

def main():
    """Main automation workflow"""
    log("="*60)
    log("ERA MEETING ANALYSIS - Daily Automation")
    log("="*60)
    
    # Count participants before
    participants_before = count_participants()
    log(f"📊 Current participants in database: {participants_before}")
    
    # Step 1: Sync ERA meetings from database
    log("\n🔄 Step 1: Sync ERA meetings from database")
    success, output = run_command(
        [sys.executable, 'sync_era_meetings.py'],
        "Syncing ERA meetings"
    )
    if not success:
        log("⚠️  Sync failed, continuing anyway...")
    
    # Step 2: Run batch analysis (no limit - analyze all new)
    log("\n🤖 Step 2: Analyzing new ERA meetings")
    success, output = run_command(
        [sys.executable, 'batch_analyze_calls.py'],
        "Running AI analysis"
    )
    
    # Count how many were analyzed
    analyses_count = output.count("Analysis successful")
    log(f"📊 Completed {analyses_count} new analyses")
    
    if analyses_count == 0:
        log("ℹ️  No new ERA meetings to analyze")
        return 0
    
    # Step 3: Parse results
    log("\n📝 Step 3: Parsing analysis results")
    success, output = run_command(
        [sys.executable, 'parse_analysis_results.py'],
        "Parsing participant data"
    )
    
    # Step 4: Import to database
    log("\n💾 Step 4: Importing to database")
    success, output = run_command(
        [sys.executable, 'import_new_participants.py'],
        "Importing participants"
    )
    
    # Extract import stats from output
    new_participants = 0
    if "Imported" in output:
        for line in output.split('\n'):
            if "Imported" in line and "participant" in line:
                try:
                    new_participants = int(line.split()[1])
                except:
                    pass
    
    # Final count
    participants_after = count_participants()
    
    # Summary
    log("\n" + "="*60)
    log("✅ ANALYSIS COMPLETE")
    log("="*60)
    log(f"Analyses run: {analyses_count}")
    log(f"New participants: {participants_after - participants_before}")
    log(f"Total participants: {participants_after}")
    log("="*60)
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        log(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
