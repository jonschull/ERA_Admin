#!/usr/bin/env python3
"""
Detect Participant Redundancies in Database

PURPOSE:
    Find potential duplicate/redundant participant records that should
    likely be merged. Uses multiple detection strategies.

DETECTION STRATEGIES:
    1. Same name with/without (N) suffixes: "Ana Calderon" vs "Ana Calderon (3)"
    2. Case differences: "Chris Searles" vs "Chris searles"
    3. Similar names: "Christopher Danch" vs "Christopher P Danch"
    4. First name only vs full name: "Ana" vs "Ana Calderon"
    5. Alias resolutions pointing to multiple variants

OUTPUT:
    HTML report with recommendations for human review

AUTHOR: ERA Admin / Cascade AI
DATE: 2025-10-25
"""

import sqlite3
from pathlib import Path
import re
from difflib import SequenceMatcher

DB_PATH = Path("../FathomInventory/fathom_emails.db")


def normalize_name(name):
    """Remove number suffixes and normalize for comparison"""
    # Remove (N) suffixes
    name = re.sub(r'\s*\(\d+\)\s*$', '', name)
    # Remove special symbols
    name = re.sub(r'🔁.*$', '', name)
    return name.strip()


def get_all_participants(conn):
    """Get all participant records"""
    return conn.execute("""
        SELECT DISTINCT name
        FROM participants
        WHERE name IS NOT NULL
        ORDER BY name
    """).fetchall()


def get_alias_variants(conn):
    """Get names that appear as different resolutions for same alias"""
    return conn.execute("""
        SELECT 
            fathom_name,
            GROUP_CONCAT(resolved_to, ' | ') as variants,
            COUNT(DISTINCT resolved_to) as variant_count
        FROM (
            SELECT DISTINCT fathom_name, resolved_to
            FROM fathom_alias_resolutions
            WHERE resolved_to IS NOT NULL
        )
        GROUP BY fathom_name
        HAVING variant_count > 1
        ORDER BY variant_count DESC
    """).fetchall()


def similarity_ratio(s1, s2):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()


def detect_redundancies(conn):
    """Detect all types of redundancies"""
    
    redundancies = {
        'number_suffix': [],      # Same name +/- (N)
        'case_difference': [],    # Same name different case
        'similar_names': [],      # High similarity (>0.85)
        'first_vs_full': [],      # "Ana" vs "Ana Calderon"
        'alias_variants': []      # From alias resolution table
    }
    
    participants = [row[0] for row in get_all_participants(conn)]
    
    print(f"Analyzing {len(participants)} participants...")
    
    # Check alias variants first
    alias_variants = get_alias_variants(conn)
    for fathom_name, variants, count in alias_variants:
        redundancies['alias_variants'].append({
            'alias': fathom_name,
            'variants': variants.split(' | '),
            'count': count
        })
    
    # Check for redundancies between participants
    checked = set()
    
    for i, name1 in enumerate(participants):
        for name2 in participants[i+1:]:
            pair = tuple(sorted([name1, name2]))
            if pair in checked:
                continue
            checked.add(pair)
            
            norm1 = normalize_name(name1)
            norm2 = normalize_name(name2)
            
            # 1. Number suffix difference
            if norm1 == norm2 and name1 != name2:
                redundancies['number_suffix'].append((name1, name2, 'EXACT_NORMALIZED'))
            
            # 2. Case difference
            elif name1.lower() == name2.lower() and name1 != name2:
                redundancies['case_difference'].append((name1, name2, 'CASE_ONLY'))
            
            # 3. High similarity (but not exact)
            else:
                sim = similarity_ratio(norm1, norm2)
                if sim > 0.85:
                    redundancies['similar_names'].append((name1, name2, f'{sim:.2%}'))
            
            # 4. First name vs full name
            parts1 = norm1.split()
            parts2 = norm2.split()
            if len(parts1) == 1 and len(parts2) > 1:
                if parts1[0].lower() == parts2[0].lower():
                    redundancies['first_vs_full'].append((name1, name2, 'FIRST_NAME'))
            elif len(parts2) == 1 and len(parts1) > 1:
                if parts2[0].lower() == parts1[0].lower():
                    redundancies['first_vs_full'].append((name2, name1, 'FIRST_NAME'))
    
    return redundancies


def generate_html_report(redundancies):
    """Generate HTML report for review"""
    
    html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>Participant Redundancy Detection</title>
