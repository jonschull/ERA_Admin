#!/usr/bin/env python3
"""
Fetch summaries from public share URLs for calls that don't have email summaries.
Reuses the existing HTML-to-Markdown conversion logic from download_emails.py
"""
import sys
import sqlite3
import asyncio
from playwright.async_api import async_playwright

# Import the conversion function
sys.path.append('email_conversion')
from fathom_email_2_md import convert_html_to_markdown

DB_FILE = "fathom_emails.db"

async def fetch_html_from_share_url(page, share_url):
    """Fetch the HTML content from a public Fathom share URL"""
    try:
        await page.goto(share_url, wait_until='networkidle', timeout=30000)
        await asyncio.sleep(2)  # Let dynamic content load
        
        html_content = await page.content()
        return html_content
    except Exception as e:
        print(f"  ❌ Error fetching {share_url}: {str(e)[:100]}")
        return None

async def main():
    print("📥 FETCHING MISSING SUMMARIES FROM PUBLIC SHARE URLs")
    print("=" * 80)
    
    # Get calls that have share URLs but no email summaries
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Find calls with public_share_url but no email with that share URL
    # (i.e., the 31 manually captured calls that don't have email summaries)
    cursor.execute("""
        SELECT c.hyperlink, c.title, c.date, c.public_share_url
        FROM calls c
        WHERE c.public_share_url IS NOT NULL 
          AND c.public_share_url != ''
          AND NOT EXISTS (
              SELECT 1 FROM emails e 
              WHERE e.meeting_url = c.public_share_url
          )
        ORDER BY c.date DESC
    """)
    
    missing_summaries = cursor.fetchall()
    print(f"📊 Found {len(missing_summaries)} calls needing summaries\n")
    
    if len(missing_summaries) == 0:
        print("✅ All calls with share URLs already have summaries!")
        conn.close()
        return
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        success_count = 0
        failed_count = 0
        
        for i, (hyperlink, title, date, share_url) in enumerate(missing_summaries, 1):
            print(f"\n[{i}/{len(missing_summaries)}] {title[:50]}")
            print(f"   Date: {date}")
            print(f"   URL: {share_url[:60]}...")
            
            # Fetch HTML from share URL
            html_content = await fetch_html_from_share_url(page, share_url)
            
            if not html_content:
                failed_count += 1
                continue
            
            # Convert HTML to Markdown using existing converter
            try:
                markdown_result = convert_html_to_markdown(html_content, extract_stats=True)
                if isinstance(markdown_result, tuple):
                    markdown_text, stats = markdown_result
                else:
                    markdown_text = markdown_result
                    stats = {}
                
                # Fix timestamp encoding issue
                markdown_text = markdown_text.replace('×tamp=', '&timestamp=')
                
                # Create a synthetic email record
                # Use the hyperlink as message_id with a prefix to avoid collisions
                synthetic_msg_id = f"synthetic_{hyperlink.split('/')[-1]}"
                
                cursor.execute("""
                    INSERT OR REPLACE INTO emails (
                        message_id, thread_id, date, subject, 
                        body_html, body_md, 
                        meeting_title, meeting_date, meeting_url
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    synthetic_msg_id,
                    synthetic_msg_id,  # Use same as thread_id
                    date,
                    f"Recap for \"{title}\"",
                    html_content,
                    markdown_text,
                    title,
                    date,
                    share_url
                ))
                
                conn.commit()
                print(f"   ✅ Summary saved to database")
                success_count += 1
                
            except Exception as e:
                print(f"   ❌ Conversion failed: {str(e)[:100]}")
                failed_count += 1
            
            await asyncio.sleep(1)  # Be nice to the server
        
        await browser.close()
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("📊 SUMMARY FETCHING COMPLETE")
    print("=" * 80)
    print(f"✅ Successfully fetched: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"\n💾 Database now has summaries for {success_count} additional calls")

if __name__ == "__main__":
    asyncio.run(main())
