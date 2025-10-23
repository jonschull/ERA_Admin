#!/usr/bin/env python3
"""
Generate Phase 4B-2 approval table with Gmail research for 50 people.
Enhanced version with embedded Gmail insights and learned mappings from previous rounds.

Features:
- Auto-fills decisions from learned mappings (phone numbers, drops, name variants)
- Shows green badges (🔁) for auto-filled entries with reason
- Integrates Gmail research for context
- Fuzzy matches against Airtable people
- Exports to CSV with all decisions

Note: Emoji badges in HTML are automatically stripped during CSV processing.
See LEARNED_MAPPINGS_SYSTEM.md for auto-fill details.
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from town_hall_search import TownHallSearch

# Paths
SCRIPT_DIR = Path(__file__).parent
# Fix timestamp at script start to avoid minute-boundary issues
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M')
OUTPUT_FILE = SCRIPT_DIR / f"phase4b2_TEST_APPROVALS_{TIMESTAMP}.html"

# Load participant data
with open('/tmp/phase4b2_test_data.json', 'r') as f:
    participants = json.load(f)

# Load learned mappings from previous rounds
LEARNED_MAPPINGS_FILE = SCRIPT_DIR / 'phase4b2_learned_mappings.json'
learned_mappings = {'phone_mappings': {}, 'device_mappings': {}, 'name_corrections': {}, 'org_to_person': {}, 'drop_patterns': []}
if LEARNED_MAPPINGS_FILE.exists():
    with open(LEARNED_MAPPINGS_FILE, 'r') as f:
        learned_mappings = json.load(f)
    print(f"✅ Loaded learned mappings: {learned_mappings['metadata']['total_phone_mappings']} phone, "
          f"{learned_mappings['metadata']['total_drop_patterns']} drop, "
          f"{learned_mappings['metadata']['total_org_mappings']} org, "
          f"{learned_mappings['metadata']['total_name_corrections']} name corrections")
    print()

# Load Airtable data to check if people are already there
import csv
from fuzzywuzzy import fuzz

AIRTABLE_CSV = Path(__file__).parent.parent / "airtable" / "people_export.csv"
airtable_people = []
if AIRTABLE_CSV.exists():
    with open(AIRTABLE_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Name'):
                name = row['Name'].strip()
                # Extract last name for fuzzy matching
                parts = name.split()
                last_name = parts[-1] if parts else name
                airtable_people.append({
                    'name': name,
                    'last_name': last_name.lower(),
                    'first_name': parts[0].lower() if len(parts) > 0 else ''
                })

def fuzzy_check_airtable(person_name, threshold=80):
    """
    Check if person exists in Airtable using smart fuzzy matching.
    
    Strategy:
    1. Try full name match (first + last)
    2. If fails, try individual word matches (handles "Moses GFCCA" cases)
    3. Return best match with explanation
    
    Returns: (exists, matched_name, score, method)
    """
    if not airtable_people:
        return False, None, 0, None
    
    # Extract parts from search name
    parts = person_name.split()
    if not parts:
        return False, None, 0, None
    
    search_last = parts[-1].lower()
    search_first = parts[0].lower() if len(parts) > 0 else ''
    
    # STRATEGY 1: Full name match (first + last)
    best_match = None
    best_score = 0
    
    for at_person in airtable_people:
        # Match on last name primarily
        last_score = fuzz.ratio(search_last, at_person['last_name'])
        
        # If last names are close, check first name
        if last_score >= 70:
            first_score = fuzz.partial_ratio(search_first, at_person['first_name'])
            # Weighted score: last name more important
            combined_score = (last_score * 0.7) + (first_score * 0.3)
            
            if combined_score > best_score:
                best_score = combined_score
                best_match = at_person['name']
    
    # If full name match is good, return it
    if best_score >= threshold:
        return True, best_match, int(best_score), 'full_name'
    
    # STRATEGY 2: Word-by-word fallback (for single names only)
    # Only use if input appears to be single name (not "Fred Hornaday")
    search_words = [w for w in parts if len(w) > 2]
    use_word_matching = len(search_words) == 1  # Only for single names
    
    word_matches = []
    if use_word_matching:
        for word in search_words:
            word_lower = word.lower()
            for at_person in airtable_people:
                airtable_name = at_person['name']
                name_words = [w.lower() for w in airtable_name.split()]
                if word_lower in name_words:
                    word_matches.append({
                        'name': airtable_name,
                        'word': word,
                        'score': 100
                    })
        
        # Use word match only if 100% word match exists AND full name score is poor
        if word_matches:
            best_word = max(word_matches, key=lambda x: x['score'])
            if best_word['score'] == 100 and best_score < 70:
                return True, best_word['name'], best_word['score'], f"word:'{best_word['word']}'"
    
    # Return full name result even if below threshold
    return best_score >= threshold, best_match, int(best_score), 'full_name' if best_match else None

# Run Gmail research and parse results
def get_gmail_results(name, affiliation=None):
    """Get Gmail research results for a person."""
    import urllib.parse
    
    # Create Gmail search URL
    search_name = name.replace('-', ' ').replace('.', ' ')  # Handle special chars
    search_url = f"https://mail.google.com/mail/u/0/#search/{urllib.parse.quote(search_name)}"
    
    try:
        # Build command with optional affiliation
        cmd = ['python3', str(SCRIPT_DIR / 'gmail_research.py'), name]
        if affiliation and affiliation not in ['Unknown', 'This participant\'s company is not listed in the calendar event']:
            cmd.extend(['--affiliation', affiliation])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout
        
        # Parse output for email count
        if 'No emails found' in output:
            return {
                'found': False, 
                'count': 0, 
                'snippet': 'No emails found',
                'search_url': search_url,
                'query': search_name
            }
        
        # Extract count from "Found X emails"
        import re
        match = re.search(r'Found (\d+) emails', output)
        if match:
            count = int(match.group(1))
            
            # Extract first email subject/context
            lines = output.split('\n')
            snippet_lines = []
            for i, line in enumerate(lines):
                if line.startswith('1. **'):
                    # Get subject
                    subject = line.replace('1. **', '').replace('**', '').strip()
                    snippet_lines.append(html.escape(subject[:80]))  # Escape HTML to prevent injection
                    # Get context if available
                    if i+3 < len(lines) and ('Context:' in lines[i+3] or 'Snippet:' in lines[i+3]):
                        context = lines[i+3].split(':', 1)[1].strip()[:100]
                        snippet_lines.append(html.escape(context))  # Escape HTML to prevent injection
                    break
            
            snippet = ' | '.join(snippet_lines) if snippet_lines else 'Found in emails'
            
            return {
                'found': True, 
                'count': count, 
                'snippet': snippet,
                'search_url': search_url,
                'query': search_name
            }
        
        return {
            'found': False, 
            'count': 0, 
            'snippet': 'Error parsing results',
            'search_url': search_url,
            'query': search_name
        }
    
    except Exception as e:
        return {
            'found': False, 
            'count': 0, 
            'snippet': f'Error: {str(e)}',
            'search_url': search_url,
            'query': search_name
        }


# Auto-categorize
def categorize(name):
    """Auto-categorize participant."""
    name_lower = name.lower()
    
    # Organizations
    if any(word in name_lower for word in ['global', 'earth', 'labyrinth', 'town', 'gfcca', 'cosmic']):
        return 'organization'
    
    # Phone numbers
    if name.replace('+', '').replace(' ', '').isdigit():
        return 'phone'
    
    # Duplicates (has location, URL, or parentheses)
    if ', ' in name or 'www.' in name or '(' in name or 'Locations:' in name:
        return 'duplicate'
    
    # Single names
    if ' ' not in name:
        return 'single_name'
    
    return 'full_name'


# Check learned mappings
def check_learned_mapping(name):
    """Check if we have a learned mapping for this name from previous rounds.
    Returns: (has_mapping, decision, reason)
    """
    phone_mappings = learned_mappings.get('phone_mappings', {})
    device_mappings = learned_mappings.get('device_mappings', {})
    org_to_person = learned_mappings.get('org_to_person', {})
    name_corrections = learned_mappings.get('name_corrections', {})
    drop_patterns = learned_mappings.get('drop_patterns', [])
    
    # Check drop patterns (exact match)
    if name in drop_patterns:
        return True, 'drop', f'🔁 Previously dropped in earlier round'
    
    # Check phone mappings
    if name in phone_mappings:
        target = phone_mappings[name]
        return True, f'merge with: {target}', f'🔁 Phone number resolved in earlier round'
    
    # Check device mappings
    if name in device_mappings:
        target = device_mappings[name]
        return True, f'merge with: {target}', f'🔁 Device name resolved in earlier round'
    
    # Check org mappings
    if name in org_to_person:
        target = org_to_person[name]
        return True, f'merge with: {target}', f'🔁 Organization mapping from earlier round'
    
    # Check name corrections (only clean ones - not instructions)
    if name in name_corrections:
        target = name_corrections[name]
        # Filter out instructions/comments
        if not any(word in target.lower() for word in ['add', 'era', 'member', 'organization', 'airtable', 'examine', 'gmail', 'link', 'should']):
            # Check if it's a simple name (2-3 words, no extra text)
            words = target.split()
            if 1 <= len(words) <= 3 and all(w[0].isupper() or w.lower() in ['de', 'van', 'von', 'da'] for w in words if w):
                return True, f'merge with: {target}', f'🔁 Name variant resolved in earlier round'
    
    return False, '', ''


# Suggest action
def suggest_action(name, category, gmail_result, airtable_match):
    """Suggest likely action based on category, Gmail, and Airtable results."""
    in_airtable, matched_name, score, method = airtable_match
    
    # Check learned mappings first
    has_learned, learned_decision, learned_reason = check_learned_mapping(name)
    if has_learned:
        return learned_decision  # Use learned decision
    
    if category == 'organization':
        return 'drop'
    if category == 'phone':
        return 'drop'
    if category == 'duplicate':
        # If matched in Airtable with HIGH confidence, use that full name
        if in_airtable and matched_name and score >= 90:
            return f'merge with: {matched_name}'
        # Otherwise extract base name
        base_name = name.split(',')[0].split('(')[0].strip()
        # Don't suggest incomplete single names - flag for research instead
        if len(base_name.split()) == 1:
            return 'research - incomplete name (single word)'
        return f'merge with: {base_name}'
    if category == 'single_name':
        if in_airtable:
            return f'merge with: {matched_name}'
        if gmail_result['found']:
            return 'research - found in Gmail'
        return 'research - not in Gmail'
    if category == 'full_name':
        if in_airtable:
            return f'merge with: {matched_name}'
        if gmail_result['found']:
            return 'add to airtable (found in Gmail)'
        return 'likely not ERA-related'
    
    return ''


print("=" * 80)
print("GENERATING PHASE 4B-2 APPROVAL TABLE")
print("=" * 80)
print()

# Enrich with Gmail research and Airtable check
print("Running Gmail research on 25 people...")
for i, p in enumerate(participants, 1):
    print(f"  {i}/25: {p['name']}")
    
    # Check learned mappings first
    has_learned, learned_decision, learned_reason = check_learned_mapping(p['name'])
    p['has_learned_mapping'] = has_learned
    p['learned_reason'] = learned_reason
    
    affiliation = p.get('affiliation', None)
    p['gmail'] = get_gmail_results(p['name'], affiliation)
    p['category'] = categorize(p['name'])
    
    # Fuzzy check Airtable with smart word-by-word fallback
    in_airtable, matched_name, score, method = fuzzy_check_airtable(p['name'])
    p['in_airtable'] = in_airtable
    p['airtable_match'] = matched_name
    p['airtable_score'] = score
    p['airtable_method'] = method  # 'full_name' or 'word:Moses'
    
    # Determine if we should auto-check "Process This"
    # Auto-check if: learned mapping OR high confidence Airtable match
    p['should_process'] = has_learned or (score >= 80 if in_airtable else False)
    
    # Determine if we should auto-check "Probe" (needs investigation)
    # DON'T probe if we have a learned mapping (already decided)
    p['should_probe'] = False
    if not has_learned:
        if not in_airtable:
            # Not found in Airtable - needs probing if found in Gmail or ambiguous name
            if p['gmail']['found'] or p['category'] == 'single_name':
                p['should_probe'] = True
            # Also probe if has special chars (org names, URLs, etc)
            if any(char in p['name'] for char in [',', '.', '(', '/', 'www', 'Locations:']):
                p['should_probe'] = True
        elif in_airtable and score < 90:
            # Low-ish confidence match - might want to probe
            p['should_probe'] = True
    
    p['suggested_action'] = suggest_action(p['name'], p['category'], p['gmail'], (in_airtable, matched_name, score, method))

print()
print(f"✅ Gmail research complete")
print(f"✅ Checked against {len(airtable_people)} Airtable people with fuzzy matching")
print()

# Generate analysis report
print("=" * 80)
print("📊 AUTOMATIC ANALYSIS REPORT")
print("=" * 80)

probing_needed = []
high_confidence = []
low_confidence = []
needs_attention = []

for p in participants:
    if p['in_airtable']:
        if p['airtable_score'] >= 90:
            high_confidence.append(p)
        elif p['airtable_score'] >= 80:
            low_confidence.append(p)
        else:
            needs_attention.append(p)
        
        # Track word-based matches (probing cases)
        if p['airtable_method'] and 'word:' in p['airtable_method']:
            probing_needed.append(p)
    elif p['category'] not in ['organization', 'phone', 'duplicate']:
        needs_attention.append(p)

if probing_needed:
    print(f"\n🔍 WORD-BY-WORD PROBING ({len(probing_needed)}):")
    for p in probing_needed:
        print(f"   • {p['name']}")
        print(f"     → Matched: {p['airtable_match']} ({p['airtable_score']}%)")
        print(f"     → Method: {p['airtable_method']}")
        print(f"     → Suggestion: {p['suggested_action']}")
        print()

if high_confidence:
    print(f"\n✅ HIGH CONFIDENCE MATCHES ({len(high_confidence)}):")
    for p in high_confidence[:5]:  # Show first 5
        print(f"   • {p['name']} → {p['airtable_match']} ({p['airtable_score']}%)")
    if len(high_confidence) > 5:
        print(f"   ... and {len(high_confidence)-5} more")

if low_confidence:
    print(f"\n⚠️  MEDIUM CONFIDENCE MATCHES ({len(low_confidence)}):")
    for p in low_confidence:
        print(f"   • {p['name']} → {p['airtable_match']} ({p['airtable_score']}%)")

if needs_attention:
    print(f"\n⚡ NEEDS ATTENTION ({len(needs_attention)}):")
    for p in needs_attention[:10]:  # Show first 10
        status = "Not in Airtable"
        if p['in_airtable']:
            status = f"Low match: {p['airtable_match']} ({p['airtable_score']}%)"
        print(f"   • {p['name']} - {status}")
        if p['gmail']['found']:
            print(f"     Gmail: {p['gmail']['count']} emails found")
    if len(needs_attention) > 10:
        print(f"   ... and {len(needs_attention)-10} more")

print("\n" + "=" * 80)
print()

# Generate HTML
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phase 4B-2: Test Batch Approval (25 People)</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 100%;
            margin: 0 auto;
            padding: 15px;
            background: #f5f5f5;
            font-size: 13px;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .header {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .instructions {{
            background: #e8f4f8;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin-bottom: 20px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .stat-box {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
            color: #3498db;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            font-size: 14px;
        }}
        
        .controls {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        button {{
            background: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 10px;
            font-size: 14px;
        }}
        
        button:hover {{
            background: #2980b9;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        th {{
            background: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
            position: sticky;
            top: 0;
            cursor: pointer;
            user-select: none;
        }}
        
        th:hover {{
            background: #2c3e50;
        }}
        
        td {{
            padding: 10px;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        input[type="checkbox"] {{
            width: 20px;
            height: 20px;
            cursor: pointer;
        }}
        
        input[type="text"], textarea {{
            width: 100%;
            padding: 6px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: inherit;
        }}
        
        textarea {{
            resize: vertical;
            min-height: 40px;
        }}
        
        .video-link {{
            color: #3498db;
            text-decoration: none;
            margin-right: 5px;
        }}
        
        .video-link:hover {{
            text-decoration: underline;
        }}
        
        .category-org {{ background-color: #fee; }}
        .category-phone {{ background-color: #fdd; }}
        .category-duplicate {{ background-color: #ffe; }}
        .category-single_name {{ background-color: #eff; }}
        .category-full_name {{ background-color: #efe; }}
        
        .gmail-found {{ color: #27ae60; font-weight: bold; }}
        .gmail-not-found {{ color: #95a5a6; }}
        
        .suggestion {{
            font-size: 12px;
            color: #7f8c8d;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 Phase 4B-2: Test Batch Approval (25 People)</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Purpose:</strong> Review unenriched Fathom participants by cross-checking against Gmail research insights and airtable data.</p>
    </div>
    
    <div class="instructions">
        <h3>📖 Instructions</h3>
        <ol>
            <li><strong>Review each person:</strong> Check videos (🎥), Gmail results (📧), and category</li>
            <li><strong>Use suggestions:</strong> Pre-filled comments based on auto-categorization</li>
            <li><strong>Update comments:</strong> Edit to add your decisions:
                <ul>
                    <li><code>drop</code> - Delete from Fathom (organization/junk)</li>
                    <li><code>merge with: Name</code> - Consolidate with existing person</li>
                    <li><code>add to airtable</code> - Real person, create Airtable entry</li>
                    <li><code>ignore</code> - Not ERA-related</li>
                </ul>
            </li>
            <li><strong>Check/uncheck boxes:</strong> ✓ = process this action, ✗ = skip for now</li>
            <li><strong>Export when done:</strong> Click "📥 Export to CSV" button</li>
        </ol>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-value">{len(participants)}</div>
            <div class="stat-label">Total People</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{sum(1 for p in participants if p['gmail']['found'])}</div>
            <div class="stat-label">Found in Gmail</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{sum(1 for p in participants if p['category'] in ['organization', 'phone'])}</div>
            <div class="stat-label">Likely Delete</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{sum(1 for p in participants if p['category'] == 'duplicate')}</div>
            <div class="stat-label">Likely Merge</div>
        </div>
    </div>
    
    <div class="controls">
        <button onclick="exportToCSV()">📥 Export to CSV</button>
        <button onclick="checkAll()">✓ Check All</button>
        <button onclick="uncheckAll()">✗ Uncheck All</button>
        <button onclick="filterCategory('all')">Show All</button>
        <button onclick="filterCategory('organization')">Organizations</button>
        <button onclick="filterCategory('duplicate')">Duplicates</button>
        <button onclick="filterCategory('full_name')">Full Names</button>
    </div>
    
    <table id="approvalTable">
        <thead>
            <tr>
                <th onclick="sortTable(0)">Fathom Name</th>
                <th onclick="sortTable(1)">Videos</th>
                <th onclick="sortTable(2)">Records</th>
                <th onclick="sortTable(3)">Category</th>
                <th onclick="sortTable(4)">In Airtable</th>
                <th onclick="sortTable(5)">Gmail</th>
                <th onclick="sortTable(6)">Comments</th>
                <th onclick="sortTable(7)">Process This</th>
                <th onclick="sortTable(8)">Probe</th>
            </tr>
        </thead>
        <tbody>
'''

# Add table rows
for p in sorted(participants, key=lambda x: (x['category'], -x['record_count'])):
    video_links = ' '.join([f'<a href="{v["url"]}" target="_blank" class="video-link">🎥</a>' 
                            for v in p['videos'][:5]])
    if len(p['videos']) > 5:
        video_links += f' <span>(+{len(p["videos"])-5} more)</span>'
    
    gmail_class = 'gmail-found' if p['gmail']['found'] else 'gmail-not-found'
    gmail_url = p['gmail']['search_url']
    
    if p['gmail']['found']:
        gmail_text = f"<a href='{gmail_url}' target='_blank'>📧 {p['gmail']['count']} emails</a>"
        gmail_snippet = p['gmail']['snippet'][:100] if p['gmail']['snippet'] else ''
    else:
        # Show clickable link even when no results found
        query_hint = f"Query: {p['gmail']['query']}"
        gmail_text = f"<a href='{gmail_url}' target='_blank'>📧 Emails</a>"
        gmail_snippet = query_hint
    
    # Airtable match display with method
    if p['in_airtable']:
        method_hint = f" via {p['airtable_method']}" if p['airtable_method'] and 'word:' in p['airtable_method'] else ""
        airtable_display = f"✅ {p['airtable_match']}<br><small>({p['airtable_score']}%{method_hint})</small>"
    else:
        airtable_display = '❌'
    
    row_class = f"category-{p['category']}"
    
    # Show learned mapping reason if available
    learned_badge = ''
    if p.get('has_learned_mapping'):
        learned_badge = f"<br><span style='background:#4CAF50;color:white;padding:2px 6px;border-radius:3px;font-size:10px;'>{p.get('learned_reason', 'Auto-filled')}</span>"
    
    html += f'''
            <tr class="{row_class}" data-category="{p['category']}">
                <td><strong>{p['name']}</strong>{learned_badge}</td>
                <td>{video_links}</td>
                <td>{p['record_count']}</td>
                <td>{p['category'].replace('_', ' ').title()}</td>
                <td style="text-align:center; font-size:11px">{airtable_display}</td>
                <td>
                    <span class="{gmail_class}">{gmail_text}</span><br>
                    <small style="color:#888">{gmail_snippet}</small>
                </td>
                <td>
                    <textarea rows="2">{p['suggested_action']}</textarea>
                    <div class="suggestion">Suggestion: {p['suggested_action']}</div>
                </td>
                <td><input type="checkbox"{' checked' if p['should_process'] else ''}></td>
                <td><input type="checkbox"{' checked' if p['should_probe'] else ''}></td>
            </tr>
'''

html += '''
        </tbody>
    </table>
    
    <script>
        function sortTable(column) {
            const table = document.getElementById('approvalTable');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            
            rows.sort((a, b) => {
                let aVal = a.cells[column].textContent.trim();
                let bVal = b.cells[column].textContent.trim();
                
                // Try numeric sort
                if (!isNaN(aVal) && !isNaN(bVal)) {
                    return parseFloat(bVal) - parseFloat(aVal);
                }
                
                return aVal.localeCompare(bVal);
            });
            
            rows.forEach(row => tbody.appendChild(row));
        }
        
        function filterCategory(category) {
            const rows = document.querySelectorAll('#approvalTable tbody tr');
            rows.forEach(row => {
                if (category === 'all' || row.dataset.category === category) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        }
        
        function checkAll() {
            document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = true);
        }
        
        function uncheckAll() {
            document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
        }
        
        function exportToCSV() {
            const rows = document.querySelectorAll('#approvalTable tbody tr');
            const csvData = [];
            
            // Header
            csvData.push(['Fathom_Name', 'Videos_Count', 'Records', 'Category', 'In_Airtable', 'Gmail_Count', 'Gmail_Snippet', 'Comments', 'ProcessThis', 'Probe']);
            
            // Data rows
            rows.forEach(row => {
                try {
                    const cells = row.cells;
                    if (cells.length < 9) {
                        console.error('Row has insufficient cells:', cells.length);
                        return;
                    }
                    
                    const name = cells[0].textContent.trim();
                    const videoCount = cells[1].querySelectorAll('.video-link').length;
                    const records = cells[2].textContent.trim();
                    const category = cells[3].textContent.trim();
                    const inAirtable = cells[4].textContent.trim();
                    
                    const gmailSpan = cells[5].querySelector('span');
                    const gmailSmall = cells[5].querySelector('small');
                    const gmailText = gmailSpan ? gmailSpan.textContent.trim() : '';
                    const gmailSnippet = gmailSmall ? gmailSmall.textContent.trim() : '';
                    
                    const textarea = cells[6].querySelector('textarea');
                    const comments = textarea ? textarea.value : '';
                    
                    const processInput = cells[7].querySelector('input');
                    const probeInput = cells[8].querySelector('input');
                    const processThis = processInput && processInput.checked ? 'YES' : 'NO';
                    const probe = probeInput && probeInput.checked ? 'YES' : 'NO';
                    
                    csvData.push([name, videoCount, records, category, inAirtable, gmailText, gmailSnippet, comments, processThis, probe]);
                } catch (e) {
                    console.error('Error processing row:', e);
                }
            });
            
            // Convert to CSV string
            const csvString = csvData.map(row => 
                row.map(cell => '"' + String(cell).replace(/"/g, '""') + '"').join(',')
            ).join('\\n');
            
            // Download
            const blob = new Blob([csvString], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            const timestamp = new Date().toISOString().slice(0,19).replace(/[-:T]/g, '').substring(0,14);
            const filename = `phase4b2_approvals_${timestamp}.csv`;
            a.download = filename;
            a.click();
            window.URL.revokeObjectURL(url);
            
            // Show file path and copy to clipboard
            const filePath = `/Users/admin/Downloads/${filename}`;
            const fileUrl = `file://${filePath}`;
            
            // Display on page
            const pathDiv = document.createElement('div');
            pathDiv.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);background:#4CAF50;color:white;padding:20px;border-radius:8px;box-shadow:0 4px 6px rgba(0,0,0,0.3);z-index:10000;max-width:80%;';
            pathDiv.innerHTML = `
                <strong>✅ CSV Exported!</strong><br>
                <div style="margin-top:10px;font-family:monospace;background:rgba(0,0,0,0.2);padding:10px;border-radius:4px;font-size:12px;word-break:break-all;">
                    ${filePath}
                </div>
                <div style="margin-top:10px;font-size:12px;">
                    📋 File path copied to clipboard!<br>
                    <small style="opacity:0.8;">Note: If file exists, macOS may add (1), (2), etc.</small>
                </div>
            `;
            document.body.appendChild(pathDiv);
            
            // Auto-remove after 5 seconds
            setTimeout(() => pathDiv.remove(), 5000);
            
            // Copy to clipboard
            navigator.clipboard.writeText(filePath).then(() => {
                console.log('File path copied to clipboard:', filePath);
            }).catch(err => {
                console.error('Failed to copy to clipboard:', err);
                // Fallback: show alert with path
                alert('CSV exported to:\\n' + filePath + '\\n\\n(Could not auto-copy to clipboard)');
            });
        }
    </script>
</body>
</html>
'''

# Save HTML
with open(OUTPUT_FILE, 'w') as f:
    f.write(html)

print(f"\n✅ Generated: {OUTPUT_FILE}")
print(f"📁 Filename: phase4b2_TEST_APPROVALS_{TIMESTAMP}.html")
print()
print("📖 Next steps:")
print("  1. Open HTML file in browser")
print("  2. Review people with Gmail insights")
print("  3. Update comments as needed")
print("  4. Export to CSV")
print("  5. Discuss unclear cases in Cascade")
print()
