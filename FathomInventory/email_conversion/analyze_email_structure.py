#!/usr/bin/env python3
"""
Analyze the structural patterns across all HTML email samples to confirm format consistency.
"""

import os
import re
from bs4 import BeautifulSoup
from collections import defaultdict

def analyze_html_structure(html_content, filename):
    """Analyze the structure of a single HTML file."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    analysis = {
        'filename': filename,
        'file_size': len(html_content),
        'title_elements': [],
        'fs24_elements': [],
        'maxw560_tables': 0,
        'action_items': False,
        'ai_notes_content': False,
        'view_meeting_links': 0,
        'ask_fathom_links': 0,
        'total_links': 0,
        'date_patterns': [],
        'meeting_duration': None,
        'main_title': None
    }
    
    # Find all fs-24 elements (main titles)
    fs24_elements = soup.find_all(lambda tag: tag.get('class') and 'fs-24' in tag.get('class', []))
    for elem in fs24_elements:
        text = elem.get_text(strip=True)
        analysis['fs24_elements'].append(text)
        if not analysis['main_title']:  # First fs-24 element is usually the main title
            analysis['main_title'] = text
    
    # Find maxw-560 tables (main content containers)
    maxw560_tables = soup.find_all('table', class_=lambda x: x and 'maxw-560' in x)
    analysis['maxw560_tables'] = len(maxw560_tables)
    
    # Check for action items
    action_items = soup.find(string=re.compile('Action Items', re.IGNORECASE))
    analysis['action_items'] = bool(action_items)
    
    # Check for AI notes content
    ai_content = soup.find('div', class_='ai_notes_html_content')
    analysis['ai_notes_content'] = bool(ai_content)
    
    # Count links
    all_links = soup.find_all('a', href=True)
    analysis['total_links'] = len(all_links)
    
    for link in all_links:
        href = link.get('href', '')
        if 'View Meeting' in link.get_text():
            analysis['view_meeting_links'] += 1
        elif 'Ask Fathom' in link.get_text():
            analysis['ask_fathom_links'] += 1
    
    # Find date patterns
    date_patterns = re.findall(r'[A-Z][a-z]+\s+\d+,\s+\d{4}', html_content)
    analysis['date_patterns'] = list(set(date_patterns))
    
    # Find meeting duration
    duration_match = re.search(r'(\d+)\s*mins?', html_content)
    if duration_match:
        analysis['meeting_duration'] = duration_match.group(1) + ' mins'
    
    return analysis

def analyze_all_samples():
    """Analyze all HTML samples in current directory."""
    samples_dir = "."  # Current directory (email_conversion)
    
    print(f"Analyzing HTML samples in current directory...")
    
    print("=" * 100)
    print("STRUCTURAL ANALYSIS OF EMAIL SAMPLES")
    print("=" * 100)
    
    analyses = []
    
    # Analyze each HTML file
    for i in range(1, 11):  # Skip 0.html as it's not from database
        html_file = os.path.join(samples_dir, f"{i}.html")
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            analysis = analyze_html_structure(html_content, f"{i}.html")
            analyses.append(analysis)
    
    if not analyses:
        print("No HTML files found to analyze.")
        return
    
    # Display individual analysis
    print("\nINDIVIDUAL FILE ANALYSIS:")
    print("-" * 100)
    
    for analysis in analyses:
        print(f"\n📄 {analysis['filename']}:")
        print(f"   Size: {analysis['file_size']:,} bytes")
        print(f"   Main Title: '{analysis['main_title']}'")
        print(f"   Date(s): {', '.join(analysis['date_patterns'])}")
        print(f"   Duration: {analysis['meeting_duration']}")
        print(f"   Total Links: {analysis['total_links']}")
        print(f"   View Meeting Links: {analysis['view_meeting_links']}")
        print(f"   Ask Fathom Links: {analysis['ask_fathom_links']}")
        print(f"   Action Items: {'✅' if analysis['action_items'] else '❌'}")
        print(f"   AI Notes Content: {'✅' if analysis['ai_notes_content'] else '❌'}")
        print(f"   maxw-560 Tables: {analysis['maxw560_tables']}")
    
    # Structural consistency analysis
    print("\n" + "=" * 100)
    print("STRUCTURAL CONSISTENCY ANALYSIS")
    print("=" * 100)
    
    # Check consistency patterns
    file_sizes = [a['file_size'] for a in analyses]
    main_titles = [a['main_title'] for a in analyses]
    total_links = [a['total_links'] for a in analyses]
    maxw560_counts = [a['maxw560_tables'] for a in analyses]
    action_items_count = sum(1 for a in analyses if a['action_items'])
    ai_content_count = sum(1 for a in analyses if a['ai_notes_content'])
    
    print(f"\n📊 SUMMARY STATISTICS:")
    print(f"   Files analyzed: {len(analyses)}")
    print(f"   File size range: {min(file_sizes):,} - {max(file_sizes):,} bytes")
    print(f"   Average file size: {sum(file_sizes)//len(file_sizes):,} bytes")
    print(f"   Link count range: {min(total_links)} - {max(total_links)}")
    print(f"   Average links: {sum(total_links)//len(total_links)}")
    print(f"   Files with Action Items: {action_items_count}/{len(analyses)}")
    print(f"   Files with AI Notes Content: {ai_content_count}/{len(analyses)}")
    
    print(f"\n🏗️  STRUCTURAL ELEMENTS:")
    print(f"   maxw-560 tables per file: {set(maxw560_counts)}")
    
    # Title pattern analysis
    print(f"\n📝 TITLE PATTERNS:")
    title_patterns = defaultdict(int)
    for title in main_titles:
        if not title:
            title_patterns['[NO TITLE]'] += 1
        elif ' from ' in title:
            title_patterns['Contains "from"'] += 1
        elif ' / ' in title:
            title_patterns['Contains " / " (name separator)'] += 1
        elif ' — ' in title:
            title_patterns['Contains " — " (em dash)'] += 1
        elif 'Meeting' in title:
            title_patterns['Contains "Meeting"'] += 1
        else:
            title_patterns['Other format'] += 1
    
    for pattern, count in title_patterns.items():
        print(f"   {pattern}: {count} files")
    
    # Consistency check
    print(f"\n✅ CONSISTENCY CHECK:")
    
    # Check if all have same basic structure
    all_have_maxw560 = all(count > 0 for count in maxw560_counts)
    all_have_links = all(count > 0 for count in total_links)
    all_have_titles = all(title for title in main_titles)
    
    print(f"   All files have maxw-560 tables: {'✅' if all_have_maxw560 else '❌'}")
    print(f"   All files have links: {'✅' if all_have_links else '❌'}")
    print(f"   All files have main titles: {'✅' if all_have_titles else '❌'}")
    
    # Structural uniformity
    maxw560_uniform = len(set(maxw560_counts)) == 1
    print(f"   Uniform maxw-560 table count: {'✅' if maxw560_uniform else '❌'}")
    
    if not maxw560_uniform:
        print(f"      Different counts found: {set(maxw560_counts)}")
    
    print(f"\n💡 CONVERTER IMPLICATIONS:")
    if all_have_maxw560 and all_have_titles:
        print("   ✅ All files have basic required structure for conversion")
        if not any(' from ' in title for title in main_titles):
            print("   ⚠️  NO files contain 'from' in title - current converter will fail on all")
        print("   📝 Need to update converter to handle actual title patterns")
    else:
        print("   ❌ Structural inconsistencies found - need deeper investigation")

if __name__ == '__main__':
    analyze_all_samples()
