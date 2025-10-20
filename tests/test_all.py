#!/usr/bin/env python3
"""
Full system test - runs after component tests pass.
Tests the complete FathomInventory run_all.sh execution.
"""

import sys
import subprocess
from pathlib import Path
import time

ERA_ADMIN = Path("/Users/admin/Library/CloudStorage/Dropbox-EcoRestorationAllianceLLC/Jon Schull/CascadeProjects/ERA_Admin")
FATHOM_DIR = ERA_ADMIN / "FathomInventory"
RUN_ALL_SH = FATHOM_DIR / "run_all.sh"

def run_component_tests():
    """First run all component tests."""
    print("=" * 60)
    print("STEP 1: Running Component Tests")
    print("=" * 60)
    
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "test_component_tests.py")],
        capture_output=False
    )
    
    if result.returncode != 0:
        print("\n❌ Component tests failed - aborting full system test")
        return False
    
    print("\n✅ Component tests passed")
    return True

def test_full_system():
    """Run the full FathomInventory system."""
    print("\n" + "=" * 60)
    print("STEP 2: Full System Test (run_all.sh)")
    print("=" * 60)
    print(f"Running: {RUN_ALL_SH}")
    print("This will take ~5-10 minutes (includes 5 min wait for emails)")
    print("=" * 60 + "\n")
    
    start_time = time.time()
    
    result = subprocess.run(
        ["/bin/bash", str(RUN_ALL_SH)],
        cwd=str(FATHOM_DIR),
        capture_output=False  # Show output in real-time
    )
    
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    
    print(f"\n⏱️  Elapsed time: {minutes}m {seconds}s")
    
    return result.returncode == 0

if __name__ == "__main__":
    print("=" * 60)
    print("FULL SYSTEM TEST - ERA_Admin Recovery")
    print("=" * 60)
    print("⚠️  WARNING: This will run the full FathomInventory system")
    print("   and may take 5-10 minutes to complete.")
    print("=" * 60 + "\n")
    
    # Run component tests first
    if not run_component_tests():
        sys.exit(1)
    
    # Run full system test
    print("\n⏸️  Starting full system test in 3 seconds...")
    time.sleep(3)
    
    if test_full_system():
        print("\n" + "=" * 60)
        print("✅ FULL SYSTEM TEST PASSED")
        print("=" * 60)
        print("FathomInventory system is fully operational!")
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ FULL SYSTEM TEST FAILED")
        print("=" * 60)
        print("Check the output above for errors")
        sys.exit(1)
