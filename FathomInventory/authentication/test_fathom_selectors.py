#!/usr/bin/env python3
"""
Test Fathom HTML selectors and UI stability.
Based on historical insights from archive documentation.
"""

import os
import json
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

# Historical selectors from archive analysis
FATHOM_SELECTORS = {
    'my_calls_link': 'a:has-text("My Calls")',
    'meeting_cards': 'call-gallery-thumbnail',
    'title_element': 'call-gallery-thumbnail-title',
    'date_element': 'li.opacity-70',
    'duration_element': 'span.font-semibold',
    'link_element': 'a[href]'
}

# Historical timeouts from archive
TIMEOUTS = {
    'page_load': 60000,  # 60 seconds - Fathom can be slow
    'my_calls_wait': 15000,  # 15 seconds - authentication verification
    'element_wait': 10000   # 10 seconds - general element waiting
}

async def test_fathom_selectors():
    """Test that historical Fathom selectors still work."""
    print("🔍 Testing Fathom HTML selectors and UI stability...")
    
    if not os.path.exists('../fathom_cookies.json'):
        print("❌ fathom_cookies.json not found - cannot test selectors")
        return False
    
    try:
        # Load cookies
        with open('../fathom_cookies.json', 'r') as f:
            cookies = json.load(f)
        
        # Sanitize cookies (from current system)
        valid_same_site_values = {'Strict', 'Lax', 'None'}
        for cookie in cookies:
            if cookie.get('sameSite') not in valid_same_site_values:
                cookie['sameSite'] = 'Lax'
            if 'partitionKey' in cookie and not isinstance(cookie.get('partitionKey'), str):
                del cookie['partitionKey']
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            await context.add_cookies(cookies)
            
            page = await context.new_page()
            
            # Test 1: Page load with historical timeout
            print("🌐 Testing Fathom page load (60s timeout)...")
            try:
                await page.goto("https://fathom.video/home", timeout=TIMEOUTS['page_load'])
                print("✅ Page loaded successfully")
            except Exception as e:
                print(f"❌ Page load failed: {e}")
                return False
            
            # Test 2: Authentication verification selector
            print("🔐 Testing authentication verification selector...")
            try:
                await page.wait_for_selector(FATHOM_SELECTORS['my_calls_link'], 
                                           timeout=TIMEOUTS['my_calls_wait'])
                print("✅ 'My Calls' link found - authentication verified")
            except Exception as e:
                print(f"❌ Authentication verification failed: {e}")
                return False
            
            # Test 3: Navigate to My Calls
            print("📞 Testing My Calls navigation...")
            try:
                my_calls_link = await page.query_selector(FATHOM_SELECTORS['my_calls_link'])
                if my_calls_link:
                    await my_calls_link.click()
                    await page.wait_for_load_state('networkidle', timeout=TIMEOUTS['element_wait'])
                    print("✅ Successfully navigated to My Calls")
                else:
                    print("❌ My Calls link not found")
                    return False
            except Exception as e:
                print(f"❌ My Calls navigation failed: {e}")
                return False
            
            # Test 4: Historical meeting card selectors
            print("🎯 Testing historical meeting card selectors...")
            
            # Wait for meeting cards to load
            try:
                await page.wait_for_selector(FATHOM_SELECTORS['meeting_cards'], 
                                           timeout=TIMEOUTS['element_wait'])
                
                meeting_cards = await page.query_selector_all(FATHOM_SELECTORS['meeting_cards'])
                print(f"✅ Found {len(meeting_cards)} meeting cards using historical selector")
                
                if len(meeting_cards) == 0:
                    print("⚠️  No meeting cards found - may indicate UI changes")
                    return False
                
            except Exception as e:
                print(f"❌ Meeting cards selector failed: {e}")
                return False
            
            # Test 5: Individual card element selectors
            print("🔍 Testing individual card element selectors...")
            
            try:
                # Test on first meeting card
                first_card = meeting_cards[0]
                
                # Test title selector
                title_element = await first_card.query_selector(FATHOM_SELECTORS['title_element'])
                if title_element:
                    title_text = await title_element.text_content()
                    print(f"✅ Title selector works: '{title_text[:50]}...'")
                else:
                    print("❌ Title selector failed")
                
                # Test date selector
                date_element = await first_card.query_selector(FATHOM_SELECTORS['date_element'])
                if date_element:
                    date_text = await date_element.text_content()
                    print(f"✅ Date selector works: '{date_text}'")
                else:
                    print("⚠️  Date selector failed - may need updating")
                
                # Test duration selector
                duration_element = await first_card.query_selector(FATHOM_SELECTORS['duration_element'])
                if duration_element:
                    duration_text = await duration_element.text_content()
                    print(f"✅ Duration selector works: '{duration_text}'")
                else:
                    print("⚠️  Duration selector failed - may need updating")
                
                # Test link selector
                link_element = await first_card.query_selector(FATHOM_SELECTORS['link_element'])
                if link_element:
                    href = await link_element.get_attribute('href')
                    print(f"✅ Link selector works: '{href[:50]}...'")
                else:
                    print("❌ Link selector failed")
                
            except Exception as e:
                print(f"❌ Card element testing failed: {e}")
                return False
            
            await browser.close()
            return True
            
    except Exception as e:
        print(f"❌ Selector testing failed: {e}")
        return False

async def test_timeout_scenarios():
    """Test various timeout scenarios based on historical experience."""
    print("\n⏱️  Testing timeout scenarios...")
    
    # Test different timeout values
    timeout_tests = [
        ("Quick timeout (5s)", 5000),
        ("Standard timeout (15s)", 15000),
        ("Historical timeout (60s)", 60000)
    ]
    
    for test_name, timeout_ms in timeout_tests:
        print(f"🕐 Testing {test_name}...")
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                
                start_time = datetime.now()
                await page.goto("https://fathom.video/home", timeout=timeout_ms)
                end_time = datetime.now()
                
                load_time = (end_time - start_time).total_seconds()
                print(f"✅ {test_name} succeeded in {load_time:.1f}s")
                
                await browser.close()
                
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")

async def main():
    """Run comprehensive Fathom selector and timeout tests."""
    print("=" * 60)
    print("🎯 FATHOM SELECTOR & UI STABILITY TEST")
    print("=" * 60)
    print("Testing selectors and patterns from historical archive analysis")
    print()
    
    # Test selectors
    selectors_ok = await test_fathom_selectors()
    
    # Test timeouts
    await test_timeout_scenarios()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SELECTOR TEST SUMMARY")
    print("=" * 60)
    
    if selectors_ok:
        print("✅ Historical selectors are still working")
        print("   Fathom UI appears stable since archive documentation")
        print("   Current system should continue working reliably")
    else:
        print("❌ Some historical selectors have changed")
        print("   Fathom UI may have been updated")
        print("   System may need selector updates")
    
    print("\n📚 Historical Context:")
    print("   These selectors were discovered through manual analysis")
    print("   They have been stable across multiple system iterations")
    print("   See HISTORICAL_INSIGHTS_FROM_ARCHIVE.md for full context")
    
    return selectors_ok

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
