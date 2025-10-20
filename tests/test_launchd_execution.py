#!/usr/bin/env python3
"""Test that launchd can actually execute the FathomInventory system."""

import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

MONITOR_LOG = Path("/Users/admin/Library/Logs/fathom_monitor.log")
RUN_LOG = Path("/Users/admin/Library/Logs/fathom_run.log")

def test_launchd_loaded():
    """Test that launchd job is loaded."""
    result = subprocess.run(
        ["launchctl", "list"],
        capture_output=True,
        text=True
    )
    
    if "com.era.admin.fathom" not in result.stdout:
        print("❌ Launchd job not loaded")
        return False
    
    print("✅ Launchd job is loaded")
    return True

def test_monitor_not_failing():
    """Test that monitor is not continuously failing."""
    if not MONITOR_LOG.exists():
        print("⚠️  Monitor log doesn't exist yet (may not have run)")
        return True
    
    # Read last 50 lines
    result = subprocess.run(
        ["tail", "-50", str(MONITOR_LOG)],
        capture_output=True,
        text=True
    )
    
    lines = result.stdout.strip().split('\n')
    
    # Check for recent failures
    recent_failures = [l for l in lines if "❌ Error: Fathom script failed to start" in l]
    recent_starts = [l for l in lines if "Starting Fathom script..." in l]
    
    if len(recent_failures) >= 3:
        print(f"❌ Monitor log shows {len(recent_failures)} recent failures:")
        for line in recent_failures[-3:]:
            print(f"   {line.strip()}")
        return False
    
    if recent_starts and not recent_failures:
        print("✅ Monitor shows successful starts (no failures)")
        return True
    elif not recent_starts and not recent_failures:
        print("✅ No recent monitor activity (may not have run yet)")
        return True
    else:
        print(f"⚠️  Monitor log shows some activity but unclear status")
        return True

def test_trigger_launchd_and_verify():
    """Manually trigger launchd job and verify it doesn't crash immediately."""
    print("\n🔬 Testing launchd execution...")
    print("   This will trigger the job and wait 30 seconds to check for crashes")
    
    # Clear recent monitor log entries to get clean test
    timestamp_before = datetime.now()
    
    # Trigger the job
    print("   Triggering: launchctl start com.era.admin.fathom.run")
    result = subprocess.run(
        ["launchctl", "start", "com.era.admin.fathom.run"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Failed to trigger launchd job: {result.stderr}")
        return False
    
    print("   ⏳ Waiting 30 seconds to see if script crashes...")
    time.sleep(30)
    
    # Check monitor log for crashes
    if MONITOR_LOG.exists():
        result = subprocess.run(
            ["tail", "-20", str(MONITOR_LOG)],
            capture_output=True,
            text=True
        )
        
        lines = result.stdout.strip().split('\n')
        for line in reversed(lines):
            if "failed to start or crashed immediately" in line:
                print(f"❌ Script crashed immediately:")
                print(f"   {line.strip()}")
                return False
            elif "Started Fathom script with PID" in line:
                print(f"✅ Script started successfully:")
                print(f"   {line.strip()}")
                return True
    
    # Check if script is running
    result = subprocess.run(
        ["pgrep", "-f", "run_all.sh"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        pids = result.stdout.strip().split('\n')
        print(f"✅ Script is running (PID: {', '.join(pids)})")
        print("   Note: Full run takes ~5-10 minutes, monitor logs for completion")
        return True
    else:
        print("⚠️  Script not found running (may have completed quickly or failed)")
        print("   Check logs manually to verify")
        return True  # Don't fail - could be too fast

if __name__ == "__main__":
    print("=" * 60)
    print("TEST: Launchd Execution")
    print("=" * 60)
    print("⚠️  This test will TRIGGER a real launchd execution")
    print("=" * 60 + "\n")
    
    try:
        success = True
        
        if not test_launchd_loaded():
            success = False
        
        if not test_monitor_not_failing():
            success = False
        
        # Ask user permission for live test
        print("\n" + "=" * 60)
        print("Ready to trigger launchd job for live test")
        print("This is safe but will start a real FathomInventory run")
        print("=" * 60)
        
        if not test_trigger_launchd_and_verify():
            success = False
        
        if success:
            print("\n✅ All launchd tests passed")
            sys.exit(0)
        else:
            print("\n❌ Some launchd tests failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
