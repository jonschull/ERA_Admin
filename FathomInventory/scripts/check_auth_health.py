#!/usr/bin/env python3
"""
Quick authentication health check.
Returns exit code 0 if auth is healthy, 1 if needs refresh.
"""

import os
import sys
import subprocess

def main():
    """Check if authentication needs refresh."""
    
    # Change to authentication directory
    auth_dir = os.path.join(os.path.dirname(__file__), 'authentication')
    os.chdir(auth_dir)
    
    # Run the fathom cookie test
    try:
        result = subprocess.run(['python', 'test_fathom_cookies.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0 and "fully functional" in result.stdout:
            print("✅ Authentication healthy")
            return 0
        else:
            print("❌ Authentication needs refresh")
            print("Run: ./refresh_fathom_auth.sh")
            return 1
            
    except Exception as e:
        print(f"❌ Error checking authentication: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
