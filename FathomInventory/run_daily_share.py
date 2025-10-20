#!/usr/bin/env python3
"""
Core Fathom call scraper - discovers and shares new calls
🔧 Modifying? Read DEVELOPMENT.md for testing requirements
⚠️ Requires: Fathom cookies (refresh weekly with scripts/refresh_fathom_auth.sh)
"""
import asyncio
import os
import sys
import json
import csv
import argparse
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from scripts.share_fathom_call2 import share_fathom_recording
from data_access import db_io

# Add parent directory to path to import era_config
sys.path.insert(0, str(Path(__file__).parent.parent))
from era_config import get_fathom_account_config

# Get active Fathom account configuration
fathom_config = get_fathom_account_config()

# --- Default Configuration ---
DEFAULT_COOKIES_FILE = fathom_config['cookies_file']
DEFAULT_TSV_FILE = "all_fathom_calls.tsv"
DEFAULT_DB_FILE = "fathom_emails.db"
DEFAULT_SHARE_EMAIL = fathom_config['share_to']
CANONICAL_HEADER = ['Title', 'Date', 'Duration', 'Hyperlink', 'shareStatus', 'sharedWith', 'shareTimestamp']

# --- Utility Functions ---

def normalize_date(date_str):
    """Convert various date formats to ISO format (YYYY-MM-DD).
    
    Handles formats like:
    - "Oct 7, 2025" -> "2025-10-07"
    - "October 07, 2025" -> "2025-10-07"
    - "2025-10-07" -> "2025-10-07" (already normalized)
    """
    from dateutil import parser
    
    if not date_str or date_str == "Unknown Date":
        return date_str
    
    try:
        # Parse the date using dateutil's flexible parser
        dt = parser.parse(date_str)
        # Return in ISO format
        return dt.strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        # If parsing fails, return original
        return date_str
