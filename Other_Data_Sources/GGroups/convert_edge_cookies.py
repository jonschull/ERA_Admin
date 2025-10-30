#!/usr/bin/env python3
"""
Convert Edge developer tools cookie export to JSON format for Google Groups.

Adapted from: /Other_Data_Sources/REFERENCE_convert_edge_cookies.py

Usage:
    python convert_edge_cookies.py
    
Process:
    1. Log into groups.google.com in Edge
    2. Open DevTools (F12) → Application → Cookies
    3. Select all cookies (Ctrl+A) and copy (Ctrl+C)
    4. Run this script and paste when prompted
    5. Press Enter twice to finish
"""

import json
import sys
from datetime import datetime

def convert_edge_cookies():
    print("=" * 80)
    print("GOOGLE GROUPS COOKIE CONVERTER")
    print("=" * 80)
    print()
    print("Instructions:")
    print("1. Open Microsoft Edge")
    print("2. Go to https://groups.google.com")
    print("3. Make sure you're logged in")
    print("4. Press F12 → Application tab → Cookies → https://groups.google.com")
    print("5. Select all cookies (Ctrl+A) and copy (Ctrl+C)")
    print("6. Paste them below")
    print("7. Press Enter twice when done")
    print()
    
    lines = []
    print("Paste your cookies here:")
    
    while True:
        try:
            line = input()
            if line.strip() == "":
                if lines:  # If we have some lines and get empty line, we're done
                    break
            else:
                lines.append(line)
        except EOFError:
            break
    
    if not lines:
        print("❌ No cookie data provided.")
        return False
    
    cookies = []
    
    # Skip header line if present
    start_idx = 0
    if lines[0].startswith("Name\t"):
        start_idx = 1
    
    for line in lines[start_idx:]:
        parts = line.split('\t')
        if len(parts) >= 6:  # Minimum required fields
            name = parts[0]
            value = parts[1]
            domain = parts[2] if parts[2] else ".google.com"
            path = parts[3] if parts[3] else "/"
            expires = parts[4] if len(parts) > 4 else ""
            
            # Convert expires to timestamp if present
            expiration_date = None
            if expires and expires != "Session":
                try:
                    # Edge typically shows dates like "2025-01-01T00:00:00.000Z"
                    if "T" in expires:
                        dt = datetime.fromisoformat(expires.replace('Z', '+00:00'))
                        expiration_date = int(dt.timestamp())
                except:
                    pass
            
            cookie = {
                "name": name,
                "value": value,
                "domain": domain if domain.startswith('.') else f".{domain}",
                "path": path,
                "secure": True,
                "httpOnly": False,
                "sameSite": "Lax",
                "session": expiration_date is None
            }
            
            if expiration_date:
                cookie["expirationDate"] = expiration_date
            
            cookies.append(cookie)
    
    if cookies:
        # Write to file
        with open('ggroups_cookies.json', 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print()
        print("=" * 80)
        print(f"✅ Successfully converted {len(cookies)} cookies")
        print("✅ Saved to ggroups_cookies.json")
        print("=" * 80)
        print()
        print("Next steps:")
        print("1. Test: python download_members.py")
        return True
    else:
        print("❌ No valid cookies found in the data")
        return False

if __name__ == "__main__":
    success = convert_edge_cookies()
    sys.exit(0 if success else 1)
