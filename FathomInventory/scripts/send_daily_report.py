#!/usr/bin/env python3
"""
Daily report email - summarizes Fathom inventory run results
Sends to jschull@gmail.com with calls captured, account used, and alerts
Uses Gmail API (same authentication as download_emails.py)
"""
import os
import sys
import sqlite3
import json
import base64
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Add parent directory to path to import era_config
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from era_config import get_fathom_account_config

# Get active Fathom account configuration
fathom_config = get_fathom_account_config()

# Configuration
REPORT_EMAIL = "jschull@gmail.com"
EXPECTED_ACCOUNT = fathom_config['email']
DB_FILE = "fathom_emails.db"
COOKIE_FILE = fathom_config['cookies_file']
# Gmail API scopes - use existing token with readonly, add send if needed
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

def get_database_health():
    """Check database health indicators for potential issues"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    health = {}
    
    # Check last email date using rowid (insertion order) for most recent
    cursor.execute("""
        SELECT meeting_date, date
        FROM emails 
        WHERE meeting_date IS NOT NULL AND meeting_date != ''
        ORDER BY rowid DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    if row:
        try:
            from dateutil import parser
            # Parse the email timestamp (date column has full timestamp)
            if row['date']:
                latest_date = parser.parse(row['date'])
                days_since_email = (datetime.now(latest_date.tzinfo) - latest_date).days
                health['last_email_date'] = row['meeting_date']
                health['days_since_last_email'] = days_since_email
            else:
                health['days_since_last_email'] = 999
        except:
            health['days_since_last_email'] = 999
    else:
        health['days_since_last_email'] = 999
    
    # Check calls missing public URLs
    cursor.execute("SELECT COUNT(*) FROM calls WHERE public_share_url IS NULL OR public_share_url = ''")
    missing_urls = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM calls")
    total_calls = cursor.fetchone()[0]
    health['calls_missing_urls'] = missing_urls
    health['total_calls'] = total_calls
    health['percent_missing_urls'] = (missing_urls / total_calls * 100) if total_calls > 0 else 0
    
    conn.close()
    return health

def check_recent_auth_failures():
    """Check recent log files for authentication failures."""
    log_patterns = [
        "TimeoutError: Page.wait_for_selector",
        "AUTHENTICATION FAILED",
        "Redirected to login",
        "Timeout 15000ms exceeded",
        "waiting for locator"
    ]
    
    try:
        # Check both log locations
        log_files = ['cron.log', 'logs/fathom_cron.log']
        
        for log_file in log_files:
            if not os.path.exists(log_file):
                continue
                
            # Read last 200 lines (approximately last run)
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()[-200:]
                log_content = ''.join(lines)
                
                # Check for auth failure patterns
                for pattern in log_patterns:
                    if pattern in log_content:
                        return True, f"Found '{pattern}' in logs"
        
        return False, None
    except Exception as e:
        return False, f"Error reading logs: {e}"

def get_cookie_info():
    """Get info about which cookie file is active and its age"""
    try:
        # Get account info from centralized config
        account_name = fathom_config['name']
        account_email = fathom_config['email']
        
        # Get modification time
        mtime = os.path.getmtime(COOKIE_FILE)
        age_days = (datetime.now().timestamp() - mtime) / 86400
        
        # Get cookie count
        with open(COOKIE_FILE, 'r') as f:
            cookies = json.load(f)
        
        return {
            'file': COOKIE_FILE,
            'account': account_email,
            'account_name': account_name,
            'age_days': age_days,
            'cookie_count': len(cookies)
        }
    except Exception as e:
        return {
            'file': 'Error',
            'account': 'Unknown',
            'age_days': -1,
            'error': str(e)
        }