def read_master_tsv(tsv_file):
    if not os.path.exists(tsv_file):
        return []
    with open(tsv_file, 'r', newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t'))

def write_master_tsv(records, tsv_file):
    with open(tsv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CANONICAL_HEADER, delimiter='\t', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(records)

# --- Main Logic ---
async def harvest_html(page, existing_hyperlinks):
    print("\n📊 Starting call discovery...")
    # Note: Authentication already verified by pre-flight check
    # Just wait for the calls to load
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
            hyperlink = "https://fathom.video" + link_element['href'] if link_element and not link_element['href'].startswith('http') else (link_element['href'] if link_element else None)
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

async def verify_authentication(page):
    """Pre-flight check: Verify authentication before attempting to scrape.
    Returns True if authenticated, False otherwise.
    """
    print("🔐 Pre-flight authentication check...")
    try:
        await page.goto("https://fathom.video/home", timeout=30000)
        
        # Check for login redirect or login button
        login_indicators = await page.query_selector_all('a[href*="login"], button:has-text("Sign in"), button:has-text("Log in")')
        if login_indicators:
            print("❌ AUTHENTICATION FAILED: Redirected to login page")
            print("   → Fathom cookies are expired or invalid")
            print("   → Run: ./scripts/refresh_fathom_auth.sh")
            return False
        
        # Look for authenticated indicators
        # Check if we're on the My Calls page (title) or can see the link
        title = await page.title()
        my_calls_link = await page.query_selector('a:has-text("My Calls")')
        call_thumbnails = await page.query_selector('call-gallery-thumbnail')
        
        if "My Calls" in title or my_calls_link or call_thumbnails:
            print("✅ Authentication verified")
            return True
        else:
            print("❌ AUTHENTICATION FAILED: No authenticated page indicators found")
            print("   → Fathom site may have changed or cookies expired")
            return False
        
    except Exception as e:
        print(f"❌ AUTHENTICATION CHECK FAILED: {type(e).__name__}: {e}")
        return False

def parse_for_new_calls(html_content, existing_hyperlinks):
    soup = BeautifulSoup(html_content, 'html.parser')
    new_meetings = []
    for card in soup.find_all('call-gallery-thumbnail'):
        link_element = card.find('a', href=True)
        hyperlink = "https://fathom.video" + link_element['href'] if link_element and not link_element['href'].startswith('http') else (link_element['href'] if link_element else None)
        if hyperlink and hyperlink not in existing_hyperlinks:
            title = (card.find('call-gallery-thumbnail-title').get_text(strip=True) if card.find('call-gallery-thumbnail-title') else "")
            raw_date = (card.find('li', class_='opacity-70').get_text(strip=True) if card.find('li', class_='opacity-70') else "Unknown Date")
            date = normalize_date(raw_date)  # Normalize to ISO format
            duration = (card.find('span', class_='font-semibold').get_text(strip=True) if card.find('span', class_='font-semibold') else "")
            new_meetings.append({'Title': title, 'Date': date, 'Duration': duration, 'Hyperlink': hyperlink})
    return new_meetings


# --- Main Execution ---
async def main(cookies_file=None, tsv_file=None, db_file=None, share_email=None, use_db=False):
    # Use defaults if not specified
    cookies_file = cookies_file or DEFAULT_COOKIES_FILE
    tsv_file = tsv_file or DEFAULT_TSV_FILE
    db_file = db_file or DEFAULT_DB_FILE
    share_email = share_email or DEFAULT_SHARE_EMAIL
    
    print(f"Running with:")
    print(f"  Cookies: {cookies_file}")
    print(f"  Backend: {'DATABASE' if use_db else 'TSV'}")
    if use_db:
        print(f"  Database: {db_file}")
    else:
        print(f"  TSV: {tsv_file}")
    print(f"  Share to: {share_email}")
    print()
    
    # 1. Read existing data
    if use_db:
        all_calls = db_io.read_calls_from_db(db_file)
        existing_links = db_io.get_existing_hyperlinks(db_file)
        print(f"Found {len(existing_links)} existing calls in the database.")
    else:
        all_calls = read_master_tsv(tsv_file)
        existing_links = {row['Hyperlink'] for row in all_calls if row.get('Hyperlink')}
        print(f"Found {len(existing_links)} existing calls in the TSV file.")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        with open(cookies_file, 'r') as f:
            cookies = json.load(f)

        # Sanitize cookies before adding them to the context
        valid_same_site_values = {'Strict', 'Lax', 'None'}
        for cookie in cookies:
            if cookie.get('sameSite') not in valid_same_site_values:
                cookie['sameSite'] = 'Lax'  # A safe default
            if 'partitionKey' in cookie and not isinstance(cookie.get('partitionKey'), str):
                del cookie['partitionKey']

        await context.add_cookies(cookies)
        page = await context.new_page()
        
        # Pre-flight authentication check
        if not await verify_authentication(page):
            await browser.close()
            print("\n" + "="*60)
            print("❌ CRITICAL: Authentication failure - cannot proceed")
            print("="*60)
            sys.exit(1)
        
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
            # Process a call only if its status is not 'success' or 'failed'.
            # This handles new calls (empty status) and prevents retrying failed ones.
            status = call.get('shareStatus', '').strip()
            if status not in ['success', 'failed'] and call.get('Hyperlink'):
                # The share function returns True on success and False on failure.
                success = await share_fathom_recording(page, call['Hyperlink'], share_email)
                if success:
                    call['shareStatus'] = 'success'
                    call['sharedWith'] = share_email
                    call['shareTimestamp'] = datetime.now().isoformat()
                else:
                    call['shareStatus'] = 'failed'  # Log the failure.
        
        await browser.close()

    # 4. Write final data
    if use_db:
        db_io.write_calls_to_db(all_calls, db_file)
        print(f"\n💾 Updated database: {db_file}")
    else:
        write_master_tsv(all_calls, tsv_file)
        print(f"\n💾 Updated TSV: {tsv_file}")
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
    parser = argparse.ArgumentParser(
        description="Scrape Fathom calls and share them",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Use default account (fathomizer)
  python run_daily_share.py
  
  # Use different identity
  python run_daily_share.py --cookies fathom_cookies_jschull.json --tsv jschull_calls.tsv
  
  # Scrape only (no sharing)
  python run_daily_share.py --no-share
"""
    )
    parser.add_argument('--cookies', default=DEFAULT_COOKIES_FILE,
                        help=f'Cookie file (default: {DEFAULT_COOKIES_FILE})')
    parser.add_argument('--tsv', default=DEFAULT_TSV_FILE,
                        help=f'TSV file for calls (default: {DEFAULT_TSV_FILE})')
    parser.add_argument('--share-email', default=DEFAULT_SHARE_EMAIL,
                        help=f'Email to share calls to (default: {DEFAULT_SHARE_EMAIL})')
    parser.add_argument('--use-db', action='store_true',
                        help='Use database instead of TSV (default: TSV)')
    parser.add_argument('--db', default=DEFAULT_DB_FILE,
                        help=f'Database file when using --use-db (default: {DEFAULT_DB_FILE})')
    
    args = parser.parse_args()
    
    try:
        asyncio.run(main(
            cookies_file=args.cookies,
            tsv_file=args.tsv,
            db_file=args.db,
            share_email=args.share_email,
            use_db=args.use_db
        ))
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
