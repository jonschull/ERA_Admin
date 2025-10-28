#!/usr/bin/env python3
"""
Scrape LinkedIn profiles for 24 members with URLs but no bio drafts
Rate limited: 10-15 seconds between requests
"""

import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
COOKIES_FILE = SCRIPT_DIR / "linkedin_cookies.json"
OUTPUT_DIR = SCRIPT_DIR / "batches" / "linkedin_profiles"
URLS_FILE = SCRIPT_DIR / "linkedin_urls_to_scrape.txt"

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
    filename = parts[-1]
    filename = filename.replace('?', '_')
    # Handle URL-encoded characters
    filename = filename.replace('%F0%9F%8C%8E', 'emoji')
    filename = filename.replace('%F0%9F%95%8A', 'emoji')
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
        'scraped_at': datetime.now().isoformat(),
        'extracted': {
            'name': name,
            'headline': headline,
            'full_text': full_text
        }
    }


async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Read URLs to scrape
    urls_to_scrape = []
    with open(URLS_FILE) as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    member_name, url = parts
                    urls_to_scrape.append((member_name, url))
    
    print(f"Scraping {len(urls_to_scrape)} LinkedIn profiles...")
    print(f"Rate limit: 10-15 seconds between requests")
    print(f"Estimated time: {len(urls_to_scrape) * 12 / 60:.0f} minutes\n")
    
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
        
        page = await context.new_page()
        
        success_count = 0
        error_count = 0
        
        for i, (member_name, url) in enumerate(urls_to_scrape, 1):
            print(f"[{i}/{len(urls_to_scrape)}] {member_name}")
            print(f"   {url}")
            
            try:
                await page.goto(url, wait_until='networkidle', timeout=30000)
                await asyncio.sleep(2)
                
                # Extract content
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
                    headline = data['extracted']['headline'][:80]
                    print(f"   Headline: {headline}...")
                
                success_count += 1
                
                # Rate limiting: 10-15 seconds between profiles
                if i < len(urls_to_scrape):
                    import random
                    delay = random.uniform(10, 15)
                    print(f"   ⏳ Waiting {delay:.1f}s...\n")
                    await asyncio.sleep(delay)
                
            except Exception as e:
                print(f"   ❌ Error: {e}\n")
                error_count += 1
                # Wait even on error to avoid rate limiting
                if i < len(urls_to_scrape):
                    await asyncio.sleep(10)
        
        # Save cookies
        cookies = await context.cookies()
        with open(COOKIES_FILE, 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print("\n" + "="*80)
        print(f"✅ Scraping Complete!")
        print(f"   Success: {success_count}/{len(urls_to_scrape)}")
        print(f"   Errors: {error_count}/{len(urls_to_scrape)}")
        print(f"   Output: {OUTPUT_DIR}")
        print("="*80)
        
        await asyncio.sleep(5)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
