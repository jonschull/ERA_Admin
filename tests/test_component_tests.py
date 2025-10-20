#!/usr/bin/env python3
"""Run all component tests before full system test."""

import sys
import subprocess
from pathlib import Path

TESTS_DIR = Path(__file__).parent

def run_test(test_script):
    """Run a single test script and return result."""
    print(f"\n{'=' * 60}")
    print(f"Running: {test_script.name}")
    print('=' * 60)
    
    result = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=False  # Show output in real-time
    )
    
    return result.returncode == 0

if __name__ == "__main__":
    print("=" * 60)
    print("COMPONENT TESTS - ERA_Admin Recovery")
    print("=" * 60)
    
    tests = [
        TESTS_DIR / "test_venv.py",
        TESTS_DIR / "test_fathom_paths.py",
        TESTS_DIR / "test_era_config.py",
        TESTS_DIR / "test_recent_logs.py",
    ]
    
    results = {}
    for test in tests:
        if test.exists():
            results[test.name] = run_test(test)
        else:
            print(f"⚠️  Test not found: {test.name}")
            results[test.name] = False
    
    print("\n" + "=" * 60)
    print("COMPONENT TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    if all(results.values()):
        print("\n✅ All component tests passed - ready for full system test")
        sys.exit(0)
    else:
        print("\n❌ Some component tests failed - fix before full system test")
        sys.exit(1)
