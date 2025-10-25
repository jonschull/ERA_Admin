#!/usr/bin/env python3
"""
Generate Actionable HTML for Town Hall participant member review.

This is an instance of the "Actionable HTML" pattern:
- Show data with rich context
- Provide links to evidence
- Enable human decisions via UI
- Export decisions to CSV

Usage:
    python3 generate_member_review_html.py
    
Output:
    member_review_YYYYMMDD_HHMM.html
"""

import sqlite3
from datetime import datetime
import os
import sys

# Gmail API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Get authenticated Gmail API service."""
    creds = None
    token_path = '/Users/admin/ERA_Admin/FathomInventory/token.json'
    creds_path = '/Users/admin/ERA_Admin/FathomInventory/credentials.json'
    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, GMAIL_SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, GMAIL_SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'Gmail API error: {error}')
        return None


def search_gmail_for_person(service, person_name):
    """
    Search Gmail for emails involving a person.
    Returns: (message_count, thread_count, sample_emails)
    """
    if not service:
        return (0, 0, [])
    
    try:
        # Search for person's name in from/to/cc
        query = f'from:"{person_name}" OR to:"{person_name}" OR cc:"{person_name}"'
        
        # Get message list
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=10  # Get up to 10 for sample
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            return (0, 0, [])
        
        # Get actual message count (could be more than 10)
        result_size = results.get('resultSizeEstimate', len(messages))
        
        # Get thread IDs to count unique threads
        threads = set()
        sample_emails = []
        
        for msg in messages[:5]:  # Get details for first 5
            msg_data = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'To', 'Subject', 'Date']
            ).execute()
            
            thread_id = msg_data.get('threadId')
            if thread_id:
                threads.add(thread_id)
            
            # Extract headers
            headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}
            
            sample_emails.append({
                'id': msg['id'],
                'thread_id': thread_id,
                'from': headers.get('From', ''),
                'to': headers.get('To', ''),
                'subject': headers.get('Subject', ''),
                'date': headers.get('Date', '')
            })
        
        return (result_size, len(threads), sample_emails)
        
    except HttpError as error:
        print(f'Error searching for {person_name}: {error}')
        return (0, 0, [])


def get_non_member_th_participants():
    """Get Town Hall participants who aren't marked as ERA members."""
    db_path = '/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Get all non-members who attended Town Halls
    # Include their organization, Airtable data, and meeting info
    cur.execute("""
        SELECT DISTINCT
            p.id,
            p.name,
            p.affiliation,
            p.email,
            p.airtable_id,
            p.validated_by_airtable,
            p.source_call_url,
            p.source_call_title,
            p.call_hyperlink
        FROM participants p
        WHERE p.source_call_title LIKE '%Town Hall%'
          AND (p.era_member IS NULL OR p.era_member = 0)
        ORDER BY p.validated_by_airtable DESC, p.name
    """)
    
    participants = cur.fetchall()
    
    # For each participant, get additional context
    enriched = []
    for pid, name, affiliation, email, airtable_id, validated, call_url, call_title, call_hyperlink in participants:
        # Get the specific Town Hall meeting they attended
        # Match by hyperlink (unique per call), not title (can be duplicate)
        cur.execute("""
            SELECT DISTINCT c.title, c.hyperlink, c.date, c.public_share_url
            FROM calls c
            WHERE c.hyperlink = ?
              AND c.title LIKE '%Town Hall%'
            LIMIT 1
        """, (call_hyperlink,))
        
        meetings = cur.fetchall()
        
        enriched.append({
            'id': pid,
            'name': name,
            'affiliation': affiliation or '',
            'email': email or '',
            'airtable_id': airtable_id or '',
            'validated': validated,
            'meetings': meetings,
            'email_data': None,  # Will be filled by Gmail search
            'call_url': call_url,
            'call_title': call_title,
            'call_hyperlink': call_hyperlink
        })
    
    conn.close()
    return enriched


