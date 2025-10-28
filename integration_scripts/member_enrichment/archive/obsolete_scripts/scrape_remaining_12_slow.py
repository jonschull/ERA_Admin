#!/usr/bin/env python3
"""
Scrape remaining 12 LinkedIn profiles with rate-limit avoidance strategies:
- Longer pauses (10-15 seconds, randomized)
- Navigate to LinkedIn home between profiles
- Smaller batch (do 6 at a time, take a break)
"""

import asyncio
import json
import random
from pathlib import Path
from playwright.async_api import async_playwright

# Paths
SCRIPT_DIR = Path(__file__).parent
COOKIES_FILE = SCRIPT_DIR / "linkedin_cookies.json"
OUTPUT_DIR = SCRIPT_DIR / "batches" / "linkedin_profiles"

# The 12 URLs
URLS = [
    "https://www.linkedin.com/in/alexahk-4b493r/",
    "https://www.linkedin.com/in/alfredo-quarto-26a4b718/",
    "https://www.linkedin.com/in/allisoncywu/",
    "https://www.linkedin.com/in/cory-albers-85417660/",
    "https://www.linkedin.com/in/fred-hornaday-3907377/",
    "https://www.linkedin.com/in/george-orbelian-4701597/",
    "https://www.linkedin.com/in/joshuakonkankoh/",
    "https://www.linkedin.com/in/ilarion-larry-merculieff-15b6429/",
    "https://www.linkedin.com/in/pete-corke-82063a3/",
    "https://www.linkedin.com/in/kriss-scioneaux-5b3645325/",
    "https://www.linkedin.com/in/larry-kopald-b076167/",
    "https://www.linkedin.com/in/matthewhotsko/",
]


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


def get_filename_from_url(url):
    """Extract proper filename from LinkedIn URL."""
    url = url.rstrip('/')
    parts = url.split('/')
    filename = parts[-1].replace('?', '_')
    return filename + '.json'


async def extract_profile_content(page):
    """Extract content from LinkedIn profile page."""
    try:
        await page.wait_for_selector('main', timeout=10000)
    except:
        pass
    
    # Get all text content
    full_text = await page.inner_text('body')
    
    # Try to extract name and headline
    name = None
    headline = None
    
    try:
        name_elem = await page.query_selector('h1')
        if name_elem:
            name = await name_elem.inner_text()
    except:
        pass
    
    try:
        headline_elem = await page.query_selector('.text-body-medium')
        if headline_elem:
            headline = await headline_elem.inner_text()
    except:
        pass
    
    return {
        'url': page.url,
        'extracted': {
            'name': name,
            'headline': headline,
            'full_text': full_text
        }
    }


async def navigate_to_linkedin_home(page):
    """Navigate to LinkedIn homepage to appear more human-like."""
    try:
        await page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(random.uniform(2, 4))
    except:
        pass


async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("Rate-Limit-Friendly LinkedIn Scraper")
    print("=" * 80)
    print()
    print("Strategy:")
    print("- 10-15 second pauses (randomized)")
    print("- Navigate to LinkedIn home between profiles")
    print("- Process all 12 profiles with breaks every 4")
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
                print("✅ Loaded cookies")
        
        page = await context.new_page()
        
        # Navigate to LinkedIn first
        print("🌐 Navigating to LinkedIn...")
        await page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=30000)
        await asyncio.sleep(3)
        
        for i, url in enumerate(URLS, 1):
            print(f"\n{'='*80}")
            print(f"[{i}/12] {url}")
            print(f"{'='*80}")
            
            try:
                # Navigate to profile
                print("   Loading profile...")
                await page.goto(url, wait_until='domcontentloaded', timeout=30000)
                
                # Wait for content
                await asyncio.sleep(3)
                
                # Extract content
                print("   Extracting content...")
                data = await extract_profile_content(page)
                
                # Save with proper filename
                filename = get_filename_from_url(url)
                output_path = OUTPUT_DIR / filename
                
                with open(output_path, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"   ✅ Saved: {filename}")
                
                if data['extracted']['name']:
                    print(f"   Name: {data['extracted']['name']}")
                if data['extracted']['headline']:
                    print(f"   Headline: {data['extracted']['headline'][:80]}")
                
                # Rate limit avoidance strategies
                if i < len(URLS):
                    # Every 4 profiles, take a longer break and visit home
                    if i % 4 == 0:
                        print(f"\n   ⏸️  Taking break after {i} profiles...")
                        await navigate_to_linkedin_home(page)
                        pause = random.uniform(20, 30)
                        print(f"   Pausing {pause:.1f} seconds...")
                        await asyncio.sleep(pause)
                    else:
                        # Regular pause
                        pause = random.uniform(10, 15)
                        print(f"   ⏸️  Pausing {pause:.1f} seconds before next profile...")
                        await asyncio.sleep(pause)
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                # On error, take a longer break
                print(f"   Taking 30 second break after error...")
                await asyncio.sleep(30)
        
        # Save cookies
        print(f"\n💾 Saving cookies for next session...")
        cookies = await context.cookies()
        with open(COOKIES_FILE, 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print(f"\n{'='*80}")
        print("✅ Complete!")
        print(f"{'='*80}")
        
        await asyncio.sleep(10)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
