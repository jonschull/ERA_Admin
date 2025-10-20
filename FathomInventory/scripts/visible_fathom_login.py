import asyncio
import json
from playwright.async_api import async_playwright

COOKIES_FILE = "fathom_cookies.json"

async def main():
    print("--- VISIBLE FATHOM LOGIN TEST ---")
    print(f"Loading cookies from: {COOKIES_FILE}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        
        try:
            with open(COOKIES_FILE, 'r') as f:
                cookies = json.load(f)
        except FileNotFoundError:
            print(f"\n❌ ERROR: Cookie file not found at '{COOKIES_FILE}'.")
            print("Please ensure you have generated the cookies first.")
            await browser.close()
            return

        # Sanitize cookies to prevent common errors
        valid_same_site_values = {'Strict', 'Lax', 'None'}
        for cookie in cookies:
            if cookie.get('sameSite') not in valid_same_site_values:
                cookie['sameSite'] = 'Lax'  # A safe default

        await context.add_cookies(cookies)
        print("Cookies loaded into browser context.")

        page = await context.new_page()
        print("Navigating to Fathom home page...")
        await page.goto("https://fathom.video/home", timeout=60000)
        print("\n✅ Successfully loaded Fathom home page.")
        print("The browser is now paused. You can inspect the page.")
        print("Press Ctrl+C in this terminal to close the browser and end the script.")

        # Pause indefinitely until the user manually closes the script
        await page.pause()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting.")
