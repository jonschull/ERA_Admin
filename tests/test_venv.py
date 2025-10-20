#!/usr/bin/env python3
"""Test virtual environment setup and dependencies."""

import sys
import subprocess
from pathlib import Path

VENV_PATH = Path("/Users/admin/ERA_Admin_venv")
PYTHON_EXE = VENV_PATH / "bin" / "python3"
PIP_EXE = VENV_PATH / "bin" / "pip"

def test_venv_exists():
    """Test that venv directory exists."""
    assert VENV_PATH.exists(), f"❌ Venv not found at {VENV_PATH}"
    print(f"✅ Venv exists at {VENV_PATH}")

def test_python_executable():
    """Test that Python executable exists and runs."""
    assert PYTHON_EXE.exists(), f"❌ Python not found at {PYTHON_EXE}"
    
    result = subprocess.run(
        [str(PYTHON_EXE), "--version"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"❌ Python execution failed: {result.stderr}"
    print(f"✅ Python executable works: {result.stdout.strip()}")

def test_required_packages():
    """Test that required packages are installed."""
    required_packages = [
        "fuzzywuzzy",           # For cross_correlate.py
        "playwright",           # For FathomInventory
        "bs4",                  # For FathomInventory (beautifulsoup4 package)
        "pyairtable",           # For Airtable scripts
        "google.auth",          # For FathomInventory email download (CRITICAL)
        "google_auth_oauthlib", # For Gmail OAuth
        "googleapiclient",      # For Google API client
    ]
    
    for package in required_packages:
        result = subprocess.run(
            [str(PYTHON_EXE), "-c", f"import {package}"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"⚠️  Package '{package}' not installed")
            return False
        else:
            print(f"✅ Package '{package}' installed")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("TEST: Virtual Environment")
    print("=" * 60)
    
    try:
        test_venv_exists()
        test_python_executable()
        test_required_packages()
        print("\n✅ All venv tests passed")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
