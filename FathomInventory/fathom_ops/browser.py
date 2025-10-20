"""Browser helpers for Fathom interactions (sanitizing cookies, harvesting HTML).

This module contains only pure helpers around the Playwright page context.
Network/auth timing remains unchanged from the original script.
"""
from __future__ import annotations

from typing import List, Dict, Set
from bs4 import BeautifulSoup


def sanitize_cookies(cookies: List[Dict]) -> List[Dict]:
    """Return a sanitized copy of cookies for Playwright context.add_cookies().

    - Ensures sameSite ∈ {"Strict","Lax","None"} (defaults to "Lax")
    - Removes non-string partitionKey
    """
    valid_same_site_values = {"Strict", "Lax", "None"}
    sanitized: List[Dict] = []
    for c in cookies:
        c2 = dict(c)
        if c2.get("sameSite") not in valid_same_site_values:
            c2["sameSite"] = "Lax"
        if "partitionKey" in c2 and not isinstance(c2.get("partitionKey"), str):
            del c2["partitionKey"]
        sanitized.append(c2)
    return sanitized


async def harvest_html(page, existing_hyperlinks: Set[str]) -> str:
    """Scroll the Fathom home page until a known call is visible and return page HTML.

    Mirrors the original scrolling logic from run_daily_share.py.
    """
    print("Navigating to Fathom home page...")
    await page.goto("https://fathom.video/home", timeout=60000)
    await page.wait_for_selector('a:has-text("My Calls")', timeout=15000)

    # Wait for the first call to be rendered before trying to find the container
    print("Waiting for call list to render...")
    await page.wait_for_selector('call-gallery-thumbnail', timeout=15000)
    print("Call list rendered.")

    print("Scrolling until a known call is found...")
    known_element_selector = 'call-gallery-thumbnail'
    stable_scrolls = 0
    last_count = 0
    while stable_scrolls < 3:
        current_html = await page.content()
        soup = BeautifulSoup(current_html, 'html.parser')
        visible_thumbnails = soup.find_all(known_element_selector)

        found_known_call = False
        for card in visible_thumbnails:
            link_element = card.find('a', href=True)
            hyperlink = (
                "https://fathom.video" + link_element['href']
                if link_element and not link_element['href'].startswith('http')
                else (link_element['href'] if link_element else None)
            )
            if hyperlink in existing_hyperlinks:
                print(f"Found known call: {hyperlink}. Stopping scroll.")
                found_known_call = True
                break
        if found_known_call:
            break

        # Scroll down to load more
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await page.wait_for_timeout(2500)
        new_count = len(visible_thumbnails)

        if new_count == last_count:
            stable_scrolls += 1
            print(f"  - Scroll attempt {stable_scrolls}/3 with no new calls found.")
        else:
            stable_scrolls = 0
            print(f"  - Scrolled, now showing {new_count} calls.")
            last_count = new_count

    print("Finished scrolling.")
    return await page.content()