def get_drive_backup_status():
    """Check Google Drive for most recent backup upload"""
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from dateutil import parser
        
        # Load credentials
        if not os.path.exists('token.json'):
            return None  # No Drive access configured yet
        
        creds = Credentials.from_authorized_user_file('token.json')
        if not creds or not creds.valid:
            return None  # Credentials expired
        
        service = build('drive', 'v3', credentials=creds)
        
        # Find FathomInventory_Backups folder
        response = service.files().list(
            q="name='FathomInventory_Backups' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        folders = response.get('files', [])
        if not folders:
            return None  # Folder doesn't exist yet
        
        folder_id = folders[0]['id']
        
        # Get most recent file in folder
        response = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            spaces='drive',
            fields='files(name, createdTime, size)',
            orderBy='createdTime desc',
            pageSize=1
        ).execute()
        
        files = response.get('files', [])
        if not files:
            return None  # No files in folder
        
        latest_file = files[0]
        created_time = parser.parse(latest_file['createdTime'])
        
        # Convert to local time for display
        import time
        local_tz_offset = -time.timezone if time.daylight == 0 else -time.altzone
        local_time = created_time + timedelta(seconds=local_tz_offset)
        
        # Calculate hours ago using timezone-aware comparison
        now_utc = datetime.now(created_time.tzinfo)
        hours_ago = (now_utc - created_time).total_seconds() / 3600
        
        return {
            'file': latest_file['name'],
            'time': local_time.strftime('%b %d, %I:%M %p'),
            'hours_ago': hours_ago,
            'size_mb': int(latest_file.get('size', 0)) / (1024*1024)
        }
    except Exception as e:
        return {'error': str(e)}

def get_backup_status():
    """Get status of most recent backups (local and cloud)"""
    try:
        backup_dir = Path("backups")
        if not backup_dir.exists():
            return {'error': 'Backup directory not found'}
        
        # Find most recent DB backup
        db_backups = sorted(backup_dir.glob('fathom_emails.backup_*.db'), key=lambda p: p.stat().st_mtime, reverse=True)
        # Find most recent ZIP backup
        zip_backups = sorted(backup_dir.glob('fathom_tables_*.zip'), key=lambda p: p.stat().st_mtime, reverse=True)
        
        result = {}
        
        if db_backups:
            latest_db = db_backups[0]
            mtime = datetime.fromtimestamp(latest_db.stat().st_mtime)
            hours_ago = (datetime.now() - mtime).total_seconds() / 3600
            result['db_backup'] = {
                'file': latest_db.name,
                'time': mtime.strftime('%b %d, %I:%M %p'),
                'hours_ago': hours_ago
            }
        
        if zip_backups:
            latest_zip = zip_backups[0]
            mtime = datetime.fromtimestamp(latest_zip.stat().st_mtime)
            hours_ago = (datetime.now() - mtime).total_seconds() / 3600
            result['zip_backup'] = {
                'file': latest_zip.name,
                'time': mtime.strftime('%b %d, %I:%M %p'),
                'hours_ago': hours_ago,
                'size_mb': latest_zip.stat().st_size / (1024*1024)
            }
        
        # Check Google Drive
        drive_status = get_drive_backup_status()
        if drive_status:
            result['drive_backup'] = drive_status
        
        if not result:
            return {'error': 'No backups found'}
        
        return result
    except Exception as e:
        return {'error': str(e)}

