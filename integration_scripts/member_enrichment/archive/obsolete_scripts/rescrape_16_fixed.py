#!/usr/bin/env python3
"""
Re-scrape the 16 profiles with fixed filename generation.
"""

import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright

# Paths
SCRIPT_DIR = Path(__file__).parent
COOKIES_FILE = SCRIPT_DIR / "linkedin_cookies.json"
OUTPUT_DIR = SCRIPT_DIR / "batches" / "linkedin_profiles"

URLs = [
    "https://www.linkedin.com/in/frank-van-schoubroeck-9524518/",
    "https://www.linkedin.com/in/abigail-karparis-57b940107/",
    "https://www.linkedin.com/in/abigail-castle-198928264/",
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
    "https://www.linkedin.com/in/michael-levin-b0983a6/",
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
    # Remove trailing slash
    url = url.rstrip('/')
    # Get last part
    parts = url.split('/')
    filename = parts[-1]
    # Clean up
    filename = filename.replace('?', '_')
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


async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Re-scraping 16 profiles with fixed filenames...")
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
        
        for i, url in enumerate(URLs, 1):
            print(f"\n[{i}/16] {url}")
            
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
                
                print(f"✅ Saved: {filename}")
                
                if data['extracted']['name']:
                    print(f"   Name: {data['extracted']['name']}")
                if data['extracted']['headline']:
                    print(f"   Headline: {data['extracted']['headline'][:80]}")
                
                # Pause between profiles
                if i < len(URLs):
                    await asyncio.sleep(5)
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        # Save cookies
        cookies = await context.cookies()
        with open(COOKIES_FILE, 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print("\n✅ Complete!")
        await asyncio.sleep(10)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
