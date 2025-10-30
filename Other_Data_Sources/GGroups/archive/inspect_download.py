#!/usr/bin/env python3
"""
Inspect what happens when download button is clicked.

This script:
1. Opens the members page with cookies
2. Enables network monitoring
3. Waits for you to click the download button
4. Shows what network requests were made

Usage:
    python inspect_download.py
"""

import json
from pathlib import Path
from playwright.sync_api import sync_playwright

# Configuration
SCRIPT_DIR = Path(__file__).parent
COOKIE_FILE = SCRIPT_DIR / "ggroups_cookies.json"
GROUP_URL = "https://groups.google.com/g/ecorestoration-alliance/members"

def sanitize_cookies(cookies):
    """Fix sameSite values for Playwright compatibility."""
    valid_same_site_values = {'Strict', 'Lax', 'None'}
    
    for cookie in cookies:
        if cookie.get('sameSite') not in valid_same_site_values:
            cookie['sameSite'] = 'Lax'
        if 'partitionKey' in cookie and not isinstance(cookie.get('partitionKey'), str):
            del cookie['partitionKey']
    
    return cookies

def inspect_download():
    print("=" * 80)
    print("NETWORK INSPECTOR - Google Groups Download")
    print("=" * 80)
    print()
    
    # Load cookies
    print("🔐 Loading cookies...")
    with open(COOKIE_FILE, 'r') as f:
        cookies = json.load(f)
    cookies = sanitize_cookies(cookies)
    print(f"   Loaded {len(cookies)} cookies")
    print()
    
    with sync_playwright() as p:
        print("🌐 Launching Microsoft Edge...")
        browser = p.chromium.launch(
            channel="msedge",
            headless=False
        )
        
        context = browser.new_context()
        context.add_cookies(cookies)
        
        page = context.new_page()
        
        # Track network requests
        requests = []
        
        def log_request(request):
            # Capture post_data safely - some requests have binary data
            try:
                post_data = request.post_data
            except:
                post_data = '<binary data>'
        
            requests.append({
                'method': request.method,
                'url': request.url,
                'headers': dict(request.headers),
                'post_data': post_data
            })
        
        def log_response(response):
            print(f"📡 {response.request.method} {response.status} {response.url}")
            if 'download' in response.url.lower() or 'export' in response.url.lower():
                print(f"   ⭐ DOWNLOAD REQUEST DETECTED!")
                print(f"   Method: {response.request.method}")
                print(f"   URL: {response.url}")
                print(f"   Status: {response.status}")
                print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
        
        page.on('request', log_request)
        page.on('response', log_response)
        
        # Navigate to members page
        print(f"📍 Navigating to: {GROUP_URL}")
        page.goto(GROUP_URL, wait_until='networkidle')
        
        print()
        print("=" * 80)
        print("✋ MANUAL ACTION REQUIRED")
        print("=" * 80)
        print()
        print("Please click the DOWNLOAD button in the browser window.")
        print("I'll monitor the network traffic and show you what happens.")
        print()
        print("Watching for 60 seconds...")
        print()
        
        # Wait for user to click download
        page.wait_for_timeout(60000)
        
        print()
        print("=" * 80)
        print("📊 NETWORK ANALYSIS")
        print("=" * 80)
        print()
        
        # Save all requests to JSON file for offline analysis
        output_file = SCRIPT_DIR / "network_capture.json"
        with open(output_file, 'w') as f:
            json.dump(requests, f, indent=2)
        print(f"💾 Saved {len(requests)} requests to: {output_file}")
        print()
        
        # Show all requests that might be download-related
        download_requests = [r for r in requests if 
                           'download' in r['url'].lower() or 
                           'export' in r['url'].lower() or
                           'csv' in r['url'].lower()]
        
        if download_requests:
            print(f"Found {len(download_requests)} download-related requests:")
            print()
            for i, req in enumerate(download_requests, 1):
                print(f"{i}. {req['method']} {req['url']}")
                if req['post_data'] and req['post_data'] != '<binary data>':
                    print(f"   POST data: {req['post_data'][:200]}")
                print()
        else:
            print("No obvious download requests detected.")
            print()
            print("All requests made:")
            for req in requests[-10:]:  # Show last 10
                print(f"  {req['method']} {req['url']}")
        
        browser.close()

if __name__ == "__main__":
    inspect_download()
