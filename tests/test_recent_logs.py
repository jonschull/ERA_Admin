#!/usr/bin/env python3
"""Test recent log files for failures and silent problems."""

import sys
from pathlib import Path
from datetime import datetime, timedelta

MONITOR_LOG = Path("/Users/admin/Library/Logs/fathom_monitor.log")
CRON_LOG = Path("/Users/admin/ERA_Admin/FathomInventory/cron.log")

def test_no_recent_crash_loops():
    """Test that monitor is not in a crash loop."""
    if not MONITOR_LOG.exists():
        print("⚠️  Monitor log doesn't exist yet")
        return True
    
    # Get file modification time
    mtime = datetime.fromtimestamp(MONITOR_LOG.stat().st_mtime)
    age = datetime.now() - mtime
    
    if age > timedelta(hours=2):
        print(f"⚠️  Monitor log is {age.total_seconds()/3600:.1f} hours old (may not be running)")
        return True
    
    # Read last 100 lines
    with open(MONITOR_LOG, 'r') as f:
        lines = f.readlines()[-100:]
    
    # Count recent failures
    failures = [l for l in lines if "failed to start or crashed immediately" in l]
    starts = [l for l in lines if "Starting Fathom script" in l]
    
    if len(failures) >= 5:
        print(f"❌ CRASH LOOP DETECTED: {len(failures)} failures in recent log")
        print("   Last 3 failures:")
        for line in failures[-3:]:
            print(f"   {line.strip()}")
        return False
    elif len(failures) > 0:
        print(f"⚠️  {len(failures)} recent failure(s) detected:")
        for line in failures[-2:]:
            print(f"   {line.strip()}")
        return True
    elif len(starts) > 0:
        print(f"✅ Monitor shows activity with no failures ({len(starts)} starts)")
        return True
    else:
        print("✅ No recent failures in monitor log")
        return True

def test_recent_successful_run():
    """Test that there was a recent successful run."""
    if not CRON_LOG.exists():
        print("❌ Cron log doesn't exist")
        return False
    
    # Get file modification time
    mtime = datetime.fromtimestamp(CRON_LOG.stat().st_mtime)
    age = datetime.now() - mtime
    
    if age > timedelta(hours=24):
        print(f"⚠️  Cron log is {age.total_seconds()/3600:.1f} hours old")
        print("   No successful run in last 24 hours")
        return False
    
    # Read last 50 lines
    with open(CRON_LOG, 'r') as f:
        lines = f.readlines()[-50:]
    
    # Look for success marker
    success_lines = [l for l in lines if "finished successfully" in l.lower()]
    error_lines = [l for l in lines if "error" in l.lower() or "failed" in l.lower()]
    
    if success_lines:
        last_success = success_lines[-1].strip()
        print(f"✅ Recent successful run found:")
        print(f"   {last_success}")
        return True
    elif error_lines:
        print("❌ Recent run found but with errors:")
        for line in error_lines[-2:]:
            print(f"   {line.strip()}")
        return False
    else:
        print("⚠️  No clear success or failure in recent logs")
        return True

def test_no_silent_failures():
    """Test for silent failures (marked success but actually failed)."""
    if not CRON_LOG.exists():
        return True
    
    with open(CRON_LOG, 'r') as f:
        lines = f.readlines()[-200:]
    
    # Look for contradiction: marked success but had errors
    text = ''.join(lines)
    
    has_success = "finished successfully" in text.lower()
    has_fatal = "fatal python error" in text.lower()
    has_deadlock = "resource deadlock" in text.lower()
    
    if has_success and (has_fatal or has_deadlock):
        print("❌ SILENT FAILURE DETECTED:")
        print("   Log shows 'finished successfully' but also contains fatal errors")
        if has_fatal:
            print("   - Contains 'Fatal Python error'")
        if has_deadlock:
            print("   - Contains 'Resource deadlock avoided'")
        return False
    
    print("✅ No silent failures detected")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("TEST: Recent Logs Analysis")
    print("=" * 60)
    
    try:
        success = True
        
        if not test_no_recent_crash_loops():
            success = False
        
        if not test_recent_successful_run():
            success = False
        
        if not test_no_silent_failures():
            success = False
        
        if success:
            print("\n✅ All log analysis tests passed")
            sys.exit(0)
        else:
            print("\n❌ Some log analysis tests failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
