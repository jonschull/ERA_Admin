#!/usr/bin/env python3
"""Fetch Thijs's LinkedIn profile"""
import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
COOKIES_FILE = SCRIPT_DIR / "linkedin_cookies.json"
OUTPUT_DIR = SCRIPT_DIR / "batches" / "linkedin_profiles"

URLs = [
    ("Thijs Christiaan van Son", "https://www.linkedin.com/in/thijsvanson/?originalSubdomain=no")
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
    
    print(f"Fetching LinkedIn profile for Thijs...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, channel="msedge")
        context = await browser.new_context()
        
        if COOKIES_FILE.exists():
            with open(COOKIES_FILE) as f:
                cookies = json.load(f)
                await context.add_cookies(sanitize_cookies(cookies))
                print("✅ Loaded cookies")
        
        page = await context.new_page()
        
        member_name, url = URLs[0]
        print(f"\n{member_name}")
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
            else:
                print(f"   ❌ No meaningful data extracted")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        cookies = await context.cookies()
        with open(COOKIES_FILE, 'w') as f:
            json.dump(cookies, f, indent=2)
        
        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