def get_participant_stats(db_path):
    """Get participant database statistics"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Total participants
        cursor.execute("SELECT COUNT(*) FROM participants")
        total = cursor.fetchone()[0]
        
        # Unique names
        cursor.execute("SELECT COUNT(DISTINCT name) FROM participants")
        unique_names = cursor.fetchone()[0]
        
        # Participants added today
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("SELECT COUNT(*) FROM participants WHERE DATE(analyzed_at) = ?", (today,))
        added_today = cursor.fetchone()[0]
        
        # ERA participants
        cursor.execute("""
            SELECT COUNT(*) FROM participants 
            WHERE source_call_title LIKE '%ERA%' OR source_call_title LIKE '%Africa%'
        """)
        era_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total': total,
            'unique_names': unique_names,
            'added_today': added_today,
            'era_count': era_count
        }
    except Exception as e:
        # If participants table doesn't exist yet, return zeros
        return {
            'total': 0,
            'unique_names': 0,
            'added_today': 0,
            'era_count': 0,
            'error': str(e)
        }

def get_todays_calls(db_path):
    """Get calls added today from database"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute("""
        SELECT title, date, hyperlink, created_at
        FROM calls
        WHERE created_at LIKE ?
        ORDER BY created_at DESC
    """, (f'{today}%',))
    
    calls = cursor.fetchall()
    
    # Get total count
    cursor.execute("SELECT COUNT(*) as total FROM calls")
    total = cursor.fetchone()['total']
    
    # Get calls with public URLs from the calls table directly
    cursor.execute("""
        SELECT hyperlink, public_share_url
        FROM calls
        WHERE created_at LIKE ?
    """, (f'{today}%',))
    
    public_urls = {row['hyperlink']: row['public_share_url'] for row in cursor.fetchall() if row['public_share_url']}
    
    # Get last 5 calls (for context)
    cursor.execute("""
        SELECT title, date, hyperlink, created_at
        FROM calls
        ORDER BY created_at DESC
        LIMIT 5
    """)
    
    recent_calls = cursor.fetchall()
    
    # Get public URLs for recent calls from the calls table directly
    cursor.execute("""
        SELECT hyperlink, public_share_url
        FROM calls
        ORDER BY created_at DESC
        LIMIT 5
    """)
    
    recent_public_urls = {row['hyperlink']: row['public_share_url'] for row in cursor.fetchall() if row['public_share_url']}
    
    conn.close()
    
    return [dict(call) for call in calls], total, public_urls, [dict(call) for call in recent_calls], recent_public_urls

def build_report_body(cookie_info, calls, total_count, public_urls, recent_calls, recent_public_urls, health, participant_stats=None, backup_status=None):
    """Build the email body"""
    now = datetime.now().strftime('%b %d, %Y at %I:%M %p')
    
    # Header
    body = f"""Fathom Inventory Daily Report - {now}

"""
    
    # Account status
    account_correct = cookie_info['account'] == EXPECTED_ACCOUNT
    if account_correct:
        body += f"✅ Account: {cookie_info['account']} (correct)\n"
    else:
        body += f"❌ WRONG ACCOUNT: Using {cookie_info['account']}, expected {EXPECTED_ACCOUNT}\n"
    
    body += f"🔑 Cookie file: {cookie_info['file']}\n"
    body += f"\n"
    
    # Discovery summary
    body += f"""📊 DISCOVERY SUMMARY
- New calls found today: {len(calls)}
- Total calls in database: {total_count}
"""
    
    if cookie_info['age_days'] >= 0:
        body += f"- Cookie age: {int(cookie_info['age_days'])} days\n"
    
    body += "\n"
    
    # Backup status
    if backup_status and not backup_status.get('error'):
        body += f"""💾 BACKUP STATUS
"""
        if 'zip_backup' in backup_status:
            zip_info = backup_status['zip_backup']
            hours = int(zip_info['hours_ago'])
            if hours < 1:
                time_ago = f"{int(zip_info['hours_ago'] * 60)} minutes ago"
            elif hours < 24:
                time_ago = f"{hours} hours ago"
            else:
                time_ago = f"{hours // 24} days ago"
            body += f"- Local backup: {zip_info['time']} ({time_ago})\n"
            body += f"  Size: {zip_info['size_mb']:.1f}MB (CSV archive)\n"
            
            # Alert if backup is old
            if hours > 30:
                body += f"  ⚠️  Local backup is {hours // 24} days old!\n"
        
        # Google Drive backup status
        if 'drive_backup' in backup_status:
            drive_info = backup_status['drive_backup']
            if 'error' not in drive_info:
                hours = int(drive_info['hours_ago'])
                if hours < 1:
                    time_ago = f"{int(drive_info['hours_ago'] * 60)} minutes ago"
                elif hours < 24:
                    time_ago = f"{hours} hours ago"
                else:
                    time_ago = f"{hours // 24} days ago"
                body += f"- Google Drive: {drive_info['time']} ({time_ago})\n"
                body += f"  Size: {drive_info['size_mb']:.1f}MB\n"
                
                # Alert if Drive backup is old
                if hours > 30:
                    body += f"  ⚠️  Cloud backup is {hours // 24} days old!\n"
            else:
                body += f"- Google Drive: ⚠️  {drive_info['error']}\n"
        else:
            body += f"- Google Drive: Not configured yet\n"
        
        body += "\n"
    elif backup_status and backup_status.get('error'):
        body += f"""💾 BACKUP STATUS
