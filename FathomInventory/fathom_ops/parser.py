"""Parsing helpers for extracting call records from Fathom HTML."""
from __future__ import annotations

from typing import List, Dict, Set
from bs4 import BeautifulSoup


def parse_for_new_calls(html_content: str, existing_hyperlinks: Set[str]) -> List[Dict[str, str]]:
    """Return list of new meetings found in page HTML.

    Each record: {Title, Date, Duration, Hyperlink}
    - Hyperlink is absolute (https://fathom.video/...)
    - Records with hyperlinks already in existing_hyperlinks are skipped
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    new_meetings: List[Dict[str, str]] = []
    for card in soup.find_all('call-gallery-thumbnail'):
        link_element = card.find('a', href=True)
        hyperlink = (
            "https://fathom.video" + link_element['href']
            if link_element and not link_element['href'].startswith('http')
            else (link_element['href'] if link_element else None)
        )
        if hyperlink and hyperlink not in existing_hyperlinks:
            title = (
                card.find('call-gallery-thumbnail-title').get_text(strip=True)
                if card.find('call-gallery-thumbnail-title') else ""
            )
            date = (
                card.find('li', class_='opacity-70').get_text(strip=True)
                if card.find('li', class_='opacity-70') else "Unknown Date"
            )
            duration = (
                card.find('span', class_='font-semibold').get_text(strip=True)
                if card.find('span', class_='font-semibold') else ""
            )
            new_meetings.append({
                'Title': title,
                'Date': date,
                'Duration': duration,
                'Hyperlink': hyperlink,
            })
    return new_meetings
