#!/usr/bin/env python3
"""
Comprehensive authentication test suite.
Tests both Google API and Fathom cookie authentication systems.
"""

import asyncio
import subprocess
import sys
import os

def run_test_script(script_name):
    """Run a test script and return success status."""
    try:
        print(f"\n{'='*60}")
        print(f"🚀 RUNNING {script_name.upper()}")
        print(f"{'='*60}")
        
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=False, 
                              text=True, 
                              cwd=os.path.dirname(__file__))
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

async def main():
    """Run comprehensive authentication test suite."""
    print("🔐 COMPREHENSIVE AUTHENTICATION TEST SUITE")
    print("=" * 60)
    print("Testing all authentication systems for FathomInventory/ERA_Admin")
    print()
    
    # Test results
    results = {}
    
    # Test Google API authentication
    print("1️⃣  Testing Google API Authentication...")
    results['google_auth'] = run_test_script('test_google_auth.py')
    
    # Test Fathom cookie authentication
    print("\n2️⃣  Testing Fathom Cookie Authentication...")
    # Need to run async test
    try:
        from test_fathom_cookies import main as test_fathom_main
        results['fathom_auth'] = await test_fathom_main()
    except Exception as e:
        print(f"❌ Error running Fathom cookie test: {e}")
        results['fathom_auth'] = False
    
    # Overall summary
    print("\n" + "=" * 60)
    print("🏁 FINAL AUTHENTICATION STATUS")
    print("=" * 60)
    
    google_status = "✅ PASS" if results.get('google_auth') else "❌ FAIL"
    fathom_status = "✅ PASS" if results.get('fathom_auth') else "❌ FAIL"
    
    print(f"Google API Authentication: {google_status}")
    print(f"Fathom Cookie Authentication: {fathom_status}")
    
    # Overall system status
    all_pass = all(results.values())
    overall_status = "✅ FULLY OPERATIONAL" if all_pass else "⚠️  NEEDS ATTENTION"
    
    print(f"\nOverall System Status: {overall_status}")
    
    if all_pass:
        print("\n🎉 All authentication systems are working correctly!")
        print("   The system is ready for automated operation.")
    else:
        print("\n⚠️  Some authentication systems need attention:")
        
        if not results.get('google_auth'):
            print("   • Fix Google API authentication (see google_api_setup_guide.md)")
        
        if not results.get('fathom_auth'):
            print("   • Fix Fathom cookie authentication (see cookie_export_guide.md)")
        
        print("\n   Run individual test scripts for detailed troubleshooting.")
    
    print("\n📚 Documentation available:")
    print("   • README.md - Complete authentication system overview")
    print("   • google_api_setup_guide.md - Google API setup instructions")
    print("   • cookie_export_guide.md - Fathom cookie export instructions")
    
    return all_pass

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
