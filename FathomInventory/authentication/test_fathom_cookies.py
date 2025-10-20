#!/usr/bin/env python3
"""
Test Fathom.video cookie authentication system.
Verifies cookie file validity, expiration status, and Fathom access.
"""

import os
import json
import asyncio
from datetime import datetime, timezone
from playwright.async_api import async_playwright

def check_cookies_file():
    """Check if fathom_cookies.json exists and analyze its contents."""
    print("🔍 Checking fathom_cookies.json...")
    
    if not os.path.exists('../fathom_cookies.json'):
        print("❌ fathom_cookies.json not found")
        return False, None
    
    try:
        with open('../fathom_cookies.json', 'r') as f:
            cookies = json.load(f)
        
        if not isinstance(cookies, list):
            print("❌ fathom_cookies.json should contain an array of cookies")
            return False, None
        
        print(f"✅ fathom_cookies.json found with {len(cookies)} cookies")
        
        # Analyze cookie expiration
        now = datetime.now(timezone.utc).timestamp()
        expired_count = 0
        expiring_soon_count = 0
        session_count = 0
        
        for cookie in cookies:
            if 'expirationDate' not in cookie:
                session_count += 1
            else:
                exp_date = cookie['expirationDate']
                if exp_date < now:
                    expired_count += 1
                elif exp_date < now + (7 * 24 * 3600):  # Expiring in 7 days
                    expiring_soon_count += 1
        
        print(f"   📊 Cookie status:")
        print(f"      - Total cookies: {len(cookies)}")
        print(f"      - Session cookies: {session_count}")
        print(f"      - Expired cookies: {expired_count}")
        print(f"      - Expiring soon (7 days): {expiring_soon_count}")
        
        if expired_count > len(cookies) * 0.5:
            print("⚠️  More than 50% of cookies are expired")
            return True, cookies  # Still return cookies for testing
        elif expired_count > 0:
            print(f"⚠️  {expired_count} cookies are expired")
        else:
            print("✅ All cookies are current")
        
        return True, cookies
        
    except json.JSONDecodeError:
        print("❌ fathom_cookies.json is not valid JSON")
        return False, None
    except Exception as e:
        print(f"❌ Error reading fathom_cookies.json: {e}")
        return False, None

def sanitize_cookies(cookies):
    """Sanitize cookies for Playwright compatibility."""
    print("🧹 Sanitizing cookies for Playwright...")
    
    valid_same_site_values = {'Strict', 'Lax', 'None'}
    sanitized_count = 0
    
    for cookie in cookies:
        original_same_site = cookie.get('sameSite')
        
        # Fix sameSite values
        if cookie.get('sameSite') not in valid_same_site_values:
            cookie['sameSite'] = 'Lax'
            sanitized_count += 1
        
        # Remove problematic partitionKey
        if 'partitionKey' in cookie and not isinstance(cookie.get('partitionKey'), str):
            del cookie['partitionKey']
            sanitized_count += 1
    
    if sanitized_count > 0:
        print(f"🔧 Sanitized {sanitized_count} cookie attributes")
    else:
        print("✅ No cookie sanitization needed")
    
    return cookies

async def test_fathom_access(cookies):
    """Test Fathom.video access using cookies."""
    print("\n🌐 Testing Fathom.video access...")
    
    try:
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            
            # Add cookies to context
            sanitized_cookies = sanitize_cookies(cookies.copy())
            await context.add_cookies(sanitized_cookies)
            
            # Create page and navigate
            page = await context.new_page()
            print("🔄 Navigating to Fathom home page...")
            
            try:
                await page.goto("https://fathom.video/home", timeout=30000)
                await page.wait_for_load_state('networkidle', timeout=15000)
                
                # Check if we're logged in
                title = await page.title()
                print(f"📄 Page title: {title}")
                
                # Look for login indicators
                login_button = await page.query_selector('a[href*="login"], button:has-text("Sign in"), button:has-text("Log in")')
                if login_button:
                    print("❌ Redirected to login page - cookies may be expired")
                    return False
                
                # Look for authenticated user indicators
                user_menu = await page.query_selector('[data-testid="user-menu"], .user-menu, [aria-label*="user"], [aria-label*="account"]')
                my_calls_link = await page.query_selector('a:has-text("My Calls"), [href*="calls"]')
                
                if user_menu or my_calls_link:
                    print("✅ Successfully authenticated with Fathom")
                    
                    # Try to access My Calls page
                    if my_calls_link:
                        print("🔄 Testing My Calls page access...")
                        await my_calls_link.click()
                        await page.wait_for_load_state('networkidle', timeout=15000)
                        
                        # Look for call thumbnails
                        thumbnails = await page.query_selector_all('call-gallery-thumbnail, .call-thumbnail, [data-testid*="call"]')
                        print(f"📹 Found {len(thumbnails)} call thumbnails")
                        
                        if len(thumbnails) > 0:
                            print("✅ My Calls page access successful")
                            return True
                        else:
                            print("⚠️  My Calls page loaded but no calls found")
                            return True
                    else:
                        print("✅ Authenticated but My Calls link not found")
                        return True
                else:
                    print("❌ Could not verify authentication status")
                    return False
                
            except Exception as nav_error:
                print(f"❌ Navigation error: {nav_error}")
                return False
            
            finally:
                await browser.close()
                
    except Exception as e:
        print(f"❌ Browser test error: {e}")
        return False

async def main():
    """Run comprehensive Fathom cookie tests."""
    print("=" * 60)
    print("🍪 FATHOM COOKIE AUTHENTICATION TEST")
    print("=" * 60)
    
    # Test cookies file
    cookies_ok, cookies = check_cookies_file()
    
    # Test actual Fathom access
    if cookies_ok and cookies:
        access_ok = await test_fathom_access(cookies)
    else:
        print("\n❌ Cannot test Fathom access without valid cookies")
        access_ok = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FATHOM AUTHENTICATION TEST SUMMARY")
    print("=" * 60)
    print(f"Cookie file: {'✅ OK' if cookies_ok else '❌ FAIL'}")
    print(f"Fathom access: {'✅ OK' if access_ok else '❌ FAIL'}")
    
    if cookies_ok and access_ok:
        print("\n🎉 Fathom cookie authentication is fully functional!")
    else:
        print("\n⚠️  Fathom cookie authentication needs attention.")
        print("\nNext steps:")
        if not cookies_ok:
            print("1. Log into Fathom.video manually in browser")
            print("2. Export cookies using browser developer tools")
            print("3. Save cookies as fathom_cookies.json")
        elif not access_ok:
            print("1. Cookies may be expired - refresh from browser")
            print("2. Check if Fathom.video site structure has changed")

if __name__ == "__main__":
    asyncio.run(main())
