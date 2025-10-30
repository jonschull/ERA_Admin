#!/usr/bin/env python3
"""
Read LinkedIn profiles using Playwright with cookie persistence.

Approach:
1. Opens browser (visible for manual login if needed)
2. Loads LinkedIn cookies if they exist
3. Navigates to each profile URL
4. Extracts relevant content
5. Pauses between profiles to avoid bot detection
6. Saves cookies for next session
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# Paths
SCRIPT_DIR = Path(__file__).parent
COOKIES_FILE = SCRIPT_DIR / "linkedin_cookies.json"
OUTPUT_DIR = SCRIPT_DIR / "profiles"


def sanitize_cookies(cookies):
    """Sanitize cookies for Playwright (from Fathom pattern)."""
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


async def extract_profile_content(page):
    """Extract relevant content from LinkedIn profile page."""
    
    # Wait for profile to load
    try:
        await page.wait_for_selector('main', timeout=10000)
    except:
        print("  ⚠️  Profile may not have loaded completely")
    
    # Scroll down to ensure all content loads
    await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
    await page.wait_for_timeout(2000)
    
    # Get the HTML
    html = await page.content()
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract key sections
    profile_data = {
        'url': page.url,
        'raw_html': html,
        'extracted': {}
    }
    
    # Name - try multiple selectors
    name_selectors = [
        'h1.text-heading-xlarge',
        'h1',
        'div[class*="top-card"] h1'
    ]
    for selector in name_selectors:
        elems = soup.select(selector)
        for elem in elems:
            text = elem.get_text(strip=True)
            if text and len(text) < 100 and len(text) > 2:  # Reasonable name length
                profile_data['extracted']['name'] = text
                break
        if 'name' in profile_data['extracted']:
            break
    
    # Headline - look for subtitle/description near name
    headline_selectors = [
        'div.text-body-medium',
        'div[class*="headline"]',
        'div.pv-text-details__left-panel div.text-body-medium'
    ]
    for selector in headline_selectors:
        elems = soup.select(selector)
        for elem in elems:
            text = elem.get_text(strip=True)
            if text and len(text) > 10 and len(text) < 300:
                profile_data['extracted']['headline'] = text
                break
        if 'headline' in profile_data['extracted']:
            break
    
    # Try to extract ALL visible text from main sections
    # This is a fallback - get everything and let human parse
    main_elem = soup.find('main')
    if main_elem:
        # Get all text, preserving some structure
        all_text_parts = []
        
        # Look for section headers and content
        for section in main_elem.find_all(['section', 'div'], class_=lambda x: x and ('pv-' in x or 'profile' in x)):
            section_text = section.get_text(separator='\n', strip=True)
            if section_text and len(section_text) > 50:
                all_text_parts.append(section_text)
        
        profile_data['extracted']['full_text'] = '\n\n---\n\n'.join(all_text_parts[:20])  # First 20 sections
    
    return profile_data


async def read_profiles(profile_urls, pause_seconds=5):
    """
    Read multiple LinkedIn profiles.
    
    Args:
        profile_urls: List of LinkedIn profile URLs
        pause_seconds: Seconds to pause between profiles (avoid bot detection)
    """
    
    print("=" * 80)
    print("LinkedIn Profile Reader")
    print("=" * 80)
    print()
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    
    async with async_playwright() as p:
        # Launch Edge (following Fathom pattern)
        print("🌐 Launching Microsoft Edge...")
        browser = await p.chromium.launch(
            headless=False,
            channel='msedge'  # Use Microsoft Edge
        )
        context = await browser.new_context()
        
        # Load cookies if they exist (following Fathom pattern)
        if COOKIES_FILE.exists():
            print(f"🍪 Loading cookies from {COOKIES_FILE}")
            with open(COOKIES_FILE, 'r') as f:
                cookies = json.load(f)
            cookies = sanitize_cookies(cookies)
            await context.add_cookies(cookies)
            print("   Cookies loaded")
        else:
            print(f"⚠️  No cookies found at {COOKIES_FILE}")
            print("   First run: You'll need to export cookies from Edge")
            print("   See: cookie_export_guide_linkedin.md")
        
        page = await context.new_page()
        
        # Process each profile
        results = []
        for i, url in enumerate(profile_urls, 1):
            print()
            print(f"📄 Profile {i}/{len(profile_urls)}: {url}")
            print("-" * 80)
            
            try:
                # Navigate to profile
                print("   Loading profile...")
                await page.goto(url, timeout=30000)
                
                # Check if LinkedIn requires login
                current_url = page.url
                if 'login' in current_url or 'checkpoint' in current_url or 'authwall' in current_url:
                    print()
                    print("🔐 LinkedIn requires login!")
                    print("   Please login manually in the Edge browser window.")
                    print("   After logging in, navigate back to the profile.")
                    print("   Press ENTER here when you're ready to continue...")
                    input()
                    
                    # Try navigating to profile again after login
                    await page.goto(url, timeout=30000)
                    current_url = page.url
                    
                    if 'login' in current_url or 'checkpoint' in current_url:
                        print("   ❌ Still not authenticated. Skipping this profile...")
                        results.append({'url': url, 'error': 'Authentication failed'})
                        continue
                
                # Wait a bit for dynamic content
                await page.wait_for_timeout(2000)
                
                # Extract content
                print("   Extracting content...")
                profile_data = await extract_profile_content(page)
                
                # Save to file
                filename = url.split('/')[-1].replace('?', '_') + '.json'
                output_path = OUTPUT_DIR / filename
                with open(output_path, 'w') as f:
                    json.dump(profile_data, f, indent=2)
                
                print(f"   ✅ Saved to: {output_path}")
                
                # Show extracted summary
                if profile_data['extracted'].get('name'):
                    print(f"   Name: {profile_data['extracted']['name']}")
                if profile_data['extracted'].get('headline'):
                    headline = profile_data['extracted']['headline'][:80]
                    print(f"   Headline: {headline}...")
                
                results.append(profile_data)
                
                # Pause before next profile (avoid bot detection)
                if i < len(profile_urls):
                    print(f"   ⏸️  Pausing {pause_seconds} seconds before next profile...")
                    await page.wait_for_timeout(pause_seconds * 1000)
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                results.append({'url': url, 'error': str(e)})
        
        # Save cookies for next session (following Fathom pattern)
        print()
        print("💾 Saving cookies for next session...")
        cookies = await context.cookies()
        with open(COOKIES_FILE, 'w') as f:
            json.dump(cookies, f, indent=2)
        print(f"   Saved to: {COOKIES_FILE}")
        
        print()
        print("=" * 80)
        print(f"✅ Completed: {len(results)} profiles processed")
        print("=" * 80)
        print()
        print("📂 Profile data saved in:", OUTPUT_DIR)
        print()
        
        # Keep browser open for review
        print("Browser will stay open for 10 seconds for review...")
        await page.wait_for_timeout(10000)
        
        await browser.close()
        
        return results


def main():
    """Run with profile URLs from command line or default test set."""
    
    if len(sys.argv) > 1:
        # URLs provided as command line arguments
        profile_urls = sys.argv[1:]
    else:
        # Default: Batch 2 members
        profile_urls = [
            'https://www.linkedin.com/in/bwrubin',
            'https://www.linkedin.com/in/noura-angulo-925992232',
            'https://www.linkedin.com/in/bill-reed-340aa42'
        ]
        print("No URLs provided, using Batch 2 members:")
        for url in profile_urls:
            print(f"  - {url}")
        print()
    
    asyncio.run(read_profiles(profile_urls, pause_seconds=5))


if __name__ == '__main__':
    main()
