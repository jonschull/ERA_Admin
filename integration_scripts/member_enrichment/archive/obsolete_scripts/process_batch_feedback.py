#!/usr/bin/env python3
"""
Process human feedback from batch review file.

Reads batch review file, extracts approved/revised bios, queues for Airtable.
"""

import re
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
BATCH_REVIEW_DIR = SCRIPT_DIR / "batches" / "batch_reviews"
APPROVED_FILE = SCRIPT_DIR / "batches" / "approved_bios.md"

def extract_bio_sections(review_content):
    """Extract individual bio sections from review file."""
    
    # Split by ## 1., ## 2., etc
    pattern = r'^## \d+\. (.+?)$'
    sections = []
    
    lines = review_content.split('\n')
    current_section = None
    current_name = None
    current_lines = []
    
    for line in lines:
        match = re.match(pattern, line)
        if match:
            # Save previous section
            if current_name:
                sections.append({
                    'name': current_name,
                    'content': '\n'.join(current_lines)
                })
            # Start new section
            current_name = match.group(1).strip()
            current_lines = [line]
        else:
            current_lines.append(line)
    
    # Save last section
    if current_name:
        sections.append({
            'name': current_name,
            'content': '\n'.join(current_lines)
        })
    
    return sections

def parse_bio_section(section_content):
    """Parse a single bio section to extract status, bio, contact, etc."""
    
    lines = section_content.split('\n')
    
    result = {
        'status': 'PENDING',
        'bio': '',
        'char_count': 0,
        'email': '',
        'location': '',
        'affiliation': '',
        'phone': '',
        'affiliated_orgs': [],
        'data_concerns': '',
        'comments': ''
    }
    
    current_section = None
    bio_lines = []
    
    for line in lines:
        # Detect status
        if line.startswith('**STATUS:**'):
            status = line.split('**STATUS:**')[1].strip()
            result['status'] = status
        
        # Detect sections
        if line.startswith('### Bio'):
            current_section = 'bio'
            # Extract char count from "### Bio (835 chars)"
            match = re.search(r'\((\d+) chars\)', line)
            if match:
                result['char_count'] = int(match.group(1))
            continue
        elif line.startswith('### Contact Info'):
            current_section = 'contact'
            continue
        elif line.startswith('### Affiliated Orgs'):
            current_section = 'orgs'
            continue
        elif line.startswith('### Data Concerns'):
            current_section = 'concerns'
            continue
        elif line.startswith('### Comments'):
            current_section = 'comments'
            continue
        elif line.startswith('---'):
            current_section = None
            continue
        
        # Collect content by section
        if current_section == 'bio':
            if line.strip() and not line.startswith('**'):
                bio_lines.append(line)
        elif current_section == 'contact':
            if 'Email:' in line:
                result['email'] = line.split('Email:')[1].strip()
            elif 'Location:' in line:
                result['location'] = line.split('Location:')[1].strip()
            elif 'Affiliation:' in line:
                result['affiliation'] = line.split('Affiliation:')[1].strip()
            elif 'Phone:' in line:
                result['phone'] = line.split('Phone:')[1].strip()
        elif current_section == 'orgs':
            if line.startswith('- ') and not line.startswith('- ('):
                org = line[2:].strip()
                if org:
                    result['affiliated_orgs'].append(org)
        elif current_section == 'concerns':
            if line.strip() and not line.startswith('**'):
                result['data_concerns'] += line + '\n'
        elif current_section == 'comments':
            if line.strip() and not line.startswith('('):
                result['comments'] += line + '\n'
    
    result['bio'] = '\n'.join(bio_lines).strip()
    result['char_count'] = len(result['bio']) if not result['char_count'] else result['char_count']
    
    return result

def main():
    """Process batch feedback."""
    
    if len(sys.argv) < 2:
        print("Usage: python3 process_batch_feedback.py <batch_num>")
        print("Example: python3 process_batch_feedback.py 4")
        sys.exit(1)
    
    batch_num = sys.argv[1]
    review_file = BATCH_REVIEW_DIR / f"batch{batch_num}_review.md"
    
    if not review_file.exists():
        print(f"❌ Review file not found: {review_file}")
        sys.exit(1)
    
    print("=" * 80)
    print(f"PROCESSING BATCH {batch_num} FEEDBACK")
    print("=" * 80)
    print()
    
    with open(review_file) as f:
        content = f.read()
    
    sections = extract_bio_sections(content)
    
    print(f"Found {len(sections)} bio sections")
    print()
    
    approved = []
    needs_revision = []
    skipped = []
    
    for section in sections:
        parsed = parse_bio_section(section['content'])
        parsed['name'] = section['name']
        
        status = parsed['status']
        
        if 'APPROVED' in status:
            approved.append(parsed)
            print(f"✅ {section['name']}: APPROVED ({parsed['char_count']} chars)")
        elif 'NEEDS_REVISION' in status or 'REVISION' in status:
            needs_revision.append(parsed)
            print(f"📝 {section['name']}: NEEDS REVISION")
            if parsed['comments']:
                print(f"   Comments: {parsed['comments'][:100]}...")
        elif 'SKIP' in status:
            skipped.append(parsed)
            print(f"⏭️  {section['name']}: SKIPPED")
        else:
            print(f"⏳ {section['name']}: PENDING (not processed)")
    
    print()
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"✅ Approved: {len(approved)}")
    print(f"📝 Needs revision: {len(needs_revision)}")
    print(f"⏭️  Skipped: {len(skipped)}")
    print()
    
    if approved:
        # Add to approved_bios.md
        with open(APPROVED_FILE, 'a') as f:
            for bio_data in approved:
                f.write(f"\n## {bio_data['name']}\n\n")
                f.write(f"{bio_data['bio']}\n\n")
                f.write(f"**Character count:** {bio_data['char_count']}  \n")
                f.write(f"**Email:** {bio_data['email']}  \n")
                f.write(f"**Affiliated Orgs:** {', '.join(bio_data['affiliated_orgs'])}  \n")
                f.write(f"**Airtable ID:** (from database)  \n")
                f.write(f"\n---\n")
        
        print(f"✅ Added {len(approved)} bios to {APPROVED_FILE}")
        
        # Create queue file for Airtable update
        queue_file = BATCH_REVIEW_DIR / f"batch{batch_num}_queue.json"
        with open(queue_file, 'w') as f:
            json.dump(approved, f, indent=2)
        
        print(f"✅ Created Airtable queue: {queue_file.name}")
    
    if needs_revision:
        print()
        print("📝 NEEDS REVISION:")
        for bio_data in needs_revision:
            print(f"   - {bio_data['name']}: {bio_data['comments'][:60]}...")
    
    print()

if __name__ == "__main__":
    main()