def generate_html(participants):
    """Generate interactive HTML review table."""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    filename = f'member_review_{timestamp}.html'
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Town Hall Participant Member Review</title>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        h1 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        .stats {{
            color: #666;
            font-size: 14px;
        }}
        .controls {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        button {{
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-right: 10px;
        }}
        button:hover {{
            background: #0056b3;
        }}
        button.secondary {{
            background: #6c757d;
        }}
        button.secondary:hover {{
            background: #545b62;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        th {{
            background: #f8f9fa;
            padding: 12px 8px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #dee2e6;
            cursor: pointer;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        th:hover {{
            background: #e9ecef;
        }}
        td {{
            padding: 12px 8px;
            border-bottom: 1px solid #dee2e6;
            vertical-align: top;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .validated {{
            color: #28a745;
            font-weight: 600;
        }}
        .not-validated {{
            color: #dc3545;
        }}
        a {{
            color: #007bff;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .meetings {{
            font-size: 12px;
            color: #666;
        }}
        .meeting-item {{
            margin: 4px 0;
            padding: 4px;
            background: #f8f9fa;
            border-radius: 3px;
        }}
        .email-count {{
            font-weight: 600;
            color: #007bff;
        }}
        input[type="checkbox"] {{
            width: 18px;
            height: 18px;
            cursor: pointer;
        }}
        input[type="text"] {{
            width: 100%;
            padding: 4px;
            border: 1px solid #ddd;
            border-radius: 3px;
            font-size: 12px;
        }}
        .check-all {{
            margin-left: 10px;
            font-size: 14px;
        }}
    </style>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <div class="header">
        <h1>🎯 Town Hall Participant Member Review</h1>
        <div class="stats">
            <strong>{len(participants)}</strong> non-member Town Hall participants to review
            <br>Review organizational affiliations and participation patterns to decide membership status
        </div>
        <div style="margin-top: 10px; color: #666; font-size: 13px;">
            <strong>Pattern:</strong> Actionable HTML - Rich context + Human decisions + CSV export
        </div>
    </div>
    
    <div class="controls">
        <button onclick="exportToCSV()">📥 Export Decisions to CSV</button>
        <button class="secondary" onclick="checkAll()">☑️ Check All</button>
        <button class="secondary" onclick="uncheckAll()">☐ Uncheck All</button>
        <span style="margin-left: 20px; color: #666;">
            Selected: <strong id="selectedCount">0</strong> / {len(participants)}
        </span>
    </div>
    
    <table id="reviewTable">
        <thead>
            <tr>
                <th onclick="sortTable(0)">✓ Make<br>Member</th>
                <th onclick="sortTable(1)">Name</th>
                <th onclick="sortTable(2)">Status</th>
                <th onclick="sortTable(3)">Organization</th>
                <th onclick="sortTable(4)">TH Attendance</th>
                <th onclick="sortTable(5)">Email<br>History</th>
                <th onclick="sortTable(6)">Contact Info</th>
                <th onclick="sortTable(7)">Notes</th>
            </tr>
        </thead>
        <tbody>
"""
    
    for p in participants:
        validated_class = 'validated' if p['validated'] else 'not-validated'
        validated_text = '✅ Validated' if p['validated'] else '⏳ Not Validated'
        
        # Build meetings list
        meetings_html = ''
        if p['meetings']:
            for title, hyperlink, date, share_url in p['meetings']:
                fathom_link = share_url or hyperlink or '#'
                date_str = date or 'Unknown date'
                meetings_html += f'<div class="meeting-item">📅 {date_str} - <a href="{fathom_link}" target="_blank">View Recording</a></div>'
        else:
            meetings_html = '<div class="meeting-item">No meeting details</div>'
        
        # Build email column with counts and samples
        gmail_search = f"https://mail.google.com/mail/u/0/#search/{p['name'].replace(' ', '+')}"
        
        email_html = ''
        if p['email_data']:
            msg_count = p['email_data']['message_count']
            thread_count = p['email_data']['thread_count']
            samples = p['email_data']['sample_emails']
            
            if msg_count > 0:
                email_html = f'<div style="font-weight: 600; color: #007bff;">{msg_count} messages ({thread_count} threads)</div>'
                email_html += f'<div style="font-size: 11px; margin-top: 4px;"><a href="{gmail_search}" target="_blank">🔍 View in Gmail</a></div>'
                
                if samples:
                    email_html += '<div style="margin-top: 6px; font-size: 10px; color: #666;">'
                    for email in samples[:3]:
                        subject = email['subject'][:40] + '...' if len(email['subject']) > 40 else email['subject']
                        date = email['date'][:16] if email['date'] else 'No date'
                        email_html += f'<div style="padding: 2px 0; border-top: 1px solid #eee;">• {subject}</div>'
                    if len(samples) > 3:
                        email_html += f'<div style="padding: 2px 0;">... and {msg_count - 3} more</div>'
                    email_html += '</div>'
            else:
                email_html = f'<div style="color: #999;">No emails</div><div style="font-size: 11px;"><a href="{gmail_search}" target="_blank">🔍 Search Gmail</a></div>'
        else:
            email_html = f'<a href="{gmail_search}" target="_blank">📧 Search Gmail</a>'
        
        # Build research links
        research_html = ''
        if p['email']:
            research_html += f"<span style='font-size: 11px; color: #666;'>{p['email']}</span><br>"
        
        if p['airtable_id']:
            research_html += f"<a href='https://airtable.com' target='_blank'>🗃️ Airtable</a>"
        
        if not research_html:
            research_html = '<span style="color: #999;">No data</span>'
        
        # Organization with link if available
        org_html = p['affiliation'] or '<span style="color: #999;">No affiliation</span>'
        
        html += f"""
            <tr data-pid="{p['id']}" data-name="{p['name']}">
                <td style="text-align: center;">
                    <input type="checkbox" class="make-member" onchange="updateCount()">
                </td>
                <td><strong>{p['name']}</strong></td>
                <td class="{validated_class}">{validated_text}</td>
                <td>{org_html}</td>
                <td><div class="meetings">{meetings_html}</div></td>
                <td style="font-size: 12px;">{email_html}</td>
                <td style="font-size: 12px;">{research_html}</td>
                <td><input type="text" class="notes" placeholder="Optional notes..."></td>
            </tr>
        """
    
    html += """
        </tbody>
    </table>
    
    <script>
        // Update selected count
        function updateCount() {
            const checked = $('.make-member:checked').length;
            $('#selectedCount').text(checked);
        }
        
        // Check all
        function checkAll() {
            $('.make-member').prop('checked', true);
            updateCount();
        }
        
        // Uncheck all
        function uncheckAll() {
            $('.make-member').prop('checked', false);
            updateCount();
        }
        
        // Sort table
        let sortDirection = {};
        function sortTable(columnIndex) {
            const table = document.getElementById('reviewTable');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            
            sortDirection[columnIndex] = !sortDirection[columnIndex];
            const ascending = sortDirection[columnIndex];
            
            rows.sort((a, b) => {
                let aVal = a.cells[columnIndex].textContent.trim();
                let bVal = b.cells[columnIndex].textContent.trim();
                
                // Handle numeric columns
                if (columnIndex === 5) { // Email count
                    aVal = parseInt(aVal) || 0;
                    bVal = parseInt(bVal) || 0;
                }
                
                if (aVal < bVal) return ascending ? -1 : 1;
                if (aVal > bVal) return ascending ? 1 : -1;
                return 0;
            });
            
            rows.forEach(row => tbody.appendChild(row));
        }
        
        // Export to CSV
        function exportToCSV() {
            let csv = 'participant_id,name,make_member,notes\\n';
            
            $('#reviewTable tbody tr').each(function() {
                const pid = $(this).data('pid');
                const name = $(this).data('name');
                const makeMember = $(this).find('.make-member').is(':checked') ? '1' : '0';
                const notes = $(this).find('.notes').val().replace(/,/g, ';').replace(/"/g, '\\"');
                
                csv += `${pid},"${name}",${makeMember},"${notes}"\\n`;
            });
            
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'member_review_decisions_""" + timestamp + """.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            alert('CSV exported! Check your downloads folder.');
        }
        
        // Initialize count
        $(document).ready(function() {
            updateCount();
        });
    </script>
</body>
</html>
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return filename


def main():
    print("🔍 Fetching Town Hall participants who aren't ERA members...")
    participants = get_non_member_th_participants()
    
    print(f"📊 Found {len(participants)} participants to review")
    print(f"   - {sum(1 for p in participants if p['validated'])} validated")
    print(f"   - {sum(1 for p in participants if not p['validated'])} not yet validated")
    print()
    
    print("📧 Connecting to Gmail API...")
    gmail_service = get_gmail_service()
    
    if gmail_service:
        print(f"📨 Searching Gmail for {len(participants)} participants...")
        print("   (This may take a few minutes...)")
        
        for i, p in enumerate(participants, 1):
            if i % 20 == 0:
                print(f"   ... processed {i}/{len(participants)}")
            
            msg_count, thread_count, emails = search_gmail_for_person(gmail_service, p['name'])
            p['email_data'] = {
                'message_count': msg_count,
                'thread_count': thread_count,
                'sample_emails': emails
            }
        
        print(f"   ✅ Gmail search complete!")
    else:
        print("   ⚠️  Gmail API unavailable - will show links only")
    print()
    
    print("🎨 Generating Actionable HTML...")
    filename = generate_html(participants)
    
    print(f"✅ Generated: {filename}")
    print()
    print("📖 Next steps:")
    print(f"   1. Open {filename} in your browser")
    print("   2. Review each participant:")
    print("      - Check organizational affiliations")
    print("      - Review Town Hall attendance patterns")
    print("      - See email message/thread counts (queried from Gmail)")
    print("      - View sample email subjects")
    print("   3. Check 'Make Member' for participants who should be ERA members")
    print("   4. Add notes for any edge cases or questions")
    print("   5. Click 'Export Decisions to CSV'")
    print("   6. Pass CSV back to Claude to process decisions")
    print()
    print("💡 This is an 'Actionable HTML' - a pattern for human-AI collaboration")
    print("   Gmail API queried: Actual message counts, not just links!")
    
    # Open in browser
    import subprocess
    subprocess.run(['open', filename])


if __name__ == '__main__':
    main()
