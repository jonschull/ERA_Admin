#!/usr/bin/env python3
"""Test FathomInventory paths and accessibility."""

import sys
from pathlib import Path

ERA_ADMIN = Path("/Users/admin/Library/CloudStorage/Dropbox-EcoRestorationAllianceLLC/Jon Schull/CascadeProjects/ERA_Admin")
FATHOM_DIR = ERA_ADMIN / "FathomInventory"
FATHOM_DB = FATHOM_DIR / "fathom_emails.db"
RUN_ALL_SH = FATHOM_DIR / "run_all.sh"

def test_fathom_directory():
    """Test that FathomInventory directory exists."""
    assert FATHOM_DIR.exists(), f"❌ FathomInventory not found at {FATHOM_DIR}"
    print(f"✅ FathomInventory directory exists")

def test_database_accessible():
    """Test that database file exists and is accessible."""
    assert FATHOM_DB.exists(), f"❌ Database not found at {FATHOM_DB}"
    
    # Check file size
    size_mb = FATHOM_DB.stat().st_size / (1024 * 1024)
    assert size_mb > 10, f"❌ Database too small ({size_mb:.1f} MB), may be corrupted"
    print(f"✅ Database accessible ({size_mb:.1f} MB)")

def test_run_all_script():
    """Test that run_all.sh exists and is executable."""
    assert RUN_ALL_SH.exists(), f"❌ run_all.sh not found at {RUN_ALL_SH}"
    assert RUN_ALL_SH.stat().st_mode & 0o111, f"❌ run_all.sh is not executable"
    print(f"✅ run_all.sh exists and is executable")

def test_authentication_files():
    """Test that authentication files exist."""
    auth_files = [
        FATHOM_DIR / "fathom_cookies.json",
        FATHOM_DIR / "token.json",
        FATHOM_DIR / "credentials.json",
    ]
    
    for auth_file in auth_files:
        if auth_file.exists():
            print(f"✅ {auth_file.name} exists")
        else:
            print(f"⚠️  {auth_file.name} missing (may need setup)")

if __name__ == "__main__":
    print("=" * 60)
    print("TEST: FathomInventory Paths")
    print("=" * 60)
    
    try:
        test_fathom_directory()
        test_database_accessible()
        test_run_all_script()
        test_authentication_files()
        print("\n✅ All path tests passed")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
