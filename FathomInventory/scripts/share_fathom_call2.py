import asyncio
from playwright.async_api import async_playwright, Page, BrowserContext
import json
import os

COOKIES_FILE = "fathom_cookies.json"

async def ensure_login(context: BrowserContext, page: Page):
    """Ensures the user is logged in. If not, prompts for login and saves cookies."""
    print("Checking authentication status...")
    await page.goto("https://fathom.video/home", timeout=60000)

    try:
        # Check for an element that only exists when logged in.
        await page.wait_for_selector('a:has-text("My Calls")', timeout=3000)
        print("Authentication is valid.")
        return True
    except Exception:
        # If the element is not found, the session has expired. Display instructions in the browser.
        print("\n*** Fathom session has expired. Please see the browser window for instructions. ***")

        html_instructions = f"""
        <html>
            <head>
                <title>Fathom Session Expired</title>
                <style>
                    body {{ font-family: sans-serif; line-height: 1.6; padding: 2em; background-color: #f4f4f4; color: #333; }}
                    .container {{ max-width: 800px; margin: auto; background: #fff; padding: 2em; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                    h1 {{ color: #d9534f; }}
                    code {{ background: #eee; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace; }}
                    li {{ margin-bottom: 1em; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Fathom Session Expired</h1>
                    <p>To re-authenticate, please follow these steps:</p>
                    <ol>
                        <li>Open your regular web browser (e.g., Chrome, Firefox).</li>
                        <li>Go to <b>https://fathom.video</b> and log in with your Google account.</li>
                        <li>Once logged in, use a browser extension to export your cookies for the <code>fathom.video</code> domain. (Recommended for Chrome: 'Get cookies.txt LOCALLY')</li>
                        <li>Save the exported cookies into a file named exactly <code>{COOKIES_FILE}</code> in this directory: <br><code>{os.getcwd()}</code></li>
                        <li>Make sure to overwrite the old file if it exists.</li>
                        <li>Re-run the script.</li>
                    </ol>
                    <p>Close this window at your convenience.</p>
                </div>
            </body>
        </html>
        """
        await page.goto("about:blank")
        await page.set_content(html_instructions)
        # Wait indefinitely until the user closes the page, then the script will exit.
        await page.wait_for_event("close", timeout=0)
        return False

async def share_fathom_recording(page: Page, call_url: str, share_email: str):
    """Navigates to a Fathom call URL and shares it with a specified email."""
    try:
        print(f"\nProcessing call: {call_url}")
        await page.goto(call_url, timeout=60000)
        await page.wait_for_selector('button:has-text("Share")', timeout=20000)
        print("  - Successfully loaded call page.")

        await page.locator('button:has-text("Share")').first.click()
        await page.wait_for_timeout(2000)

        await page.keyboard.type(share_email)
        await page.keyboard.press('Enter')
        print(f"  - Entered email: {share_email}")
        await page.wait_for_timeout(2000)

        final_share_button_xpath = "/html/body/inertia-app/app-layout/main/page-call-detail/div[2]/div/page-call-detail-notes/ui-scrollarea/section/div[2]/div[2]/div/div/section/page-call-detail-share-menu/page-call-detail-share-dialog/ui-dialog/aside/div/div/div[2]/button[2]"
        await page.locator(f'xpath={final_share_button_xpath}').click()
        print("  - Clicked final share button.")
        await page.wait_for_timeout(2000)
        print("  - Share successful.")
        return True
    except Exception as e:
        print(f"  - Failed to share call {call_url}. Error: {e}")
        try:
            await page.screenshot(path=f"error_screenshot_{call_url.split('/')[-1]}.png")
            print("  - Screenshot of the error was saved.")
        except Exception as screenshot_error:
            print(f"  - CRITICAL: Could not take a screenshot. Error: {screenshot_error}")
        return False

async def main():
    """Main function to run the script for a single test case."""
    test_call_url = "https://fathom.video/calls/408473279"
    test_share_email = "jschull@gmail.com"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        if os.path.exists(COOKIES_FILE):
            with open(COOKIES_FILE, 'r') as f:
                cookies = json.load(f)

            # Sanitize cookies: Playwright does not accept 'unspecified' for sameSite.
            # A safe default is 'Lax'.
            valid_same_site_values = {"Strict", "Lax", "None"}
            for cookie in cookies:
                # Sanitize sameSite
                if cookie.get("sameSite") not in valid_same_site_values:
                    cookie["sameSite"] = "Lax"
                
                # Sanitize partitionKey: remove if it's not a string
                if "partitionKey" in cookie and not isinstance(cookie.get("partitionKey"), str):
                    del cookie["partitionKey"]

            await context.add_cookies(cookies)

        page = await context.new_page()
        
        # Ensure we are logged in before proceeding
        if not await ensure_login(context, page):
            await browser.close()
            return

        success = await share_fathom_recording(page, test_call_url, test_share_email)

        if success:
            print("\nTest run completed successfully.")
        else:
            print("\nTest run failed. Please check the error message and screenshot.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
