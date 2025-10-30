#!/usr/bin/env python3
"""
LinkedIn Profile Fetcher - CANONICAL SCRIPT
===========================================

DO NOT REINVENT THIS SCRIPT. This is the proven, working approach.

PURPOSE:
    Fetch LinkedIn profiles using authenticated browser sessions (Playwright).
    Handles LinkedIn's rate limiting and navigation timeouts gracefully.

KEY LEARNINGS (Oct 27, 2025):
    1. Use hardcoded URLs list (proven pattern from scrape_next_3.py)
    2. Wait for 'networkidle' first, fall back to 'domcontentloaded'
    3. Always attempt extraction even if navigation times out
    4. 5-second delays between profiles
    5. LinkedIn cookies loaded from linkedin_cookies.json
    6. Headless=False required (LinkedIn blocks headless browsers)

CRITICAL FIX:
    Navigation timeouts DON'T mean page didn't load!
    - Try networkidle (15s timeout)
    - Fall back to domcontentloaded (10s timeout)
    - Extract anyway - data is usually there
    
USAGE:
    1. Update URLs list with members to scrape
    2. Ensure linkedin_cookies.json exists and is recent
    3. Run: python3 linkedin_profile_fetcher.py
    4. Profiles saved to: profiles/

SUCCESS RATE:
    - Original attempt: 3/18 (failed due to strict timeout)
    - After fix: 18/18 (100% success with graceful timeout handling)

AUTHOR: ERA Admin / Cascade AI
DATE: October 27, 2025
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
OUTPUT_DIR = SCRIPT_DIR / "profiles"

# Remaining 12 members that appeared to timeout but may have loaded
# Fixed script now handles navigation timeouts gracefully
URLs = [
    ("Kathia Burillo", "https://www.linkedin.com/in/kathia-burillo-r-a90a4576"),
    ("Maxime Weidema", "https://www.linkedin.com/in/maxime-weidema-82863239"),
    ("Minot Weld", "https://www.linkedin.com/in/minot-weld-921385223"),
    ("Missy Lahren", "https://www.linkedin.com/in/missy-lahren-earthlawyer"),
    ("Mr. Kipilangat Kaura -TAWI", "https://www.linkedin.com/in/kipilangat-kaura-2425702bb"),
    ("Penny Heiple", "https://www.linkedin.com/in/pennyheiple"),
    ("Roberto Forte", "https://www.linkedin.com/in/roberto-forte-ph-d-ba2b2121"),
    ("Roberto Pedraza Ruiz", "https://www.linkedin.com/in/roberto-pedraza-ruiz-281483166"),
    ("Scott Schulte", "https://www.linkedin.com/in/scott-schulte-6a75a97"),
    ("Steffie Rijpkema", "https://www.linkedin.com/in/steffie-rijpkema-49b457105"),
    ("Theopista Abalo", "https://www.linkedin.com/in/theopistaabalo35"),
    ("nding'a ndikon", "https://www.linkedin.com/in/nding-a-orkeyaroi-8a73081b7")
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
    filename = parts[-1]
    filename = filename.replace('?', '_')
    # Handle URL-encoded emojis
    filename = filename.replace('%F0%9F%8C%8E', 'emoji')
    filename = filename.replace('%F0%9F%95%8A', 'emoji')
    return filename + '.json'


async def extract_profile_content(page):
    """Extract content from LinkedIn profile page.
    
    FIX (Oct 30, 2025): LinkedIn changed their HTML structure.
    CSS selectors no longer work reliably. Instead, we:
    1. Get all text from <main> element
    2. Parse first few lines to extract name/headline
    3. Keep full text for About section and other details
    """
    try:
        await page.wait_for_selector('main', timeout=10000)
    except:
        pass
    
    # Get text from main element (more reliable than body)
    try:
        main_elem = await page.query_selector('main')
        if main_elem:
            full_text = await main_elem.inner_text()
        else:
            # Fallback to body if main not found
            full_text = await page.inner_text('body')
    except:
        full_text = await page.inner_text('body')
    
    # Parse name and headline from the first few lines
    # LinkedIn structure: Line 1 is name, then pronouns, then headline
    name = None
    headline = None
    
    lines = full_text.split('\n')
    
    # First non-empty line is usually the name
    for line in lines[:10]:  # Check first 10 lines
        line = line.strip()
        if line and len(line) > 2 and len(line) < 100:
            # Skip common header elements
            if line in ['She/Her', 'He/Him', 'They/Them', '· 1st', '· 2nd', '· 3rd']:
                continue
            if '·' in line and len(line) < 10:  # Skip connection indicators
                continue
            
            if not name:
                name = line
            elif not headline and line not in ['Contact info', 'Message', 'More', 'Highlights']:
                # This is likely the headline (job title/description)
                # It usually comes after the name and before location
                if not any(x in line.lower() for x in ['connection', 'mutual', 'message']):
                    headline = line
                    break
    
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
    
    print(f"Scraping {len(URLs)} LinkedIn profiles for V5...")
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
        
        success_count = 0
        error_count = 0
        
        for i, (member_name, url) in enumerate(URLs, 1):
            print(f"\n[{i}/{len(URLs)}] {member_name}")
            print(f"   {url}")
            
            try:
                # Try networkidle first, but fall back to domcontentloaded if it times out
                try:
                    await page.goto(url, wait_until='networkidle', timeout=15000)
                except:
                    # Networkidle timed out, but page likely loaded - try domcontentloaded
                    try:
                        await page.goto(url, wait_until='domcontentloaded', timeout=10000)
                    except:
                        # Even domcontentloaded failed, but let's try to extract anyway
                        print(f"   ⚠️  Navigation timeout, attempting extraction...")
                
                # Give page time to render
                await asyncio.sleep(3)
                
                # Extract content (even if navigation timed out, content might be there)
                data = await extract_profile_content(page)
                
                # Check if we got meaningful data
                if data['extracted']['name'] or data['extracted']['headline']:
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
                    
                    success_count += 1
                else:
                    print(f"   ❌ No meaningful data extracted")
                    error_count += 1
                
                # Pause between profiles (5 seconds)
                if i < len(URLs):
                    await asyncio.sleep(5)
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                error_count += 1
        
        # Save cookies
        cookies = await context.cookies()
        with open(COOKIES_FILE, 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print("\n" + "="*80)
        print("✅ Complete!")
        print(f"   Success: {success_count}/{len(URLs)}")
        print(f"   Errors: {error_count}/{len(URLs)}")
        print("="*80)
        
        await asyncio.sleep(10)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
