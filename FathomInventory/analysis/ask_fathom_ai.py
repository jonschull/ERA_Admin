import asyncio
import json
import os
import argparse
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# --- Configuration ---
COOKIES_FILE = "../fathom_cookies.json"

async def main(fathom_url: str, question: str):
    """Accesses a Fathom URL, asks a question to the AI, and prints the response."""
    if not os.path.exists(COOKIES_FILE):
        print(f"Error: Cookies file not found at '{COOKIES_FILE}'. Please ensure the file exists.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        try:
            with open(COOKIES_FILE, 'r') as f:
                cookies = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {COOKIES_FILE}. The file might be corrupt.")
            await browser.close()
            return

        # Sanitize cookies to prevent errors, reusing logic from existing scripts
        valid_same_site_values = {'Strict', 'Lax', 'None'}
        for cookie in cookies:
            if cookie.get('sameSite') not in valid_same_site_values:
                cookie['sameSite'] = 'Lax'  # A safe default
            if 'partitionKey' in cookie and not isinstance(cookie.get('partitionKey'), str):
                del cookie['partitionKey']

        await context.add_cookies(cookies)
        page = await context.new_page()

        print(f"Navigating to: {fathom_url}")
        try:
            await page.goto(fathom_url, timeout=60000, wait_until='domcontentloaded')
            title = await page.title()
            print(f"Successfully accessed page. Title: '{title}'")

            # Handle the 'Fathom Premium Required' popup with a more robust method
            print("Checking for 'Fathom Premium' popup...")
            try:
                # First, try to click the close button with a very specific selector
                close_button_selector = 'user-premium-required ui-icon.cursor-pointer'
                close_button = page.locator(close_button_selector)
                await close_button.click(timeout=5000) # Wait up to 5 seconds
                print("Closed the 'Fathom Premium' popup by clicking the 'X' button.")
                await page.wait_for_timeout(1000) # Wait for popup to disappear
            except Exception:
                # If clicking fails, try pressing the Escape key as a fallback
                print("Could not click the 'X' button, trying to press 'Escape' key...")
                try:
                    await page.keyboard.press('Escape')
                    print("Pressed 'Escape' key to close the popup.")
                    await page.wait_for_timeout(1000) # Wait for popup to disappear
                except Exception as e:
                    print(f"'Fathom Premium' popup not found or could not be closed. Error: {e}")

            # Click the 'ASK FATHOM' tab to ensure it's visible
            print("Clicking 'ASK FATHOM' tab...")
            await page.get_by_role("button", name="ASK FATHOM").click()
            await page.wait_for_timeout(1000) # Wait a moment for the tab to load

            # Interact with the Fathom AI
            print("Interacting with Fathom AI...")
            ask_fathom_textarea = page.locator('textarea[placeholder="Ask Fathom AI"]')
            await ask_fathom_textarea.fill(question)
            await ask_fathom_textarea.press('Enter')

            # Wait for the response to be generated
            print("Waiting for AI response...")
            # This waits for the AI's response to finish generating, indicated by the disappearance of the 'is thinking' element.
            await page.locator('ask-fathom-conversation-thinking').wait_for(state='detached', timeout=30000)

            # Capture the content using the precise XPath provided by the user.
            response_xpath = '/html/body/inertia-app/app-layout/main/page-call-detail/div[2]/div/section/ask-fathom-chat/ui-scrollarea/section/div[2]/div[2]/ask-fathom-message[2]/figure/div/blockquote/div/preview-markdown/ui-content'
            conversation_area = page.locator(f'xpath={response_xpath}')
            conversation_html = await conversation_area.inner_html()

            # Use BeautifulSoup to parse and print the text content nicely
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(conversation_html, 'html.parser')
            ai_response_text = soup.get_text(separator='\n', strip=True)
            # Add a blank line before each participant for readability
            formatted_response = ai_response_text.replace('\nName:', '\n\nName:')
            print("\n--- Fathom AI Response ---")
            print(formatted_response)
            print("--------------------------")

        except Exception as e:
            print(f"Failed to access or interact with the URL. Error: {e}")
            await page.screenshot(path='fathom_access_error.png')
            print("A screenshot of the error has been saved to 'fathom_access_error.png'.")
        finally:
            await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ask a question to the Fathom AI on a specific call page.')
    parser.add_argument('url', type=str, help='The full URL of the Fathom call page.')
    parser.add_argument('question', type=str, help='The question to ask the Fathom AI.')
    args = parser.parse_args()

    asyncio.run(main(args.url, args.question))
