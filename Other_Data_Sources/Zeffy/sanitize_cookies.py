#!/usr/bin/env python3
"""
Sanitize cookies for Playwright compatibility - Zeffy.

ADAPTED FROM: /Users/admin/ERA_Admin/Other_Data_Sources/REFERENCE_sanitize_cookies.py
PATTERN: Browser Cookie Authentication Pattern

USAGE:
    python sanitize_cookies.py

PURPOSE:
Fixes common cookie format issues that prevent Playwright from loading cookies:
- Invalid sameSite values (must be Strict, Lax, or None)
- Removes fields Playwright doesn't support (storeId, hostOnly)
- Handles null sameSite values from cookie-editor extension

WHEN TO USE:
- After exporting cookies from cookie-editor extension
- Before loading cookies into Playwright
"""

import json

def sanitize_cookies(cookies):
    """Fix cookie format for Playwright compatibility."""
    valid_same_site_values = {'Strict', 'Lax', 'None'}
    
    for cookie in cookies:
        # Fix sameSite values (cookie-editor uses lowercase, Playwright needs capitalized)
        same_site = cookie.get('sameSite')
        if same_site is None:
            cookie['sameSite'] = 'Lax'
        elif isinstance(same_site, str):
            # Capitalize first letter
            same_site_capitalized = same_site.capitalize() if same_site else 'Lax'
            if same_site_capitalized not in valid_same_site_values:
                cookie['sameSite'] = 'Lax'
            else:
                cookie['sameSite'] = same_site_capitalized
        
        # Remove fields Playwright doesn't support
        for field in ['storeId', 'hostOnly', 'partitionKey']:
            if field in cookie:
                del cookie[field]
    
    return cookies

# Read, sanitize, and write back
try:
    with open('zeffy_cookies.json', 'r') as f:
        cookies = json.load(f)
    
    print(f"Loaded {len(cookies)} cookies")
    
    sanitized = sanitize_cookies(cookies)
    
    with open('zeffy_cookies.json', 'w') as f:
        json.dump(sanitized, f, indent=2)
    
    print(f"✅ Sanitized and saved {len(sanitized)} cookies")
    print("✅ Ready for Playwright automation!")
    
except FileNotFoundError:
    print("❌ zeffy_cookies.json not found")
    print("   Please paste cookie-editor JSON into zeffy_cookies.json first")
except json.JSONDecodeError:
    print("❌ Invalid JSON in zeffy_cookies.json")
    print("   Please check the file format")
