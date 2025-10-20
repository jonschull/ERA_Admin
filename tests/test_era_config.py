#!/usr/bin/env python3
"""Test ERA configuration system."""

import sys
from pathlib import Path

# Add parent to path to import era_config
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from era_config import Config
    CONFIG_IMPORTED = True
except ImportError as e:
    CONFIG_IMPORTED = False
    IMPORT_ERROR = str(e)

def test_config_import():
    """Test that era_config can be imported."""
    assert CONFIG_IMPORTED, f"❌ Failed to import era_config: {IMPORT_ERROR}"
    print("✅ era_config imported successfully")

def test_config_paths():
    """Test that all config paths resolve correctly."""
    paths_to_test = {
        "ERA_ADMIN_ROOT": Config.ERA_ADMIN_ROOT,
        "AIRTABLE_DIR": Config.AIRTABLE_DIR,
        "FATHOM_INVENTORY_ROOT": Config.FATHOM_INVENTORY_ROOT,
        "FATHOM_DB_PATH": Config.FATHOM_DB_PATH,
    }
    
    for name, path in paths_to_test.items():
        path_obj = Path(path)
        assert path_obj.exists(), f"❌ {name} does not exist: {path}"
        print(f"✅ {name}: {path}")

def test_fathom_db_path():
    """Test that Fathom DB path is correct."""
    db_path = Path(Config.FATHOM_DB_PATH)
    assert db_path.exists(), f"❌ Fathom DB not found at {db_path}"
    assert db_path.name == "fathom_emails.db", f"❌ Wrong DB name: {db_path.name}"
    print(f"✅ Fathom DB path correct: {Config.FATHOM_DB_PATH}")

if __name__ == "__main__":
    print("=" * 60)
    print("TEST: ERA Configuration")
    print("=" * 60)
    
    try:
        test_config_import()
        test_config_paths()
        test_fathom_db_path()
        print("\n✅ All config tests passed")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
