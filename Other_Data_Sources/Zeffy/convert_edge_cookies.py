#!/usr/bin/env python3
"""
Convert Edge developer tools cookie export to JSON format for Zeffy.

ADAPTED FROM: /Users/admin/ERA_Admin/Other_Data_Sources/REFERENCE_convert_edge_cookies.py
PATTERN: Browser Cookie Authentication Pattern

USAGE:
    python convert_edge_cookies.py

PROCESS:
1. User copies cookies from Edge DevTools (Application → Cookies)
2. Pastes tab-separated data into script
3. Script converts to Playwright-compatible JSON
4. Saves as zeffy_cookies.json
"""

import json
import sys
from datetime import datetime

def convert_edge_cookies():
    print("Edge Cookie Converter - Zeffy")
    print("=" * 50)
    print("1. Copy cookies from Edge Developer Tools")
    print("2. Paste them below (press Enter twice when done)")
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
        print("No cookie data provided.")
        return
    
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
            domain = parts[2] if parts[2] else ".zeffy.com"
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
        with open('zeffy_cookies.json', 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print(f"\n✅ Successfully converted {len(cookies)} cookies")
        print("✅ Saved to zeffy_cookies.json")
        print("\nNext step: Run sanitize_cookies.py to fix compatibility issues")
    else:
        print("❌ No valid cookies found in the data")

if __name__ == "__main__":
    convert_edge_cookies()