<style>
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;max-width:1200px;margin:0 auto;padding:20px;background:#f5f5f5}
h1{color:#2c3e50;border-bottom:3px solid #e74c3c}
h2{color:#34495e;border-bottom:2px solid #3498db;margin-top:30px}
.category{background:white;padding:20px;margin:20px 0;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.1)}
.pair{background:#f8f9fa;padding:12px;margin:8px 0;border-left:4px solid #3498db;border-radius:4px}
.name{font-weight:bold;color:#2c3e50}
.reason{color:#7f8c8d;font-size:0.9em;margin-left:10px}
.count{background:#3498db;color:white;padding:2px 8px;border-radius:12px;font-size:0.85em}
.high{border-left-color:#e74c3c}
.medium{border-left-color:#f39c12}
.low{border-left-color:#95a5a6}
</style></head><body>
<h1>🔍 Participant Redundancy Detection</h1>
<p><strong>Generated:</strong> """ + str(Path().absolute()) + """</p>
<p><strong>Purpose:</strong> Identify potential duplicate participant records that should be merged.</p>
"""
    
    total = sum(len(v) if isinstance(v, list) else 0 for v in redundancies.values())
    html += f"<p><strong>Total potential redundancies:</strong> <span class='count'>{total}</span></p>"
    
    # Alias variants (highest priority)
    if redundancies['alias_variants']:
        html += """
<h2>🔀 Alias Variants (Same alias → Different resolutions)</h2>
<div class="category">
<p><strong>Priority:</strong> HIGH - These came from inconsistent Phase 4B-2 decisions</p>
"""
        for item in redundancies['alias_variants']:
            html += f"""
<div class="pair high">
    <strong>Alias:</strong> '{item['alias']}'<br>
    <strong>Resolved to:</strong> {' <strong>OR</strong> '.join(item['variants'])}
    <span class="reason">{item['count']} variants</span>
</div>
"""
        html += "</div>"
    
    # Number suffix
    if redundancies['number_suffix']:
        html += """
<h2>🔢 Number Suffix Differences</h2>
<div class="category">
<p><strong>Example:</strong> "Ana Calderon" vs "Ana Calderon (3)"</p>
"""
        for name1, name2, reason in redundancies['number_suffix']:
            html += f"""
<div class="pair high">
    <span class="name">{name1}</span> ⟷ <span class="name">{name2}</span>
    <span class="reason">{reason}</span>
</div>
"""
        html += "</div>"
    
    # Case differences
    if redundancies['case_difference']:
        html += """
<h2>Aa Case Differences</h2>
<div class="category">
<p><strong>Example:</strong> "Chris Searles" vs "Chris searles"</p>
"""
        for name1, name2, reason in redundancies['case_difference']:
            html += f"""
<div class="pair high">
    <span class="name">{name1}</span> ⟷ <span class="name">{name2}</span>
    <span class="reason">{reason}</span>
</div>
"""
        html += "</div>"
    
    # Similar names
    if redundancies['similar_names']:
        html += """
<h2>📝 Similar Names (>85% match)</h2>
<div class="category">
<p><strong>Example:</strong> "Christopher Danch" vs "Christopher P Danch"</p>
"""
        for name1, name2, similarity in redundancies['similar_names']:
            html += f"""
<div class="pair medium">
    <span class="name">{name1}</span> ⟷ <span class="name">{name2}</span>
    <span class="reason">{similarity} similar</span>
</div>
"""
        html += "</div>"
    
    # First vs full name
    if redundancies['first_vs_full']:
        html += """
<h2>👤 First Name vs Full Name</h2>
<div class="category">
<p><strong>Example:</strong> "Ana" vs "Ana Calderon"</p>
"""
        for short, full, reason in redundancies['first_vs_full']:
            html += f"""
<div class="pair medium">
    <span class="name">{short}</span> ⟷ <span class="name">{full}</span>
    <span class="reason">{reason}</span>
</div>
"""
        html += "</div>"
    
    html += """
</body></html>
"""
    
    return html


def main():
    print("="*60)
    print("🔍 PARTICIPANT REDUNDANCY DETECTION")
    print("="*60)
    
    conn = sqlite3.connect(DB_PATH)
    
    redundancies = detect_redundancies(conn)
    
    # Print summary
    print("\n📊 SUMMARY:")
    print(f"  Alias variants: {len(redundancies['alias_variants'])}")
    print(f"  Number suffix: {len(redundancies['number_suffix'])}")
    print(f"  Case difference: {len(redundancies['case_difference'])}")
    print(f"  Similar names: {len(redundancies['similar_names'])}")
    print(f"  First vs full: {len(redundancies['first_vs_full'])}")
    
    total = sum(len(v) if isinstance(v, list) else 0 for v in redundancies.values())
    print(f"\n✅ Total potential redundancies: {total}")
    
    # Generate HTML
    html = generate_html_report(redundancies)
    output_file = Path("PARTICIPANT_REDUNDANCIES.html")
    output_file.write_text(html)
    
    print(f"\n📄 Report saved to: {output_file.absolute()}")
    print("\nOpen in browser to review, then ask Claude to investigate!")
    
    conn.close()


if __name__ == '__main__':
    main()
