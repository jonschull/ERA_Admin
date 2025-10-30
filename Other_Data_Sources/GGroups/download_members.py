#!/usr/bin/env python3
"""
Download Google Groups member list using browser automation.

Based on: /Other_Data_Sources/BROWSER_COOKIE_AUTH_PATTERN.md

This script:
1. Loads Google cookies from ggroups_cookies.json
2. Navigates to Google Groups
3. Clicks through to download CSV
4. Saves member list

Usage:
    python download_members.py
    
Prerequisites:
    1. Export cookies: ./refresh_ggroups_auth.sh
    2. Install playwright: pip install playwright && playwright install chromium
"""

import json
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from datetime import datetime

# Configuration
SCRIPT_DIR = Path(__file__).parent
COOKIE_FILE = SCRIPT_DIR / "ggroups_cookies.json"
GROUP_URL = "https://groups.google.com/g/ecorestoration-alliance/members"
DOWNLOAD_DIR = SCRIPT_DIR / "downloads"
OUTPUT_FILE = SCRIPT_DIR / f"members_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

def sanitize_cookies(cookies):
    """Fix sameSite values for Playwright compatibility."""
    valid_same_site_values = {'Strict', 'Lax', 'None'}
    
    for cookie in cookies:
        # Fix sameSite values
        if cookie.get('sameSite') not in valid_same_site_values:
            cookie['sameSite'] = 'Lax'
        
        # Remove problematic partitionKey
        if 'partitionKey' in cookie and not isinstance(cookie.get('partitionKey'), str):
            del cookie['partitionKey']
    
    return cookies

def load_cookies():
    """Load and sanitize cookies from file."""
    if not COOKIE_FILE.exists():
        print(f"❌ Cookie file not found: {COOKIE_FILE}")
        print("   Run: ./refresh_ggroups_auth.sh")
        sys.exit(1)
    
    with open(COOKIE_FILE, 'r') as f:
        cookies = json.load(f)
    
    return sanitize_cookies(cookies)

def download_members():
    """Download Google Groups member list."""
    print("=" * 80)
    print("GOOGLE GROUPS MEMBER DOWNLOAD")
    print("=" * 80)
    print()
    
    # Load cookies
    print("🔐 Loading cookies...")
    cookies = load_cookies()
    print(f"   Loaded {len(cookies)} cookies")
    print()
    
    # Create download directory
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        print("🌐 Launching Microsoft Edge...")
        # Use Edge (following BROWSER_COOKIE_AUTH_PATTERN.md)
        browser = p.chromium.launch(
            channel="msedge",  # Use Microsoft Edge
            headless=False,  # Visible so you can see what's happening
            downloads_path=str(DOWNLOAD_DIR)
        )
        
        context = browser.new_context(
            accept_downloads=True
        )
        
        # Add cookies
        print("🍪 Adding cookies to browser...")
        context.add_cookies(cookies)
        
        page = context.new_page()
        
        try:
            # Navigate to group members page
            print(f"📍 Navigating to: {GROUP_URL}")
            page.goto(GROUP_URL, wait_until='networkidle', timeout=60000)
            
            # Wait a moment for page to settle
            page.wait_for_timeout(2000)
            
            # Check if we're authenticated
            print("🔍 Checking authentication...")
            
            # Check if we see the member list (confirms authentication)
            if page.locator('text=EcoRestoration Alliance').first.is_visible(timeout=5000):
                print("✅ Authenticated - member list visible")
            else:
                print("❌ Authentication failed - not on members page")
                screenshot_path = SCRIPT_DIR / "auth_failed.png"
                page.screenshot(path=str(screenshot_path))
                print(f"   Screenshot saved: {screenshot_path}")
                sys.exit(1)
            
            # Find the download button - it's the download icon next to "Add members"
            # The icon is in a button with a download SVG
            download_button = None
            selectors = [
                # Try finding by the download icon SVG path
                'button:has(svg path[d*="M19 9h-4V3H9v6H5l7 7 7-7"])',  # Material download icon
                'button[aria-label*="Download"]',
                'button[aria-label*="download"]',
                # Try finding near "Add members" button
                'text=Add members >> xpath=following-sibling::button[1]',
                # Generic icon button selectors
                'button[jsname]:has(svg)',
            ]
            
            for selector in selectors:
                try:
                    btn = page.locator(selector).first
                    if btn.is_visible(timeout=2000):
                        download_button = btn
                        print(f"✅ Found download button")
                        break
                except:
                    continue
            
            if not download_button:
                print("⚠️  Could not find download button automatically")
                print("   Taking screenshot - you may need to click manually")
                screenshot_path = SCRIPT_DIR / "need_manual_click.png"
                page.screenshot(path=str(screenshot_path))
                print(f"   Screenshot: {screenshot_path}")
                print("\n   Waiting 30 seconds for manual download...")
                page.wait_for_timeout(30000)
                sys.exit(0)
            
            # Click download button
            print("📥 Clicking download button...")
            
            # Wait for download to start
            with page.expect_download() as download_info:
                download_button.click()
            
            download = download_info.value
            
            # Save the download
            print(f"💾 Saving to: {OUTPUT_FILE}")
            download.save_as(OUTPUT_FILE)
            
            print()
            print("=" * 80)
            print("✅ SUCCESS")
            print("=" * 80)
            print(f"Member list saved: {OUTPUT_FILE}")
            print()
            
            # Quick preview
            if OUTPUT_FILE.exists():
                with open(OUTPUT_FILE, 'r') as f:
                    lines = f.readlines()
                    print(f"Downloaded {len(lines)} lines")
                    if len(lines) > 1:
                        print("\nFirst few lines:")
                        for line in lines[:5]:
                            print(f"  {line.strip()}")
            
        except PlaywrightTimeout as e:
            print(f"❌ Timeout error: {e}")
            screenshot_path = SCRIPT_DIR / "timeout_error.png"
            page.screenshot(path=str(screenshot_path))
            print(f"   Screenshot saved: {screenshot_path}")
            sys.exit(1)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            screenshot_path = SCRIPT_DIR / "error.png"
            page.screenshot(path=str(screenshot_path))
            print(f"   Screenshot saved: {screenshot_path}")
            sys.exit(1)
            
        finally:
            browser.close()

if __name__ == "__main__":
    download_members()
