#!/usr/bin/env python3
"""
Identify and tag which Fathom account owns each call.
This is important before consolidating accounts.

Strategy:
1. Try to access each call URL with different accounts
2. Record which account(s) can access each call
3. Update database with owner information
"""
import sqlite3
import asyncio
import json
from playwright.async_api import async_playwright

DB_FILE = "fathom_emails.db"
COOKIES_ERA = "fathom_cookies_era.json"
COOKIES_ENABLE = "fathom_cookies_enable.json"

async def check_access(context, call_url):
    """Check if current account can access the call"""
    page = await context.new_page()
    try:
        await page.goto(call_url, wait_until='domcontentloaded', timeout=15000)
        await asyncio.sleep(2)
        
        content = await page.content()
        
        # Check for access indicators
        if "You Need Permission" in content or "Request Access" in content:
            access = False
        elif "Sign in with Google" in content or "Sign in with Microsoft" in content:
            access = False  # Not logged in
        else:
            access = True  # Can view the call
        
        await page.close()
        return access
    except Exception as e:
        await page.close()
        return None  # Error/timeout

async def main():
    print("🔍 IDENTIFYING ACCOUNT OWNERSHIP FOR ALL CALLS")
    print("=" * 80)
    print("\nThis will test which account(s) can access each call.")
    print("Run this BEFORE consolidating accounts with Fathom.\n")
    
    # First, add account_owner column if it doesn't exist
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE calls ADD COLUMN account_owner TEXT")
        conn.commit()
        print("✅ Added account_owner column to database\n")
    except sqlite3.OperationalError:
        print("ℹ️  account_owner column already exists\n")
    
    # Get all calls
    cursor.execute("SELECT hyperlink, title, date FROM calls ORDER BY date DESC")
    all_calls = cursor.fetchall()
    print(f"📊 Testing access for {len(all_calls)} calls\n")
    
    # Load cookies
    with open(COOKIES_ERA, 'r') as f:
        era_cookies = json.load(f)
    with open(COOKIES_ENABLE, 'r') as f:
        enable_cookies = json.load(f)
    
    # Sanitize cookies
    valid_same_site_values = {'Strict', 'Lax', 'None'}
    for cookie_set in [era_cookies, enable_cookies]:
        for cookie in cookie_set:
            if cookie.get('sameSite') not in valid_same_site_values:
                cookie['sameSite'] = 'Lax'
            if 'partitionKey' in cookie:
                del cookie['partitionKey']
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        era_only = 0
        enable_only = 0
        both = 0
        neither = 0
        errors = 0
        
        for i, (hyperlink, title, date) in enumerate(all_calls, 1):
            if i % 50 == 0:
                print(f"Progress: {i}/{len(all_calls)} calls tested...")
            
            # Test ERA account
            context_era = await browser.new_context()
            await context_era.add_cookies(era_cookies)
            era_access = await check_access(context_era, hyperlink)
            await context_era.close()
            
            # Test e-NABLE account
            context_enable = await browser.new_context()
            await context_enable.add_cookies(enable_cookies)
            enable_access = await check_access(context_enable, hyperlink)
            await context_enable.close()
            
            # Determine ownership
            if era_access is None or enable_access is None:
                owner = 'unknown'
                errors += 1
            elif era_access and enable_access:
                owner = 'both'
                both += 1
            elif era_access:
                owner = 'ERA'
                era_only += 1
            elif enable_access:
                owner = 'e-NABLE'
                enable_only += 1
            else:
                owner = 'neither'
                neither += 1
            
            # Update database
            cursor.execute("""
                UPDATE calls 
                SET account_owner = ? 
                WHERE hyperlink = ?
            """, (owner, hyperlink))
            
            if i % 100 == 0:
                conn.commit()  # Periodic save
            
            await asyncio.sleep(0.5)  # Be nice to the server
        
        await browser.close()
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 80)
    print("📊 ACCOUNT OWNERSHIP SUMMARY")
    print("=" * 80)
    print(f"✅ ERA account only:     {era_only}")
    print(f"✅ e-NABLE account only: {enable_only}")
    print(f"🔗 Accessible by both:   {both}")
    print(f"❌ Neither account:      {neither}")
    print(f"⚠️  Errors/timeouts:      {errors}")
    print(f"\n📊 Total: {len(all_calls)} calls")
    
    print("\n" + "=" * 80)
    print("💡 NEXT STEPS FOR CONSOLIDATION")
    print("=" * 80)
    print("1. Export calls by account using: sqlite3 fathom_emails.db")
    print("   SELECT hyperlink, title, date FROM calls WHERE account_owner = 'ERA';")
    print("2. Give Fathom support the list of calls to transfer")
    print("3. After consolidation, all calls should show 'both' access")

if __name__ == "__main__":
    asyncio.run(main())
