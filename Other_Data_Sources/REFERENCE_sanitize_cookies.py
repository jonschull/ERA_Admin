#!/usr/bin/env python3
"""
REFERENCE MODEL - DO NOT EDIT

Sanitize cookies for Playwright compatibility.

SOURCE: /Users/admin/ERA_Admin/FathomInventory/sanitize_cookies.py
PROVEN: Production use in FathomInventory since October 2025
STATUS: Stable reference implementation

TO USE:
1. Copy this file to your project
2. Adapt input/output filenames as needed
3. Keep sanitization logic intact

USAGE:
    python sanitize_cookies.py

PURPOSE:
Fixes common cookie format issues that prevent Playwright from loading cookies:
- Invalid sameSite values (must be Strict, Lax, or None)
- Malformed partitionKey fields (Playwright doesn't support objects)

WHEN TO USE:
- After exporting cookies from browser
- Before loading cookies into Playwright
- When seeing cookie validation errors
"""

import json

def sanitize_cookies(cookies):
    """Fix sameSite values for Playwright."""
    valid_same_site_values = {'Strict', 'Lax', 'None'}
    
    for cookie in cookies:
        # Fix sameSite values
        if cookie.get('sameSite') not in valid_same_site_values:
            cookie['sameSite'] = 'Lax'
        
        # Remove problematic partitionKey
        if 'partitionKey' in cookie and not isinstance(cookie.get('partitionKey'), str):
            del cookie['partitionKey']
    
    return cookies

# Read, sanitize, and write back
with open('fathom_cookies_enable.json', 'r') as f:
    cookies = json.load(f)

print(f"Loaded {len(cookies)} cookies")

sanitized = sanitize_cookies(cookies)

with open('fathom_cookies_enable.json', 'w') as f:
    json.dump(sanitized, f, indent=2)

print(f"✅ Sanitized and saved {len(sanitized)} cookies")