⚠️  {backup_status['error']}

"""
    
    # Participant analysis stats (if available)
    if participant_stats and participant_stats.get('total', 0) > 0:
        body += f"""🤖 PARTICIPANT ANALYSIS
- Total participant records: {participant_stats['total']}
- Unique individuals: {participant_stats['unique_names']}
- ERA community members: {participant_stats['era_count']}
"""
        if participant_stats.get('added_today', 0) > 0:
            body += f"- New participants today: {participant_stats['added_today']}\n"
        body += "\n"
    
    # New calls with links
    if calls:
        body += f"""🆕 NEW CALLS ADDED ({len(calls)})

"""
        for i, call in enumerate(calls, 1):
            body += f"""{i}. "{call['title']}" ({call['date']})
   Fathom: {call['hyperlink']}
"""
            # Try to find public share URL
            public_url = public_urls.get(call['hyperlink'])
            if public_url:
                body += f"   Public: {public_url}\n"
            else:
                body += f"   Public: (pending - check after emails arrive)\n"
            body += "\n"
    else:
        body += "ℹ️  No new calls found today\n\n"
    
    # Alerts section
    alerts = []
    critical_alerts = []  # Separate critical from warnings
    
    # Check for authentication failures in logs
    auth_failed, auth_reason = check_recent_auth_failures()
    
    if auth_failed:
        critical_alerts.append(f"🔴 AUTHENTICATION FAILURE DETECTED: {auth_reason}")
        critical_alerts.append("   ACTION REQUIRED: Run ./scripts/refresh_fathom_auth.sh")
        critical_alerts.append("   → New calls cannot be discovered until cookies are refreshed")
    
    if not account_correct:
        critical_alerts.append(f"❌ Wrong account: Using {cookie_info['account']}, expected {EXPECTED_ACCOUNT}")
    
    if 'error' in cookie_info:
        critical_alerts.append(f"❌ Cookie error: {cookie_info['error']}")
    
    # Database health alerts
    if health['days_since_last_email'] > 2:
        if len(calls) == 0 and cookie_info['age_days'] > 3:
            # High confidence this is auth failure
            critical_alerts.append(f"🔴 SYSTEM NOT WORKING: Last email {health['days_since_last_email']} days old + zero new calls + stale cookies")
            critical_alerts.append("   → This strongly indicates authentication failure")
        else:
            alerts.append(f"⚠️  Last email is {health['days_since_last_email']} days old (last: {health.get('last_email_date', 'unknown')})")
    
    # Cookie age warnings
    if cookie_info['age_days'] > 7:
        alerts.append(f"⚠️  Cookies are {int(cookie_info['age_days'])} days old - refresh recommended")
    elif len(calls) == 0 and cookie_info['age_days'] > 3 and not auth_failed:
        alerts.append("⚠️  Zero new calls + cookies >3 days old (possible auth issue)")
    
    if health['percent_missing_urls'] > 20:
        alerts.append(f"⚠️  {health['calls_missing_urls']}/{health['total_calls']} calls ({health['percent_missing_urls']:.0f}%) missing public URLs")
        alerts.append("   → Date format mismatch or linking errors may be occurring")
    
    # Show critical alerts first with emphasis
    if critical_alerts:
        body += """🚨 CRITICAL ISSUES - IMMEDIATE ACTION REQUIRED

"""
        for alert in critical_alerts:
            body += f"{alert}\n"
        body += "\n"
    
    # Then regular alerts
    if alerts:
        body += """⚠️  WARNINGS

