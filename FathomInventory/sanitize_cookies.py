#!/usr/bin/env python3
"""Sanitize cookies for Playwright compatibility."""

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
