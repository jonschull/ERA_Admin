#!/usr/bin/env python3
"""
Query Participant Sessions by Name or Alias

PURPOSE:
    Easy command-line tool to find all sessions for a participant,
    handling aliases automatically (e.g., "bk" → Brian Kravitz).

USAGE:
    python query_participant_sessions.py "Brian Kravitz"
    python query_participant_sessions.py "bk"
    python query_participant_sessions.py --list-ambiguous

AUTHOR: ERA Admin / Cascade AI
DATE: 2025-10-25
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path("../FathomInventory/fathom_emails.db")


def find_sessions_by_name(name):
    """Find all sessions where person appeared (by any alias)"""
    
    conn = sqlite3.connect(DB_PATH)
    
    # Query the helper view
    results = conn.execute("""
        SELECT DISTINCT
            participant_name,
            appeared_as,
            meeting_date,
            meeting_title,
            meeting_url
        FROM participant_meetings
        WHERE participant_name LIKE ?
           OR appeared_as LIKE ?
        ORDER BY meeting_date DESC
    """, (f"%{name}%", f"%{name}%")).fetchall()
    
    conn.close()
    return results


def find_who_is_alias(alias):
    """Find who an alias refers to across all meetings"""
    
    conn = sqlite3.connect(DB_PATH)
    
    results = conn.execute("""
        SELECT 
            fathom_name,
            resolved_to,
            meeting_url,
            decision_type
        FROM fathom_alias_resolutions
        WHERE fathom_name LIKE ?
        ORDER BY resolved_to
    """, (f"%{alias}%",)).fetchall()
    
    conn.close()
    return results


def list_ambiguous_aliases():
    """List aliases that map to multiple people"""
    
    conn = sqlite3.connect(DB_PATH)
    
    results = conn.execute("""
        SELECT 
            fathom_name,
            GROUP_CONCAT(resolved_to, ', ') as people,
            COUNT(DISTINCT resolved_to) as person_count
        FROM (
            SELECT DISTINCT fathom_name, resolved_to
            FROM fathom_alias_resolutions
            WHERE resolved_to IS NOT NULL
        )
        GROUP BY fathom_name
        HAVING person_count > 1
        ORDER BY person_count DESC, fathom_name
    """).fetchall()
    
    conn.close()
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python query_participant_sessions.py 'Brian Kravitz'")
        print("  python query_participant_sessions.py 'bk'")
        print("  python query_participant_sessions.py --list-ambiguous")
        sys.exit(1)
    
    if sys.argv[1] == '--list-ambiguous':
        print("\n🔀 Ambiguous Aliases (same alias → multiple people):")
        print("="*70)
        results = list_ambiguous_aliases()
        for row in results:
            print(f"\n'{row[0]}' → {row[2]} people:")
            print(f"   {row[1]}")
        print(f"\nTotal: {len(results)} ambiguous aliases")
        return
    
    search_term = sys.argv[1]
    
    # Try as participant name first
    sessions = find_sessions_by_name(search_term)
    
    if sessions:
        print(f"\n🎥 Sessions for '{search_term}':")
        print("="*70)
        
        current_person = None
        for row in sessions:
            if row[0] != current_person:
                if current_person:
                    print()
                current_person = row[0]
                print(f"\n👤 {row[0]}:")
            
            date = row[2] or "Unknown date"
            appeared_as = f"appeared as '{row[1]}'" if row[1] != row[0] else "full name"
            title = row[3] or "Unknown meeting"
            url = row[4] or "(no URL)"
            
            print(f"   • {date}: {appeared_as}")
            if row[3]:
                print(f"     {title[:70]}")
            if row[4]:
                print(f"     {url}")
        
        print(f"\n✅ Found {len(sessions)} session(s)")
    
    # Also check as alias
    alias_results = find_who_is_alias(search_term)
    
    if alias_results:
        print(f"\n🏷️  Alias '{search_term}' resolutions:")
        print("="*70)
        
        for row in alias_results:
            resolved = row[1] or "(dropped)"
            url = row[2] or "Unknown meeting"
            print(f"   • {resolved}")
            if row[2]:
                print(f"     {url}")
        
        if not sessions:
            print(f"\n💡 Try searching for the resolved names above")


if __name__ == '__main__':
    main()
