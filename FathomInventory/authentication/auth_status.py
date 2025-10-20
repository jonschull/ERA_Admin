#!/usr/bin/env python3
"""
Quick authentication status check.
Provides fast overview of authentication file status without full testing.
"""

import os
import json
from datetime import datetime, timezone

def check_file_status(filename, description):
    """Check if a file exists and get basic info."""
    filepath = f"../{filename}"
    
    if not os.path.exists(filepath):
        return f"❌ {description}: File not found"
    
    try:
        size = os.path.getsize(filepath)
        if size == 0:
            return f"⚠️  {description}: File is empty"
        
        # Try to parse JSON for additional info
        if filename.endswith('.json'):
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            if filename == 'token.json':
                # Check token expiry
                if 'expiry' in data:
                    expiry_str = data['expiry']
                    expiry_time = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
                    now = datetime.now(timezone.utc)
                    
                    if expiry_time > now:
                        time_left = expiry_time - now
                        hours_left = int(time_left.total_seconds() / 3600)
                        return f"✅ {description}: Valid ({hours_left}h remaining)"
                    else:
                        return f"⚠️  {description}: Access token expired"
                else:
                    return f"✅ {description}: Present (no expiry info)"
            
            elif filename == 'fathom_cookies.json':
                # Check cookie count and expiry
                if isinstance(data, list):
                    now = datetime.now(timezone.utc).timestamp()
                    expired_count = 0
                    
                    for cookie in data:
                        if 'expirationDate' in cookie and cookie['expirationDate'] < now:
                            expired_count += 1
                    
                    total_cookies = len(data)
                    if expired_count == 0:
                        return f"✅ {description}: {total_cookies} cookies, all valid"
                    elif expired_count < total_cookies * 0.5:
                        return f"⚠️  {description}: {total_cookies} cookies, {expired_count} expired"
                    else:
                        return f"❌ {description}: {total_cookies} cookies, {expired_count} expired (>50%)"
                else:
                    return f"⚠️  {description}: Invalid format (not array)"
            
            else:
                # credentials.json
                return f"✅ {description}: Valid JSON ({size:,} bytes)"
        
        else:
            return f"✅ {description}: Present ({size:,} bytes)"
    
    except json.JSONDecodeError:
        return f"❌ {description}: Invalid JSON"
    except Exception as e:
        return f"❌ {description}: Error reading file ({e})"

def main():
    """Quick authentication status overview."""
    print("🔐 AUTHENTICATION STATUS OVERVIEW")
    print("=" * 50)
    
    # Check each authentication file
    files_to_check = [
        ('credentials.json', 'Google API Credentials'),
        ('token.json', 'Google OAuth Token'),
        ('fathom_cookies.json', 'Fathom Session Cookies')
    ]
    
    statuses = []
    for filename, description in files_to_check:
        status = check_file_status(filename, description)
        print(status)
        statuses.append('✅' in status)
    
    # Overall status
    print("\n" + "=" * 50)
    if all(statuses):
        print("🎉 All authentication files present and appear valid")
        print("   Run 'python test_all_auth.py' for comprehensive testing")
    elif any(statuses):
        print("⚠️  Some authentication files need attention")
        print("   Run individual test scripts for detailed diagnosis")
    else:
        print("❌ No authentication files found")
        print("   See setup guides in this directory")
    
    print("\n📚 Available commands:")
    print("   python test_google_auth.py    - Test Google API authentication")
    print("   python test_fathom_cookies.py - Test Fathom cookie authentication")
    print("   python test_all_auth.py       - Run comprehensive test suite")

if __name__ == "__main__":
    main()
