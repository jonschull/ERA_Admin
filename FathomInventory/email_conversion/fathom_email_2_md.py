#!/usr/bin/env python3
"""
Straightforward HTML-to-Markdown converter for actual database email structure.
Works with all database emails regardless of title format.
Supports both file-based and database batch conversion.
"""

import re
import os
import json
import sqlite3
from bs4 import BeautifulSoup

def get_text_and_link(element):
    """Extracts text and a single hyperlink from a BeautifulSoup element if one exists."""
    if not element:
        return None, None
    text = element.get_text(" ", strip=True)
    link_tag = element.find('a', href=True)
    if link_tag:
        return text, link_tag['href']
    return text, None

def convert_html_to_markdown(html_content, extract_stats=False):
    """Convert database email HTML to Markdown following the specification.
    
    Args:
        html_content: HTML content to convert
        extract_stats: If True, also return extraction statistics
        
    Returns:
        If extract_stats=False: markdown string
        If extract_stats=True: (markdown string, stats dict)
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    md_lines = []
    
    # Initialize statistics tracking
    stats = {
        'meeting_title': None,
        'meeting_date': None,
        'meeting_duration_mins': None,
        'meeting_url': None,
        'ask_fathom_url': None,
        'action_items_count': 0,
        'topics_count': 0,
        'key_takeaways_count': 0,
        'topic_subsections_count': 0,
        'next_steps_count': 0,
        'total_links_count': 0,
        'fathom_timestamp_links_count': 0,
        'parsing_success': True,
        'parsing_errors': []
    }

    # Find the main title (fs-24 class) - works for any title format
    main_title_tag = soup.find('td', class_=lambda x: x and 'fs-24' in x)
    if not main_title_tag:
        return "# Error: Could not find main title. Conversion failed."
    
    main_title = main_title_tag.get_text(strip=True)
    stats['meeting_title'] = main_title
    
    # Find the main container (maxw-560 table)
    main_container = main_title_tag.find_parent('table', class_=lambda x: x and 'maxw-560' in x)
    if not main_container:
        error_msg = "# Error: Could not find main content container. Conversion failed."
        if extract_stats:
            stats['parsing_success'] = False
            stats['parsing_errors'].append("Could not find main content container")
            return error_msg, stats
        return error_msg

    # 1. Header: Subtitle and Main Title
    md_lines.append("*Meeting with Enabling The Future*\n")
    md_lines.append(f"# {main_title}\n")

    # 2. Find metadata line (date, duration, links) - format cleanly
    date_tag = main_container.find(lambda tag: re.search(r'\w+\s+\d+,\s+\d{4}', tag.get_text()))
    if date_tag:
        date_text = date_tag.get_text(separator=" ", strip=True)
        
        # Extract date and normalize to ISO format
        date_match = re.search(r'(\w+\s+\d+,\s+\d{4})', date_text)
        date_str = date_match.group(1) if date_match else ""
        if date_str:
            # Normalize to ISO format (YYYY-MM-DD)
            try:
                from datetime import datetime
                dt = datetime.strptime(date_str, '%B %d, %Y')  # "October 09, 2025"
                stats['meeting_date'] = dt.strftime('%Y-%m-%d')  # "2025-10-09"
            except ValueError:
                # If parsing fails, keep original
                stats['meeting_date'] = date_str
        
        # Extract duration
        duration_match = re.search(r'(\d+)\s*mins?', date_text)
        duration_str = f"{duration_match.group(1)} mins" if duration_match else ""
        if duration_match:
            stats['meeting_duration_mins'] = int(duration_match.group(1))
        
        # Get links - prioritize /share/ URLs over /calls/ URLs
        view_link_tag = date_tag.find('a', string=re.compile("View Meeting"))
        ask_link_tag = date_tag.find('a', string=re.compile("Ask Fathom"))
        
        # Capture URLs for stats - prefer /share/ URLs (public) over /calls/ URLs (require login)
        if view_link_tag:
            view_url = view_link_tag.get('href')
            # Prefer /share/ URL if available, otherwise use /calls/
            if view_url and '/share/' in view_url:
                stats['meeting_url'] = view_url
            elif view_url:
                # Store /calls/ URL temporarily, may be overridden by /share/ if found
                stats['meeting_url'] = view_url
        
        if ask_link_tag:
            ask_url = ask_link_tag.get('href')
            stats['ask_fathom_url'] = ask_url
            # If ask_fathom_url is a /share/ URL and we only have /calls/ for meeting_url, use it
            if ask_url and '/share/' in ask_url and stats.get('meeting_url') and '/calls/' in stats.get('meeting_url'):
                stats['meeting_url'] = ask_url
        
        # Format cleanly
        metadata_parts = []
        if date_str:
            metadata_parts.append(f"**Date:** {date_str}")
        if duration_str:
            metadata_parts.append(f"**Duration:** {duration_str}")
        
        if metadata_parts:
            md_lines.append(" | ".join(metadata_parts) + "\n")
        
        # Links on separate line
        if view_link_tag and ask_link_tag:
            md_lines.append(f"**Links:** [View Meeting]({view_link_tag['href']}) | [Ask Fathom]({ask_link_tag['href']})\n")

    # 3. Action Items
    action_items_header = main_container.find('td', class_=lambda x: x and 'fs-20' in x, 
                                            string=re.compile('Action Items', re.IGNORECASE))
    if action_items_header:
        md_lines.append("## ACTION ITEMS ✨\n")
        header_row = action_items_header.find_parent('tr')
        if header_row:
            items_container_row = header_row.find_next_sibling('tr')
            if items_container_row:
                # Find action item links directly (they're in <a> tags, not <span> tags)
                action_links = items_container_row.find_all('a', href=lambda x: x and 'action_item' in x)
                stats['action_items_count'] = len(action_links)
                
                for link in action_links:
                    text = link.get_text(strip=True)
                    href = link.get('href')
                    if text and href:
                        md_lines.append(f"- [ ] [{text}]({href})")
                        
                        # Look for assignee in the same table/container as the link
                        link_table = link.find_parent('table')
                        if link_table:
                            assignee_tag = link_table.find('td', class_=lambda x: x and 'lh-17' in x)
                            if assignee_tag:
                                assignee = assignee_tag.get_text(strip=True)
                                if assignee and assignee != text:  # Don't duplicate the action text
                                    md_lines.append(f"  *{assignee}*")
        md_lines.append("\n")

    # 4. Main Content Sections (AI Notes)
    summary_container = main_container.find('div', class_='ai_notes_html_content')
    if summary_container:
        for element in summary_container.find_all(['h2', 'h3', 'ul'], recursive=False):
            if element.name == 'h2':
                section_title = element.get_text(strip=True)
                md_lines.append(f"## {section_title}\n")
                
                # Count sections for stats
                if 'next steps' in section_title.lower():
                    # Count next steps items in following ul
                    next_ul = element.find_next_sibling('ul')
                    if next_ul:
                        stats['next_steps_count'] = len(next_ul.find_all('li'))
                elif 'key takeaways' in section_title.lower():
                    # Count Key Takeaways bullet points
                    next_ul = element.find_next_sibling('ul')
                    if next_ul:
                        stats['key_takeaways_count'] = len(next_ul.find_all('li'))
                elif 'topics' in section_title.lower():
                    # Count h3 subsections under Topics
                    h3_count = 0
                    current = element.find_next_sibling()
                    while current and current.name != 'h2':
                        if current.name == 'h3':
                            h3_count += 1
                        current = current.find_next_sibling()
                    stats['topic_subsections_count'] = h3_count
                    
                # For backward compatibility, set topics_count to the sum
                stats['topics_count'] = stats['key_takeaways_count'] + stats['topic_subsections_count']
                        
            elif element.name == 'h3':
                md_lines.append(f"### {element.get_text(strip=True)}\n")
            elif element.name == 'ul':
                for li in element.find_all('li'):
                    text, link = get_text_and_link(li)
                    if text:
                        md_lines.append(f"- [{text}]({link})" if link else f"- {text}")
                md_lines.append("\n")

    # Final statistics: count all links in the generated markdown
    final_md = "\n".join(md_lines)
    
    # Count total links in markdown
    total_links = len(re.findall(r'\[([^\]]+)\]\([^\)]+\)', final_md))
    stats['total_links_count'] = total_links
    
    # Count fathom timestamp links
    timestamp_links = len(re.findall(r'\[([^\]]+)\]\([^)]*fathom\.video[^)]*timestamp=[^)]*\)', final_md))
    stats['fathom_timestamp_links_count'] = timestamp_links

    if extract_stats:
        return final_md, stats
    else:
        return final_md

def convert_file(input_file, output_file, extract_stats=False):
    """Convert a single HTML file to Markdown and optionally extract statistics."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        if extract_stats:
            result, stats = convert_html_to_markdown(html_content, extract_stats=True)
        else:
            result = convert_html_to_markdown(html_content)
            stats = None
        
        # Apply timestamp fix
        result = result.replace('×tamp=', '&timestamp=')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        
        # Save stats if requested
        if extract_stats and stats:
            stats_file = output_file.replace('.md', '_stats.json')
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2)
        
        # Count links
        link_count = len(re.findall(r'\[([^\]]+)\]\([^\)]+\)', result))
        
        if extract_stats:
            return True, link_count, result[:100] + "..." if len(result) > 100 else result, stats
        else:
            return True, link_count, result[:100] + "..." if len(result) > 100 else result
    
    except Exception as e:
        if extract_stats:
            return False, 0, str(e), None
        else:
            return False, 0, str(e)

if __name__ == "__main__":
    # Test on a single file
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = input_file.replace('.html', '_converted.md')
        
        # Check if --stats flag is provided
        extract_stats = '--stats' in sys.argv
        
        if extract_stats:
            success, links, preview, stats = convert_file(input_file, output_file, extract_stats=True)
        else:
            success, links, preview = convert_file(input_file, output_file)
        
        if success:
            print(f"✅ Converted {input_file} -> {output_file}")
            print(f"📊 Found {links} links")
            print(f"📄 Preview: {preview}")
            
            if extract_stats and stats:
                stats_file = output_file.replace('.md', '_stats.json')
                print(f"📈 Stats saved to: {stats_file}")
                print(f"📋 Quick stats: {stats['action_items_count']} actions, {stats['topics_count']} topics, {stats['next_steps_count']} next steps")
        else:
            print(f"❌ Failed to convert {input_file}: {preview}")
    else:
        print("Usage: python3 fathom_email_2_md.py <input.html> [--stats]")
        print("Example: python3 fathom_email_2_md.py 1.html --stats")
