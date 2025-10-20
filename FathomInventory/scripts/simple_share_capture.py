#!/usr/bin/env python3
"""
Simplest approach: Open URLs in your default browser where you're already logged in.
You manually copy share links and paste them here.
"""
import sqlite3
import webbrowser
import re
import time

DB_FILE = "fathom_emails.db"

def main():
    print("🔗 SIMPLE SHARE LINK CAPTURE")
    print("=" * 80)
    print("\nThis will open each call in your DEFAULT web browser.")
    print("Use whatever browser you're already logged into Fathom with.")
    print("\nFor each call:")
    print("  1. Browser opens to the Fathom call")
    print("  2. Click ⋯ menu → 'Copy Share Link'")
    print("  3. Return here and paste the link")
    print("  4. Press Enter to continue")
    print("\nPress Enter to start...")
    input()
    
    # Get calls missing public URLs
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT title, date, hyperlink
        FROM calls
        WHERE (public_share_url IS NULL OR public_share_url = '')
        ORDER BY date DESC
    """)
    
    missing_calls = cursor.fetchall()
    print(f"\n📊 Found {len(missing_calls)} calls missing public URLs\n")
    
    success_count = 0
    skipped_count = 0
    
    for i, (title, date, hyperlink) in enumerate(missing_calls, 1):
        print("\n" + "=" * 80)
        print(f"[{i}/{len(missing_calls)}] {title}")
        print(f"Date: {date}")
        print(f"URL:  {hyperlink}")
        print("=" * 80)
        
        # Suggest which account to use
        title_lower = title.lower()
        if 'e-nable' in title_lower or 'enable' in title_lower:
            suggested_account = "jschull@e-nable.org"
            print("\n💡 SUGGESTED ACCOUNT: jschull@e-nable.org (e-NABLE call)")
        else:
            suggested_account = "ecorestorationalliance@gmail.com"
            print("\n💡 SUGGESTED ACCOUNT: ecorestorationalliance@gmail.com (ERA call)")
        
        print("   If access denied, try the other account.")
        
        print("\n🌐 Opening in your browser...")
        webbrowser.open(hyperlink)
        time.sleep(1)  # Give browser time to open
        
        print("\n📋 INSTRUCTIONS:")
        print(f"  1. Make sure you're signed in as: {suggested_account}")
        print("  2. In the browser: Click ⋯ menu → 'Copy Share Link'")
        print("  3. Return here and paste the share URL below")
        print("\n  If 'Access Denied', switch accounts and try again.")
        print("\nOptions:")
        print("  [url]   = Paste the share link")
        print("  [skip]  = Skip this call")
        print("  [quit]  = Save and exit")
        
        user_input = input("\n👉 Paste share link: ").strip()
        
        if user_input.lower() == 'quit':
            print("\n💾 Saving and exiting...")
            break
        elif user_input.lower() == 'skip' or not user_input:
            print("⏭️  Skipped")
            skipped_count += 1
            continue
        elif 'fathom.video/share/' in user_input:
            # Extract clean URL
            match = re.search(r'https://fathom\.video/share/[A-Za-z0-9_-]+', user_input)
            if match:
                share_url = match.group(0)
                cursor.execute("""
                    UPDATE calls
                    SET public_share_url = ?
                    WHERE hyperlink = ?
                """, (share_url, hyperlink))
                conn.commit()
                print(f"✅ Saved: {share_url}")
                success_count += 1
            else:
                print("❌ Invalid URL format - skipping")
                skipped_count += 1
        else:
            print("❌ Invalid input - skipping")
            skipped_count += 1
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 80)
    print("📊 FINAL SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully captured: {success_count}")
    print(f"⏭️  Skipped: {skipped_count}")
    print(f"📊 Total processed: {success_count + skipped_count}/{len(missing_calls)}")
    
    # Check final database state
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM calls WHERE public_share_url IS NOT NULL AND public_share_url != ''")
    total_with_urls = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM calls")
    total_calls = cursor.fetchone()[0]
    conn.close()
    
    print(f"\n💾 DATABASE STATUS:")
    print(f"   Calls with URLs: {total_with_urls}/{total_calls} ({total_with_urls/total_calls*100:.1f}%)")
    print(f"   Missing: {total_calls - total_with_urls}")

if __name__ == "__main__":
    main()
