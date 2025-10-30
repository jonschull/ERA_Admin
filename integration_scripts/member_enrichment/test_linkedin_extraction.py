#!/usr/bin/env python3
"""
LinkedIn Extraction Diagnostic - Test what's actually on the page

This script will:
1. Load ONE profile
2. Save a screenshot
3. Dump the HTML to a file
4. Try multiple extraction strategies
5. Show what selectors work
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
COOKIES_FILE = SCRIPT_DIR / "linkedin_cookies.json"
OUTPUT_DIR = SCRIPT_DIR / "test_output"

# Test with just ONE profile
TEST_URL = "https://www.linkedin.com/in/pennyheiple"


def sanitize_cookies(cookies):
    """Sanitize cookies for Playwright."""
    valid_same_site_values = {'Strict', 'Lax', 'None'}
    sanitized = []
    for cookie in cookies:
        c = dict(cookie)
        if c.get('sameSite') not in valid_same_site_values:
            c['sameSite'] = 'Lax'
        if 'partitionKey' in c and not isinstance(c.get('partitionKey'), str):
            del c['partitionKey']
        sanitized.append(c)
    return sanitized


async def diagnostic_extraction(page):
    """Try multiple extraction strategies and report what works."""
    
    print("\n" + "="*80)
    print("DIAGNOSTIC: Testing extraction strategies")
    print("="*80)
    
    results = {}
    
    # Strategy 1: Original selectors
    print("\n1. Testing original selectors...")
    try:
        name_elem = await page.query_selector('h1')
        if name_elem:
            name = await name_elem.inner_text()
            print(f"   h1 found: '{name}'")
            results['h1'] = name
        else:
            print("   h1 NOT FOUND")
    except Exception as e:
        print(f"   h1 error: {e}")
    
    try:
        headline_elem = await page.query_selector('.text-body-medium')
        if headline_elem:
            headline = await headline_elem.inner_text()
            print(f"   .text-body-medium found: '{headline[:100]}'")
            results['text-body-medium'] = headline
        else:
            print("   .text-body-medium NOT FOUND")
    except Exception as e:
        print(f"   .text-body-medium error: {e}")
    
    # Strategy 2: Try ALL h1 elements
    print("\n2. Finding ALL h1 elements...")
    try:
        h1_elems = await page.query_selector_all('h1')
        print(f"   Found {len(h1_elems)} h1 elements")
        for i, elem in enumerate(h1_elems[:5], 1):  # First 5
            text = await elem.inner_text()
            print(f"   h1[{i}]: '{text[:100]}'")
            if i == 1:
                results['first_h1'] = text
    except Exception as e:
        print(f"   Error: {e}")
    
    # Strategy 3: Look for common LinkedIn class patterns
    print("\n3. Testing LinkedIn-specific classes...")
    selectors_to_try = [
        ('text-heading-xlarge', 'Name (xlarge)'),
        ('pv-text-details__left-panel', 'Profile details'),
        ('text-body-medium', 'Body medium'),
        ('[data-field="headline"]', 'Headline data field'),
        ('div.ph5', 'Main content area'),
    ]
    
    for selector, description in selectors_to_try:
        try:
            elem = await page.query_selector(selector)
            if elem:
                text = await elem.inner_text()
                print(f"   ✓ {description} ({selector}): '{text[:80]}'")
                results[selector] = text[:200]
            else:
                print(f"   ✗ {description} ({selector}): NOT FOUND")
        except Exception as e:
            print(f"   ✗ {description} ({selector}): Error - {e}")
    
    # Strategy 4: Get ALL text from main element
    print("\n4. Extracting full main text...")
    try:
        main_elem = await page.query_selector('main')
        if main_elem:
            full_text = await main_elem.inner_text()
            print(f"   Main element text length: {len(full_text)} characters")
            print(f"   First 300 chars:\n{full_text[:300]}")
            results['main_full_text'] = full_text[:500]
        else:
            print("   main element NOT FOUND")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Strategy 5: Check for auth wall
    print("\n5. Checking for authentication issues...")
    url = page.url
    if 'authwall' in url or 'login' in url or 'checkpoint' in url:
        print(f"   ⚠️  AUTH WALL DETECTED: {url}")
        results['auth_issue'] = True
    else:
        print(f"   ✓ No auth wall detected")
        results['auth_issue'] = False
    
    return results


async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("="*80)
    print("LinkedIn Extraction Diagnostic Test")
    print("="*80)
    print(f"\nTest URL: {TEST_URL}")
    print()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            channel="msedge"
        )
        
        context = await browser.new_context()
        
        # Load cookies
        if COOKIES_FILE.exists():
            with open(COOKIES_FILE) as f:
                cookies = json.load(f)
                await context.add_cookies(sanitize_cookies(cookies))
                print("✅ Loaded cookies\n")
        else:
            print("⚠️  No cookies file found\n")
        
        page = await context.new_page()
        
        print("Loading profile...")
        try:
            await page.goto(TEST_URL, wait_until='networkidle', timeout=15000)
        except:
            try:
                await page.goto(TEST_URL, wait_until='domcontentloaded', timeout=10000)
            except:
                print("⚠️  Navigation timeout")
        
        # Wait for page to render
        await asyncio.sleep(3)
        
        # Save screenshot
        screenshot_path = OUTPUT_DIR / "profile_screenshot.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"\n📸 Screenshot saved: {screenshot_path}")
        
        # Save HTML
        html = await page.content()
        html_path = OUTPUT_DIR / "profile_page.html"
        with open(html_path, 'w') as f:
            f.write(html)
        print(f"📄 HTML saved: {html_path}")
        
        # Run diagnostic extraction
        results = await diagnostic_extraction(page)
        
        # Save results
        results_path = OUTPUT_DIR / "extraction_results.json"
        with open(results_path, 'w') as f:
            json.dump({
                'url': TEST_URL,
                'timestamp': datetime.now().isoformat(),
                'results': results
            }, f, indent=2)
        print(f"\n💾 Results saved: {results_path}")
        
        print("\n" + "="*80)
        print("Diagnostic complete!")
        print("="*80)
        print(f"\nReview files in: {OUTPUT_DIR}")
        print("\nBrowser will stay open for 30 seconds for manual inspection...")
        
        await asyncio.sleep(30)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
