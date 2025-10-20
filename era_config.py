"""
ERA Admin Configuration
Central configuration for external dependencies and system paths.

Update this file when moving to server or changing locations.
"""

import os
from pathlib import Path

# Get ERA_Admin root directory (this file is in ERA_Admin/)
ERA_ADMIN_ROOT = Path(__file__).parent.resolve()

# Internal paths (relative to ERA_Admin) - portable
AIRTABLE_DIR = ERA_ADMIN_ROOT / "airtable"
AIRTABLE_EXPORTS_DIR = AIRTABLE_DIR
LANDSCAPE_DIR = ERA_ADMIN_ROOT.parent / "ERA_Landscape_Static"  # Sibling folder

# External paths - EDIT THESE when moving to server
# Option 1: Use environment variable (preferred for server)
# Option 2: Hardcode path here (easier for local dev)

# FathomInventory location (now in ERA_Admin)
FATHOM_INVENTORY_ROOT = os.environ.get(
    'FATHOM_INVENTORY_ROOT',
    str(ERA_ADMIN_ROOT / 'FathomInventory')  # Default for local laptop
)

# Derived paths from FathomInventory
FATHOM_DB = Path(FATHOM_INVENTORY_ROOT) / "fathom_emails.db"
FATHOM_ANALYSIS_DIR = Path(FATHOM_INVENTORY_ROOT) / "analysis"

# Fathom Account Configuration
# Which Fathom account to use for scraping calls
FATHOM_ACTIVE_ACCOUNT = os.environ.get('FATHOM_ACCOUNT', 'enable')  # 'enable' or 'era'

FATHOM_ACCOUNTS = {
    'enable': {
        'name': 'e-NABLE',
        'cookies_file': 'fathom_cookies_enable.json',
        'email': 'jschull@e-nable.org',
        'share_to': 'fathomizer@ecorestorationalliance.org'
    },
    'era': {
        'name': 'ERA',
        'cookies_file': 'fathom_cookies_era.json',
        'email': 'ecorestorationalliance@gmail.com',
        'share_to': 'fathomizer@ecorestorationalliance.org'
    }
}

# Get active account config
def get_fathom_account_config(account=None):
    """Get configuration for specified Fathom account (or active account)"""
    account = account or FATHOM_ACTIVE_ACCOUNT
    if account not in FATHOM_ACCOUNTS:
        raise ValueError(f"Unknown Fathom account: {account}. Valid options: {list(FATHOM_ACCOUNTS.keys())}")
    return FATHOM_ACCOUNTS[account]

# Google Sheets configuration
LANDSCAPE_SHEET_ID = "1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY"

# Airtable configuration (read from airtable/config.py)
# Don't duplicate - import from there if needed


class Config:
    """
    Centralized configuration object.
    Usage: from era_config import Config
    """
    
    # Directories
    ERA_ADMIN_ROOT = ERA_ADMIN_ROOT
    AIRTABLE_DIR = AIRTABLE_DIR
    LANDSCAPE_DIR = LANDSCAPE_DIR
    FATHOM_INVENTORY_ROOT = Path(FATHOM_INVENTORY_ROOT)
    
    # Databases
    FATHOM_DB_PATH = FATHOM_DB
    
    # Exports
    AIRTABLE_PEOPLE_CSV = AIRTABLE_EXPORTS_DIR / "people_export.csv"
    AIRTABLE_MATCHING_CSV = AIRTABLE_EXPORTS_DIR / "people_for_matching.csv"
    
    # Google Sheets
    LANDSCAPE_SHEET_ID = LANDSCAPE_SHEET_ID
    
    # Fathom Account
    FATHOM_ACTIVE_ACCOUNT = FATHOM_ACTIVE_ACCOUNT
    FATHOM_ACCOUNTS = FATHOM_ACCOUNTS
    
    @classmethod
    def get_fathom_config(cls, account=None):
        """Get Fathom account configuration"""
        return get_fathom_account_config(account)
    
    @classmethod
    def verify_paths(cls):
        """Verify all critical paths exist."""
        checks = {
            'ERA_Admin root': cls.ERA_ADMIN_ROOT,
            'Airtable directory': cls.AIRTABLE_DIR,
            'FathomInventory root': cls.FATHOM_INVENTORY_ROOT,
            'Fathom database': cls.FATHOM_DB_PATH,
        }
        
        missing = []
        for name, path in checks.items():
            if not path.exists():
                missing.append(f"{name}: {path}")
        
        if missing:
            print("⚠️  Warning: Missing paths:")
            for item in missing:
                print(f"   - {item}")
            return False
        
        print("✅ All paths verified")
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration."""
        print("ERA Admin Configuration:")
        print("=" * 50)
        print(f"ERA_Admin root: {cls.ERA_ADMIN_ROOT}")
        print(f"Airtable dir:   {cls.AIRTABLE_DIR}")
        print(f"Landscape dir:  {cls.LANDSCAPE_DIR}")
        print(f"Fathom root:    {cls.FATHOM_INVENTORY_ROOT}")
        print(f"Fathom DB:      {cls.FATHOM_DB_PATH}")
        
        # Show active Fathom account
        fathom_config = cls.get_fathom_config()
        print(f"\nActive Fathom Account: {cls.FATHOM_ACTIVE_ACCOUNT}")
        print(f"  Name:         {fathom_config['name']}")
        print(f"  Email:        {fathom_config['email']}")
        print(f"  Cookies file: {fathom_config['cookies_file']}")
        print("=" * 50)


# Server deployment example:
"""
On server, set environment variables before running:

export FATHOM_INVENTORY_ROOT=/opt/era/FathomInventory
export FATHOM_ACCOUNT=enable  # or 'era' to use different Fathom account

Or edit this file directly to change defaults.

To switch Fathom accounts:
1. Set FATHOM_ACCOUNT environment variable (preferred)
2. Or edit FATHOM_ACTIVE_ACCOUNT in this file
"""

if __name__ == "__main__":
    # Test configuration
    Config.print_config()
    Config.verify_paths()
