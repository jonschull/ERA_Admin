#!/usr/bin/env python3
"""Simple test to see what's happening with Fathom authentication."""

import asyncio
import json
from playwright.async_api import async_playwright

async def test():
    with open('fathom_cookies_enable.json', 'r') as f:
        cookies = json.load(f)
    
    print(f"Loaded {len(cookies)} cookies")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.add_cookies(cookies)
        
        page = await context.new_page()
        print("Navigating to Fathom...")
        await page.goto("https://fathom.video/home", timeout=30000)
        await page.wait_for_load_state('networkidle', timeout=15000)
        
        title = await page.title()
        print(f"Page title: {title}")
        
        # Wait for inspection
        print("\nBrowser open - press Ctrl+C to close")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nClosing...")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test())
