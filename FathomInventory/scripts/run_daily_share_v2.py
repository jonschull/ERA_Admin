import asyncio
import json
from datetime import datetime
from playwright.async_api import async_playwright

from data_access.tsv_io import read_master_tsv, write_master_tsv, CANONICAL_HEADER
from fathom_ops.browser import sanitize_cookies, harvest_html
from fathom_ops.parser import parse_for_new_calls
from fathom_ops.share import share_call

COOKIES_FILE = "fathom_cookies.json"
MASTER_TSV_FILE = "all_fathom_calls.tsv"
SHARE_EMAIL = "fathomizer@ecorestorationalliance.org"


async def main():
    # 1. Read existing data
    all_calls = read_master_tsv(MASTER_TSV_FILE)
    existing_links = {row.get('Hyperlink') for row in all_calls if row.get('Hyperlink')}
    print(f"Found {len(existing_links)} existing calls in the master list.")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        with open(COOKIES_FILE, 'r') as f:
            cookies = json.load(f)
        cookies = sanitize_cookies(cookies)
        await context.add_cookies(cookies)

        page = await context.new_page()
        html_content = await harvest_html(page, existing_links)
        new_calls = parse_for_new_calls(html_content, existing_links)
        if new_calls:
            print("\nFound the following new call URLs to be added:")
            for call in new_calls:
                print(f"  - {call['Hyperlink']}")
            print(f"Found {len(new_calls)} new calls to add.")
            all_calls.extend(new_calls)
        else:
            print("No new calls found.")

        # 3. Share all calls that haven't been successfully shared yet
        print("\nStarting sharing process for all un-shared calls...")
        for call in all_calls:
            status = (call.get('shareStatus') or '').strip()
            if status not in ['success', 'failed'] and call.get('Hyperlink'):
                success = await share_call(page, call['Hyperlink'], SHARE_EMAIL)
                if success:
                    call['shareStatus'] = 'success'
                    call['sharedWith'] = SHARE_EMAIL
                    call['shareTimestamp'] = datetime.now().isoformat()
                else:
                    call['shareStatus'] = 'failed'

        await browser.close()

    # 4. Write final data
    write_master_tsv(all_calls, MASTER_TSV_FILE)
    print("\n" + "="*60)
    print("SUMMARY:")
    print(f"  Total calls in database: {len(all_calls)}")
    print(f"  New calls added this run: {len(new_calls)}")
    if new_calls:
        print(f"  New call titles:")
        for call in new_calls:
            print(f"    - {call['Title']} ({call['Date']})")
    print("="*60)
    print("\nProcess complete. Master list has been updated.")


if __name__ == "__main__":
    asyncio.run(main())
