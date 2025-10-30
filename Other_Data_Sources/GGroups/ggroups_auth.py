#!/usr/bin/env python3
"""
Google Groups Authentication Module

Reusable authentication pattern for Google Groups automation.
Follows the browser cookie pattern from /Other_Data_Sources/BROWSER_COOKIE_AUTH_PATTERN.md

Usage:
    from ggroups_auth import authenticate_ggroups
    
    with authenticate_ggroups() as page:
        # page is authenticated and ready to use
        page.goto("https://groups.google.com/g/ecorestoration-alliance/members")
        # ... do your automation ...
"""

import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

# Configuration
SCRIPT_DIR = Path(__file__).parent
COOKIE_FILE = SCRIPT_DIR / "ggroups_cookies.json"

def sanitize_cookies(cookies):
    """
    Fix sameSite values for Playwright compatibility.
    
    Playwright requires sameSite to be one of: 'Strict', 'Lax', 'None'
    Cookie extensions may export 'no_restriction' or null values.
    """
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
    """
    Load and sanitize cookies from ggroups_cookies.json.
    
    Returns:
        list: Sanitized cookies ready for Playwright
        
    Raises:
        SystemExit: If cookie file not found
    """
    if not COOKIE_FILE.exists():
        print(f"❌ Cookie file not found: {COOKIE_FILE}")
        print()
        print("To export cookies:")
        print("1. Open Edge → https://groups.google.com")
        print("2. Use cookie extension to export as JSON")
        print("3. Paste into ggroups_cookies.json")
        print()
        print("Or run: ./refresh_ggroups_auth.sh")
        sys.exit(1)
    
    with open(COOKIE_FILE, 'r') as f:
        cookies = json.load(f)
    
    return sanitize_cookies(cookies)

class GGroupsAuth:
    """
    Context manager for authenticated Google Groups browser sessions.
    
    Usage:
        with GGroupsAuth() as page:
            page.goto("https://groups.google.com/...")
            # ... automation code ...
    """
    
    def __init__(self, headless=False, downloads_path=None):
        """
        Initialize authentication context.
        
        Args:
            headless (bool): Run browser in headless mode (default: False)
            downloads_path (str/Path): Directory for downloads (default: None)
        """
        self.headless = headless
        self.downloads_path = str(downloads_path) if downloads_path else None
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
    
    def __enter__(self):
        """Set up authenticated browser session."""
        # Load cookies
        cookies = load_cookies()
        
        # Launch Playwright
        self.playwright = sync_playwright().start()
        
        # Launch Microsoft Edge (following BROWSER_COOKIE_AUTH_PATTERN.md)
        launch_options = {
            'channel': 'msedge',
            'headless': self.headless
        }
        if self.downloads_path:
            launch_options['downloads_path'] = self.downloads_path
        
        self.browser = self.playwright.chromium.launch(**launch_options)
        
        # Create context with downloads enabled
        context_options = {'accept_downloads': True}
        self.context = self.browser.new_context(**context_options)
        
        # Add cookies
        self.context.add_cookies(cookies)
        
        # Create page
        self.page = self.context.new_page()
        
        return self.page
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up browser session."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

def authenticate_ggroups(headless=False, downloads_path=None):
    """
    Convenience function to create authenticated Google Groups session.
    
    Args:
        headless (bool): Run browser in headless mode (default: False)
        downloads_path (str/Path): Directory for downloads (default: None)
    
    Returns:
        GGroupsAuth: Context manager for authenticated session
        
    Example:
        with authenticate_ggroups() as page:
            page.goto("https://groups.google.com/g/ecorestoration-alliance/members")
            page.screenshot(path="members.png")
    """
    return GGroupsAuth(headless=headless, downloads_path=downloads_path)

def verify_authentication(page, group_name="EcoRestoration Alliance", timeout=5000):
    """
    Verify that the page is authenticated to Google Groups.
    
    Args:
        page: Playwright page object
        group_name (str): Expected group name to verify
        timeout (int): Timeout in milliseconds
        
    Returns:
        bool: True if authenticated, False otherwise
    """
    try:
        return page.locator(f'text={group_name}').first.is_visible(timeout=timeout)
    except:
        return False

if __name__ == "__main__":
    """Test the authentication module."""
    print("=" * 80)
    print("GOOGLE GROUPS AUTHENTICATION TEST")
    print("=" * 80)
    print()
    
    print("🔐 Testing authentication...")
    
    with authenticate_ggroups() as page:
        print("✅ Browser launched with cookies")
        
        # Navigate to members page
        url = "https://groups.google.com/g/ecorestoration-alliance/members"
        print(f"📍 Navigating to: {url}")
        page.goto(url, wait_until='networkidle')
        
        # Verify authentication
        if verify_authentication(page):
            print("✅ Authentication successful!")
            print("   Member list is visible")
        else:
            print("❌ Authentication failed")
            print("   Could not verify member list")
            
            # Take screenshot for debugging
            screenshot_path = SCRIPT_DIR / "auth_test_failed.png"
            page.screenshot(path=str(screenshot_path))
            print(f"   Screenshot saved: {screenshot_path}")
        
        # Wait a moment so you can see the browser
        print()
        print("Browser will close in 3 seconds...")
        page.wait_for_timeout(3000)
    
    print()
    print("✅ Test complete")
