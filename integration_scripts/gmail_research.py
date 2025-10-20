#!/usr/bin/env python3
"""
Gmail Research Tool for Phase 4B-2
Search Gmail for information about unknown Fathom participants
"""

import base64
import re
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

# Paths - Use separate token for jschull@gmail.com (not fathomizer)
SCRIPT_DIR = Path(__file__).parent
TOKEN_FILE = SCRIPT_DIR / "token_jschull.json"  # Separate token for research
CREDENTIALS_FILE = SCRIPT_DIR / "credentials.json"  # OAuth credentials


def get_gmail_service():
    """Get authenticated Gmail service."""
    if not TOKEN_FILE.exists():
        print(f"❌ No Gmail token found: {TOKEN_FILE}")
        print("Run FathomInventory Gmail script first to authenticate")
        return None
    
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
    return build('gmail', 'v1', credentials=creds)


def search_person_in_gmail(service, person_name, max_results=10, affiliation=None):
    """
    Search Gmail for emails mentioning a person.
    Returns: List of email snippets with context
    """
    print(f"\n🔍 Searching Gmail for: '{person_name}'")
    
    try:
        # Simple search strategy:
        # - Single names: NO quotes (catches "Karim" AND "Karim Camara")
        # - Full names: WITH quotes (exact "John Smith")
        # - Let user decide what's relevant from results
        
        name_parts = person_name.strip().split()
        
        if len(name_parts) == 1:
            # Single name: no quotes = broader match
            query = person_name
        else:
            # Full name: use quotes for exact phrase
            query = f'"{person_name}"'
        
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            print(f"   No emails found mentioning '{person_name}'")
            return []
        
        print(f"   Found {len(messages)} emails")
        
        # Get message details
        email_contexts = []
        for msg_ref in messages[:max_results]:
            msg = service.users().messages().get(
                userId='me',
                id=msg_ref['id'],
                format='full'
            ).execute()
            
            # Extract metadata
            subject = ''
            sender = ''
            date = ''
            
            for header in msg['payload']['headers']:
                if header['name'] == 'Subject':
                    subject = header['value']
                elif header['name'] == 'From':
                    sender = header['value']
                elif header['name'] == 'Date':
                    date = header['value']
            
            # Get snippet (Gmail provides this automatically)
            snippet = msg.get('snippet', '')
            
            # Try to get more body context
            body_preview = get_body_preview(msg, person_name)
            
            email_contexts.append({
                'subject': subject,
                'from': sender,
                'date': date,
                'snippet': snippet,
                'body_preview': body_preview,
                'message_id': msg['id']
            })
        
        return email_contexts
    
    except Exception as e:
        print(f"   ❌ Error searching Gmail: {e}")
        return []


def get_body_preview(msg, search_term, context_chars=200):
    """Extract a preview of the email body around the search term."""
    try:
        # Get body text
        body = ''
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                        break
        elif 'body' in msg['payload'] and 'data' in msg['payload']['body']:
            body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8', errors='ignore')
        
        if not body:
            return None
        
        # Find search term (case-insensitive)
        body_lower = body.lower()
        term_lower = search_term.lower()
        
        index = body_lower.find(term_lower)
        if index == -1:
            return None
        
        # Extract context around the term
        start = max(0, index - context_chars)
        end = min(len(body), index + len(search_term) + context_chars)
        
        preview = body[start:end].strip()
        
        # Clean up (remove excessive whitespace)
        preview = re.sub(r'\s+', ' ', preview)
        
        return preview
    
    except Exception:
        return None


def research_person(person_name, max_results=5, affiliation=None):
    """
    Main research function - searches Gmail and returns formatted summary.
    
    Returns dict with:
        - found: bool
        - email_count: int
        - contexts: list of email info
        - summary: formatted text summary
    """
    service = get_gmail_service()
    if not service:
        return {
            'found': False,
            'email_count': 0,
            'contexts': [],
            'summary': 'Gmail API not available'
        }
    
    contexts = search_person_in_gmail(service, person_name, max_results, affiliation)
    
    # Generate summary
    if not contexts:
        summary = f"❌ No emails found mentioning '{person_name}'"
    else:
        summary_lines = [f"✅ Found {len(contexts)} emails mentioning '{person_name}':\n"]
        
        for i, ctx in enumerate(contexts, 1):
            summary_lines.append(f"{i}. **{ctx['subject']}**")
            summary_lines.append(f"   From: {ctx['from']}")
            summary_lines.append(f"   Date: {ctx['date']}")
            
            if ctx['body_preview']:
                summary_lines.append(f"   Context: ...{ctx['body_preview']}...")
            else:
                summary_lines.append(f"   Snippet: {ctx['snippet']}")
            
            summary_lines.append("")
        
        summary = '\n'.join(summary_lines)
    
    return {
        'found': len(contexts) > 0,
        'email_count': len(contexts),
        'contexts': contexts,
        'summary': summary
    }


def research_multiple_people(names, max_per_person=3):
    """Research multiple people at once."""
    results = {}
    
    print("=" * 80)
    print("📧 GMAIL RESEARCH TOOL")
    print("=" * 80)
    
    for name in names:
        result = research_person(name, max_results=max_per_person)
        results[name] = result
        
        print()
        print(result['summary'])
        print("-" * 80)
    
    return results


# CLI interface
if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Search Gmail for information about people')
    parser.add_argument('name', help='Person name to search for')
    parser.add_argument('--affiliation', help='Optional affiliation/organization to narrow search', default=None)
    parser.add_argument('--max-results', type=int, default=5, help='Maximum number of emails to return')
    
    args = parser.parse_args()
    
    # Single person research
    result = research_person(args.name, max_results=args.max_results, affiliation=args.affiliation)
    
    print()
    print(result['summary'])
    
    print()
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    if result['found']:
        print(f"✅ {args.name}: {result['email_count']} emails")
    else:
        print(f"❌ {args.name}: No emails found")
