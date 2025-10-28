#!/usr/bin/env python3
"""
Fix ERA member flags based on Town Hall attendance principle.

PRINCIPLE: ERA Member = Attended Town Hall (unless exception made by Jon)

This script:
1. Tests with ONE case first (Abby Karparsi name fix)
2. After validation, can process remaining fixes

Following pattern from update_airtable_bios.py
"""

import os
import sys
from pathlib import Path

# Add airtable module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'airtable'))

try:
    from pyairtable import Api
    from config import AIRTABLE_CONFIG
    AIRTABLE_AVAILABLE = True
except ImportError:
    AIRTABLE_AVAILABLE = False
    print("⚠️  WARNING: pyairtable or config not available")
    print("    Install with: pip install pyairtable")
    print()

# TEST CASE: Single spelling fix to validate approach
TEST_FIX = {
    'id': 'recp6cA4v3QZm3R6A',
    'old_name': 'Abby Karparsi',
    'new_name': 'Abby Karparis',
    'reason': 'Spelling mismatch - database has "Karparis", found in Town Hall transcripts'
}

def test_single_fix():
    """Test with one case before bulk operations."""
    
    print("=" * 80)
    print("TEST: SINGLE SPELLING FIX")
    print("=" * 80)
    print()
    print("PRINCIPLE: ERA Member = Attended Town Hall")
    print()
    
    if not AIRTABLE_AVAILABLE:
        print("❌ Cannot proceed without Airtable configuration")
        return 1
    
    # Initialize Airtable API (same pattern as update_airtable_bios.py)
    api = Api(AIRTABLE_CONFIG['api_key'])
    table = api.table(AIRTABLE_CONFIG['base_id'], AIRTABLE_CONFIG['tables']['people'])
    
    print(f"Testing with: {TEST_FIX['old_name']} → {TEST_FIX['new_name']}")
    print(f"Airtable ID: {TEST_FIX['id']}")
    print(f"Reason: {TEST_FIX['reason']}")
    print()
    
    # First, read current state
    print("📖 Reading current record...")
    try:
        current = table.get(TEST_FIX['id'])
        current_name = current['fields'].get('Name', '')
        current_era = current['fields'].get('era Member', '')
        current_bio = current['fields'].get('Bio', '')
        
        print(f"   Current Name: {current_name}")
        print(f"   ERA Member: {current_era}")
        print(f"   Has Bio: {'Yes' if current_bio else 'No'}")
        print()
        
    except Exception as e:
        print(f"❌ Error reading record: {e}")
        return 1
    
    # Validate before updating
    if current_name != TEST_FIX['old_name']:
        print(f"⚠️  WARNING: Expected '{TEST_FIX['old_name']}' but found '{current_name}'")
        print("   Aborting for safety")
        return 1
    
    # Prompt for confirmation
    print("Ready to update:")
    print(f"  Name: '{TEST_FIX['old_name']}' → '{TEST_FIX['new_name']}'")
    print()
    response = input("Proceed with test update? (yes/no): ")
    
    if response.lower() != 'yes':
        print("❌ Test cancelled by user")
        return 1
    
    # Perform update
    print()
    print("📝 Updating record...")
    try:
        table.update(TEST_FIX['id'], {
            'Name': TEST_FIX['new_name']
        })
        print("✅ Update successful")
        print()
        
        # Read back to verify
        print("🔍 Verifying update...")
        updated = table.get(TEST_FIX['id'])
        updated_name = updated['fields'].get('Name', '')
        
        if updated_name == TEST_FIX['new_name']:
            print(f"✅ Verified: Name is now '{updated_name}'")
            print()
            print("=" * 80)
            print("TEST PASSED - Ready for bulk operations")
            print("=" * 80)
            return 0
        else:
            print(f"❌ Verification failed: Expected '{TEST_FIX['new_name']}' but got '{updated_name}'")
            return 1
            
    except Exception as e:
        print(f"❌ Error updating record: {e}")
        return 1


def main():
    """Main entry point - run test first."""
    
    print()
    print("This script will test Airtable update with ONE case.")
    print("After successful test, we'll build bulk operations.")
    print()
    
    return test_single_fix()


if __name__ == '__main__':
    sys.exit(main())
