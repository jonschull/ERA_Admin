#!/usr/bin/env python3
"""
Login to Fathom manually in Chromium and save cookies.
This ensures cookies work with Playwright's Chromium.
"""

import asyncio
import json
from playwright.async_api import async_playwright

async def login_and_save():
    print("=" * 60)
    print("FATHOM LOGIN - SAVE COOKIES FROM CHROMIUM")
    print("=" * 60)
    print()
    print("Instructions:")
    print("1. A Chromium browser will open")
    print("2. Log into Fathom with: jschull@e-nable.org")
    print("3. Once logged in, press Enter in this terminal")
    print("4. Cookies will be saved automatically")
    print()
    
    async with async_playwright() as p:
        # Launch Chromium (same as what Playwright uses)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navigate to Fathom
        print("🌐 Opening Fathom.video...")
        await page.goto("https://fathom.video/home")
        
        print()
        print("=" * 60)
        print("⏸️  BROWSER OPEN - LOG IN NOW")
        print("=" * 60)
        print()
        print("Log in with: jschull@e-nable.org")
        print()
        print("When you're logged in and can see your calls,")
        input("press Enter here to save cookies... ")
        
        # Get cookies from the browser context
        cookies = await context.cookies()
        
        # Save cookies
        with open('fathom_cookies_enable.json', 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print()
        print(f"✅ Saved {len(cookies)} cookies to fathom_cookies_enable.json")
        
        # Also save to default location
        with open('fathom_cookies.json', 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print(f"✅ Saved {len(cookies)} cookies to fathom_cookies.json")
        print()
        print("🎉 Cookie save complete!")
        print()
        print("Next step: Test with ./run_all.sh")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(login_and_save())