"""
        for alert in alerts:
            body += f"{alert}\n"
        body += "\n"
    
    # All clear message
    if not critical_alerts and not alerts:
        body += "✅ No issues detected\n\n"
    
    # Maintenance reminder
    if cookie_info['age_days'] >= 0:
        days_until_refresh = 7 - int(cookie_info['age_days'])
        if days_until_refresh <= 0:
            body += """📅 MAINTENANCE REQUIRED

Cookie refresh overdue! Run:
  ./scripts/refresh_fathom_auth.sh

"""
        elif days_until_refresh <= 2:
            body += f"""📅 MAINTENANCE REMINDER

Cookie refresh due in {days_until_refresh} days
Run: ./scripts/refresh_fathom_auth.sh

"""
    
    # Last 5 calls in database
    body += """📋 LAST 5 CALLS IN DATABASE

"""
    for i, call in enumerate(recent_calls, 1):
        body += f"""{i}. "{call['title']}" ({call['date']})
   Fathom: {call['hyperlink']}
"""
        # Try to find public share URL
        public_url = recent_public_urls.get(call['hyperlink'])
        if public_url:
            body += f"   Public: {public_url}\n"
        body += "\n"
    
    body += """---
Fathom Inventory System
Project: /Users/admin/Library/CloudStorage/Dropbox-EcoRestorationAllianceLLC/Jon Schull/CascadeProjects/ERA_Admin/FathomInventory
"""
    
    return body

def get_gmail_service():
    """Get authenticated Gmail API service"""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def send_email(subject, body, to_email):
    """Send email via Gmail API"""
    try:
        service = get_gmail_service()
        
        # Create message
        message = MIMEText(body)
        message['To'] = to_email
        message['From'] = to_email
        message['Subject'] = subject
        
        # Encode the message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        # Send via Gmail API
        send_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        print(f"✅ Email sent (Message ID: {send_message['id']})")
        return True
        
    except HttpError as error:
        print(f"❌ Gmail API error: {error}")
        # Fallback: Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'fathom_daily_report_{timestamp}.txt'
        with open(filename, 'w') as f:
            f.write(f"To: {to_email}\n")
            f.write(f"Subject: {subject}\n\n")
            f.write(body)
        print(f"📝 Report saved to {filename} instead")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        # Fallback: Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'fathom_daily_report_{timestamp}.txt'
        with open(filename, 'w') as f:
            f.write(f"To: {to_email}\n")
            f.write(f"Subject: {subject}\n\n")
            f.write(body)
        print(f"📝 Report saved to {filename} instead")
        return False

def main():
    # Change to project directory
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    os.chdir(project_dir)
    
    print("📧 Generating daily report...")
    
    # Gather information
    cookie_info = get_cookie_info()
    health = get_database_health()
    calls, total_count, public_urls, recent_calls, recent_public_urls = get_todays_calls(DB_FILE)
    participant_stats = get_participant_stats(DB_FILE)
    backup_status = get_backup_status()
    
    # Build report
    body = build_report_body(cookie_info, calls, total_count, public_urls, recent_calls, recent_public_urls, health, participant_stats, backup_status)
    
    # Determine subject based on status
    if len(calls) > 0:
        subject = f"Fathom Inventory: {len(calls)} new call(s) - {datetime.now().strftime('%b %d')}"
    else:
        subject = f"Fathom Inventory: No new calls - {datetime.now().strftime('%b %d')}"
    
    if cookie_info['account'] != EXPECTED_ACCOUNT:
        subject = "⚠️  " + subject + " (WRONG ACCOUNT)"
    elif health['days_since_last_email'] > 2:
        subject = "⚠️  " + subject + " (STALE DATA)"
    
    # Send email
    success = send_email(subject, body, REPORT_EMAIL)
    
    if success:
        print(f"✅ Daily report sent to {REPORT_EMAIL}")
    else:
        print(f"⚠️  Email failed, report saved to file")
    
    # Always print summary to console
    print("\n" + "="*60)
    print(body)
    print("="*60)

if __name__ == "__main__":
    main()
