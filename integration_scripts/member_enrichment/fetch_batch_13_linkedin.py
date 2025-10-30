#!/usr/bin/env python3
"""Fetch LinkedIn profiles for remaining 13 members (9 with URLs)"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
COOKIES_FILE = SCRIPT_DIR / "linkedin_cookies.json"
OUTPUT_DIR = SCRIPT_DIR / "batches" / "linkedin_profiles"

URLs = [
    ("Terrance Long", "https://www.linkedin.com/in/terrance-p-long-6b59829/"),
    ("Douglas Sheil", "https://www.linkedin.com/in/douglas-sheil-55330a9a/"),
    ("Hollis Mclellan", "https://www.linkedin.com/in/hollis-mclellan-a084b2b0/"),
    ("Sarah Herzog", "https://www.linkedin.com/in/sarah-herzog-78a07a243/"),
    ("Nadait Gebremedhen", "https://www.linkedin.com/in/nadaitgebremedhen/"),
    ("Joe James", "https://www.linkedin.com/in/joe-james-765b6415/"),
    ("Scot Bryson", "https://www.linkedin.com/in/scotbryson/"),
    ("Coakee William Wildcat", "https://www.linkedin.com/in/william-wildcat-93a21164/"),
    ("Edib Korkut", "https://www.linkedin.com/in/edib-korkut-21a00a29/"),
]

def sanitize_cookies(cookies):
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
    url = url.rstrip('/')
    parts = url.split('/')
    filename = parts[-1].split('?')[0]
    return filename + '.json'

async def extract_profile_content(page):
    try:
        await page.wait_for_selector('main', timeout=10000)
    except:
        pass
    
    try:
        main_elem = await page.query_selector('main')
        if main_elem:
            full_text = await main_elem.inner_text()
        else:
            full_text = await page.inner_text('body')
    except:
        full_text = await page.inner_text('body')
    
    name = None
    headline = None
    
    lines = full_text.split('\n')
    
    for line in lines[:10]:
        line = line.strip()
        if line and len(line) > 2 and len(line) < 100:
            if line in ['She/Her', 'He/Him', 'They/Them', '· 1st', '· 2nd', '· 3rd']:
                continue
            if '·' in line and len(line) < 10:
                continue
            
            if not name:
                name = line
            elif not headline and line not in ['Contact info', 'Message', 'More', 'Highlights']:
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
    
    print(f"Fetching {len(URLs)} LinkedIn profiles...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, channel="msedge")
        context = await browser.new_context()
        
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
                try:
                    await page.goto(url, wait_until='networkidle', timeout=15000)
                except:
                    try:
                        await page.goto(url, wait_until='domcontentloaded', timeout=10000)
                    except:
                        print(f"   ⚠️  Navigation timeout, attempting extraction...")
                
                await asyncio.sleep(3)
                data = await extract_profile_content(page)
                
                if data['extracted']['name'] or data['extracted']['headline']:
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
                
                if i < len(URLs):
                    await asyncio.sleep(5)
            
            except Exception as e:
                print(f"   ❌ Error: {e}")
                error_count += 1
        
        cookies = await context.cookies()
        with open(COOKIES_FILE, 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print("\n" + "="*80)
        print(f"✅ Complete! Success: {success_count}/{len(URLs)}, Errors: {error_count}")
        print("="*80)
        
        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
