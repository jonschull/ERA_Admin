#!/usr/bin/env python3
"""
Phase 4B-1: Enrich existing Fathom participants with Airtable data

SAFE OPERATION: Only UPDATES existing Fathom records. No INSERTs yet.

What this does:
1. Fuzzy match Fathom participants → Airtable people (80% threshold)
2. UPDATE matched Fathom records with:
   - Corrected name spelling (Airtable is ground truth)
   - Member status (era Member field)
   - Donor flag
   - Email address
   - Projects
   - Airtable ID
   - Data source = 'both'
3. Generate detailed enrichment report

What this does NOT do:
- Does NOT insert new Airtable-only people (that's Phase 4B-2)
- Does NOT delete any Fathom records
"""

import subprocess
import sys
import sqlite3
import csv
from pathlib import Path
from datetime import datetime
from fuzzywuzzy import fuzz
from collections import defaultdict

# Paths
SCRIPT_DIR = Path(__file__).parent
ERA_ADMIN_ROOT = SCRIPT_DIR.parent
FATHOM_DIR = ERA_ADMIN_ROOT / "FathomInventory"
DB_PATH = FATHOM_DIR / "fathom_emails.db"
BACKUP_SCRIPT = FATHOM_DIR / "scripts" / "backup_database.sh"
AIRTABLE_EXPORT = ERA_ADMIN_ROOT / "airtable" / "people_export.csv"
REPORT_PATH = SCRIPT_DIR / f"phase4b1_enrichment_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md"

# Fuzzy matching threshold
MATCH_THRESHOLD = 80


def require_backup():
    """
    Enforce backup before any database modifications.
    Script exits if backup fails.
    """
    print("=" * 60)
    print("🔒 BACKUP REQUIREMENT CHECK")
    print("=" * 60)
    print(f"Database: {DB_PATH}")
    print(f"Backup script: {BACKUP_SCRIPT}")
    print()
    
    if not BACKUP_SCRIPT.exists():
        print(f"❌ ERROR: Backup script not found: {BACKUP_SCRIPT}")
        print("Cannot proceed without backup capability.")
        sys.exit(1)
    
    print("Running backup script...")
    try:
        result = subprocess.run(
            [str(BACKUP_SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
            cwd=str(FATHOM_DIR)
        )
        print(result.stdout)
        
        # Verify backup was created
        backup_dir = FATHOM_DIR / "backups"
        if not backup_dir.exists():
            print("❌ ERROR: Backup directory not created")
            sys.exit(1)
            
        print("✅ Backup verified - proceeding with database modifications")
        print("=" * 60)
        print()
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ BACKUP FAILED: {e}")
        print(e.stderr)
        print()
        print("Cannot proceed without successful backup.")
        print("Fix backup issues and try again.")
        sys.exit(1)


def get_db_connection():
    """Get database connection with proper error handling."""
    if not DB_PATH.exists():
        print(f"❌ ERROR: Database not found: {DB_PATH}")
        sys.exit(1)
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ ERROR connecting to database: {e}")
        sys.exit(1)


def verify_database_integrity(conn):
    """Check database integrity before modifications."""
    print("🔍 Checking database integrity...")
    cursor = conn.cursor()
    cursor.execute("PRAGMA integrity_check;")
    result = cursor.fetchone()[0]
    
    if result != "ok":
        print(f"❌ DATABASE INTEGRITY CHECK FAILED: {result}")
        print("Database may be corrupt. Restore from backup.")
        sys.exit(1)
    
    print("✅ Database integrity OK")


def load_airtable_data():
    """Load Airtable export CSV."""
    print(f"📊 Loading Airtable data from {AIRTABLE_EXPORT}...")
    
    if not AIRTABLE_EXPORT.exists():
        print(f"❌ ERROR: Airtable export not found: {AIRTABLE_EXPORT}")
        sys.exit(1)
    
    people = []
    with open(AIRTABLE_EXPORT, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only include people with names
            if row.get('Name'):
                people.append({
                    'airtable_id': row.get('airtable_id'),
                    'name': row.get('Name', '').strip(),
                    'email': row.get('Email', '').strip(),
                    'era_member': row.get('era Member') == 'True',
                    'is_donor': row.get('Donor Flag') == 'True',
                    'projects': row.get('Projects', '').strip() if row.get('Projects') else None
                })
    
    print(f"✅ Loaded {len(people)} people from Airtable")
    print(f"   - {sum(1 for p in people if p['era_member'])} members")
    print(f"   - {sum(1 for p in people if p['is_donor'])} donors")
    print(f"   - {sum(1 for p in people if p['email'])} with email")
    return people


def load_fathom_participants(conn):
    """Load all Fathom participants (unique by name) with their Fathom video URLs."""
    print(f"📊 Loading Fathom participants...")
    cursor = conn.cursor()
    
    # Get unique names with sample IDs and all video URLs
    # Also check if already enriched (has validated_by_airtable flag)
    cursor.execute("""
        SELECT 
            name,
            COUNT(*) as record_count,
            MIN(id) as sample_id,
            GROUP_CONCAT(DISTINCT source_call_url) as video_urls,
            MAX(validated_by_airtable) as validated_by_airtable
        FROM participants
        GROUP BY name
    """)
    
    participants = {}
    already_enriched = 0
    
    for row in cursor.fetchall():
        # GROUP_CONCAT uses comma as default delimiter
        video_urls = row['video_urls'].split(',') if row['video_urls'] else []
        
        participants[row['name']] = {
            'name': row['name'],
            'record_count': row['record_count'],
            'sample_id': row['sample_id'],
            'video_urls': video_urls,
            'validated_by_airtable': row['validated_by_airtable']  # 1 if enriched, None/0 if not
        }
        
        if row['validated_by_airtable']:
            already_enriched += 1
    
    print(f"✅ Loaded {len(participants)} unique participants")
    print(f"   - Total records: {sum(p['record_count'] for p in participants.values())}")
    if already_enriched > 0:
        print(f"   - Already enriched: {already_enriched} (will skip)")
    return participants


def fuzzy_match_names(fathom_participants, airtable_people, threshold=MATCH_THRESHOLD):
    """
    Fuzzy match Fathom participants to Airtable people.
    Skips participants that are already enriched (have airtable_name).
    Returns: dict of fathom_name -> airtable_person with match scores
    """
    # Filter out already-enriched participants
    unenriched = {name: data for name, data in fathom_participants.items() 
                  if not data.get('validated_by_airtable')}
    
    enriched_count = len(fathom_participants) - len(unenriched)
    
    print(f"\n🔍 Fuzzy matching (threshold: {threshold}%)...")
    if enriched_count > 0:
        print(f"   Skipping {enriched_count} already-enriched participants")
    print(f"   Matching {len(unenriched)} unenriched participants...")
    
    matches = {}
    match_scores = defaultdict(list)
    
    for fathom_name, fathom_data in unenriched.items():
        best_match = None
        best_score = 0
        
        for airtable_person in airtable_people:
            airtable_name = airtable_person['name']
            
            # Try multiple fuzzy algorithms
            ratio = fuzz.ratio(fathom_name.lower(), airtable_name.lower())
            partial = fuzz.partial_ratio(fathom_name.lower(), airtable_name.lower())
            token_sort = fuzz.token_sort_ratio(fathom_name.lower(), airtable_name.lower())
            
            # Use highest score
            score = max(ratio, partial, token_sort)
            
            if score >= threshold and score > best_score:
                best_score = score
                best_match = airtable_person
        
        if best_match:
            matches[fathom_name] = {
                'airtable_person': best_match,
                'score': best_score,
                'fathom_data': fathom_data
            }
            match_scores[best_score].append(fathom_name)
    
    print(f"✅ Matched {len(matches)} Fathom participants to Airtable")
    print(f"\n   Match quality distribution:")
    for score in sorted(match_scores.keys(), reverse=True):
        if score >= 90:
            print(f"   - {score}% (excellent): {len(match_scores[score])} matches")
        elif score >= 85:
            print(f"   - {score}% (very good): {len(match_scores[score])} matches")
        elif score >= threshold:
            print(f"   - {score}% (good): {len(match_scores[score])} matches")
    
    return matches


def add_enrichment_columns(conn):
    """Add new columns to participants table if they don't exist."""
    print("\n📝 Adding enrichment columns to participants table...")
    cursor = conn.cursor()
    
    columns_to_add = [
        ("validated_by_airtable", "BOOLEAN DEFAULT 0"),
        ("era_member", "BOOLEAN DEFAULT 0"),
        ("is_donor", "BOOLEAN DEFAULT 0"),
        ("email", "TEXT"),
        ("airtable_id", "TEXT"),
        ("projects", "TEXT"),
        ("data_source", "TEXT DEFAULT 'fathom_ai'"),
        ("landscape_node_id", "TEXT")
    ]
    
    for col_name, col_def in columns_to_add:
        try:
            cursor.execute(f"ALTER TABLE participants ADD COLUMN {col_name} {col_def}")
            print(f"   ✅ Added column: {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"   ℹ️  Column already exists: {col_name}")
            else:
                raise
    
    conn.commit()
    print("✅ Schema update complete")


def delete_fathom_participants(conn, names_to_delete):
    """Delete specified participants from Fathom database completely."""
    if not names_to_delete:
        return
    
    print(f"\n🗑️  Deleting {len(names_to_delete)} participants from Fathom database...")
    cursor = conn.cursor()
    
    deleted_count = 0
    for name in names_to_delete:
        # Get count first
        cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (name,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            cursor.execute("DELETE FROM participants WHERE name = ?", (name,))
            deleted_count += count
            print(f"   ✓ Deleted '{name}' ({count} records)")
        else:
            print(f"   ⚠️  '{name}' not found (already deleted?)")
    
    conn.commit()
    print(f"✅ Deleted {deleted_count} total records")
    return deleted_count


def enrich_participants(conn, matches):
    """
    UPDATE Fathom participants with Airtable data.
    Airtable spelling takes precedence (ground truth).
    """
    print("\n🔄 Enriching Fathom participants with Airtable data...")
    print("   (Airtable spelling is ground truth - correcting AI errors)\n")
    
    cursor = conn.cursor()
    
    stats = {
        'name_corrections': 0,
        'members_identified': 0,
        'donors_identified': 0,
        'emails_added': 0,
        'projects_added': 0,
        'total_updated': 0
    }
    
    corrections = []
    
    for fathom_name, match_data in matches.items():
        airtable_person = match_data['airtable_person']
        airtable_name = airtable_person['name']
        score = match_data['score']
        
        # Track if name needs correction
        name_changed = fathom_name != airtable_name
        if name_changed:
            stats['name_corrections'] += 1
            corrections.append({
                'fathom': fathom_name,
                'airtable': airtable_name,
                'score': score
            })
        
        # Update ALL records for this person (by name)
        cursor.execute("""
            UPDATE participants
            SET 
                name = ?,
                validated_by_airtable = 1,
                era_member = ?,
                is_donor = ?,
                email = ?,
                airtable_id = ?,
                projects = ?,
                data_source = 'both'
            WHERE name = ?
        """, (
            airtable_name,  # Corrected spelling
            1 if airtable_person['era_member'] else 0,
            1 if airtable_person['is_donor'] else 0,
            airtable_person['email'] if airtable_person['email'] else None,
            airtable_person['airtable_id'],
            airtable_person['projects'],
            fathom_name  # WHERE clause uses old name
        ))
        
        records_updated = cursor.rowcount
        stats['total_updated'] += records_updated
        
        if airtable_person['era_member']:
            stats['members_identified'] += 1
        if airtable_person['is_donor']:
            stats['donors_identified'] += 1
        if airtable_person['email']:
            stats['emails_added'] += 1
        if airtable_person['projects']:
            stats['projects_added'] += 1
    
    conn.commit()
    
    print(f"✅ Enrichment complete!")
    print(f"\n   📊 Statistics:")
    print(f"   - Total participant records updated: {stats['total_updated']}")
    print(f"   - Unique people matched: {len(matches)}")
    print(f"   - Names corrected (AI → Airtable): {stats['name_corrections']}")
    print(f"   - Members identified: {stats['members_identified']}")
    print(f"   - Donors identified: {stats['donors_identified']}")
    print(f"   - Emails added: {stats['emails_added']}")
    print(f"   - Projects added: {stats['projects_added']}")
    
    return stats, corrections


def generate_editable_approval_table(matches, fathom_participants, airtable_people):
    """Generate editable HTML table for user approval."""
    html_path = SCRIPT_DIR / f"phase4b1_APPROVALS_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    print(f"\n📝 Generating editable approval table (HTML): {html_path}")
    
    # Calculate what WOULD happen
    name_corrections = sum(1 for fathom_name, match_data in matches.items() 
                          if fathom_name != match_data['airtable_person']['name'])
    members_identified = sum(1 for m in matches.values() if m['airtable_person']['era_member'])
    donors_identified = sum(1 for m in matches.values() if m['airtable_person']['is_donor'])
    emails_added = sum(1 for m in matches.values() if m['airtable_person']['email'])
    
    with open(html_path, 'w', encoding='utf-8') as f:
        # HTML header with styling
        f.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Phase 4B-1: Approval Table</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        h1 { color: #333; }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .guidance-row { display: flex; gap: 20px; margin: 20px 0; }
        .instructions { background: #e8f4f8; padding: 20px; border-radius: 5px; border-left: 4px solid #2196F3; flex: 1; }
        .terminology { background: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ff9800; flex: 1; }
        .terminology h4 { margin-top: 0; }
        .terminology ul { margin: 10px 0; }
        .terminology li { margin: 5px 0; }
        .actions { margin: 20px 0; }
        .btn { padding: 10px 20px; margin: 5px; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; }
        .btn-primary { background: #4CAF50; color: white; }
        .btn-secondary { background: #2196F3; color: white; }
        .btn:hover { opacity: 0.8; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; font-size: 13px; }
        th { 
            background: #4CAF50; 
            color: white; 
            padding: 12px 8px; 
            text-align: left; 
            position: sticky; 
            top: 0; 
            cursor: pointer;
            user-select: none;
        }
        th:hover { background: #45a049; }
        th:after { content: ' ⇅'; opacity: 0.5; }
        td { padding: 8px; border-bottom: 1px solid #ddd; }
        tr:hover { background: #f5f5f5; }
        .video-link { margin: 0 3px; text-decoration: none; font-size: 16px; }
        .low-score { background: #fff3cd; }
        input[type="checkbox"] { width: 18px; height: 18px; cursor: pointer; }
        input[type="text"] { width: 100%; border: 1px solid #ddd; padding: 4px; font-size: 12px; }
        .member-yes { color: green; font-weight: bold; }
        .donor-yes { color: blue; font-weight: bold; }
        .stats { background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Phase 4B-1: Match Approval Table (Enhanced)</h1>
        
        <div class="guidance-row">
            <div class="instructions">
                <h3>📋 Instructions:</h3>
                <ol>
                    <li>Click video links (🎥) to verify each person in Fathom recordings</li>
                    <li>Check/uncheck the ✓ checkbox to approve/reject matches</li>
                    <li>Add comments using the terminology (right) or free-form</li>
                    <li>Click column headers to sort the table</li>
                    <li>Click "Export to CSV" button when done reviewing</li>
                    <li>Save the CSV file and re-run the script</li>
                </ol>
            </div>
            
            <div class="terminology">
                <h4>💡 Comment Terminology (recommended):</h4>
                <ul>
                    <li><strong>"drop"</strong> → Remove from Fathom database</li>
                    <li><strong>"Correct Name"</strong> → Real name to use</li>
                    <li><strong>"email@example.com"</strong> → Correct email</li>
                    <li><strong>"needs reunion"</strong> → Multiple accounts</li>
                    <li><strong>"add to airtable"</strong> → New person</li>
                    <li><strong>"remove from Fathom"</strong> → Contamination</li>
                    <li><strong>"investigate"</strong> → Needs review</li>
                </ul>
                <p style="margin: 10px 0 0 0; font-size: 0.9em;"><em>Free-form comments OK!</em></p>
            </div>
        </div>
        
        <div class="actions">
            <button class="btn btn-primary" onclick="exportToCSV()">📥 Export to CSV</button>
            <button class="btn btn-secondary" onclick="toggleApproved()">👁️ Show Only Approved</button>
            <button class="btn btn-secondary" onclick="toggleRejected()">👁️ Show Only Rejected</button>
            <button class="btn btn-secondary" onclick="showAll()">👁️ Show All</button>
        </div>
        
        <div class="stats">
            <strong>Stats:</strong> """ + f"{len(matches)} matches found | {name_corrections} name corrections | {members_identified} members | {donors_identified} donors" + """
            <span id="filterStats" style="margin-left: 20px;"></span>
        </div>
        
        <table id="matchTable">
            <thead>
                <tr>
                    <th onclick="sortTable(0)">Fathom Name</th>
                    <th onclick="sortTable(1)">Videos</th>
                    <th onclick="sortTable(2)">Airtable Name</th>
                    <th onclick="sortTable(3)">Email</th>
                    <th onclick="sortTable(4)">Score</th>
                    <th onclick="sortTable(5)">M</th>
                    <th onclick="sortTable(6)">D</th>
                    <th onclick="sortTable(7)">Comments</th>
                    <th onclick="sortTable(8)">✓</th>
                </tr>
            </thead>
            <tbody id="tableBody">
""")
        
        # Generate table rows sorted by score (lowest first)
        sorted_matches = sorted(matches.items(), key=lambda x: x[1]['score'])
        
        for fathom_name, match_data in sorted_matches:
            airtable_person = match_data['airtable_person']
            fathom_data = match_data['fathom_data']
            
            # Video links as clickable emoji links
            video_urls = fathom_data.get('video_urls', [])
            video_links_html = ''
            for url in video_urls[:5]:  # Max 5 links
                video_links_html += f'<a href="{url}" target="_blank" class="video-link">🎥</a>'
            if len(video_urls) > 5:
                video_links_html += f' (+{len(video_urls)-5})'
            
            # Member/Donor flags
            member_class = 'member-yes' if airtable_person['era_member'] else ''
            donor_class = 'donor-yes' if airtable_person['is_donor'] else ''
            member_flag = "✓" if airtable_person['era_member'] else ""
            donor_flag = "✓" if airtable_person['is_donor'] else ""
            
            # Default comment
            default_comment = ""
            if match_data['score'] < 90:
                default_comment = "Low score"
            if fathom_name != airtable_person['name'] and ' ' not in fathom_name:
                default_comment = "Single name"
            
            # Row class for low scores
            row_class = ' class="low-score"' if match_data['score'] < 90 else ''
            
            # Checkbox - default checked for high scores
            checked = ' checked' if match_data['score'] >= 95 else ''
            
            # Escape HTML in names
            fathom_name_html = fathom_name.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            airtable_name_html = airtable_person['name'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            email_html = (airtable_person['email'] or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            f.write(f"""            <tr{row_class} data-fathom-name="{fathom_name_html}">
                <td>{fathom_name_html}</td>
                <td>{video_links_html}</td>
                <td>{airtable_name_html}</td>
                <td style="font-size: 0.9em;">{email_html}</td>
                <td>{match_data['score']}%</td>
                <td class="{member_class}">{member_flag}</td>
                <td class="{donor_class}">{donor_flag}</td>
                <td><input type="text" value="{default_comment}" /></td>
                <td><input type="checkbox"{checked} /></td>
            </tr>
""")
        
        # Close HTML with JavaScript
        f.write("""        </tbody>
        </table>
        
        <div class="actions">
            <button class="btn btn-primary" onclick="exportToCSV()">📥 Export to CSV</button>
        </div>
        
        <p style="color: #666; font-size: 0.9em;">
            <strong>Legend:</strong> M = Member, D = Donor, ✓ = Approved | Yellow rows = Low confidence matches (need review)
        </p>
    </div>
    
    <script>
    // Table sorting
    let sortDirection = 1;
    
    function sortTable(columnIndex) {
        const tbody = document.getElementById("tableBody");
        const rows = Array.from(tbody.rows);
        
        rows.sort((a, b) => {
            let aValue, bValue;
            
            // Handle Comments column (has input field)
            if (columnIndex === 7) {
                const aInput = a.cells[columnIndex].querySelector('input[type="text"]');
                const bInput = b.cells[columnIndex].querySelector('input[type="text"]');
                aValue = aInput ? aInput.value.trim() : '';
                bValue = bInput ? bInput.value.trim() : '';
            }
            // Handle Checkbox column
            else if (columnIndex === 8) {
                const aCheckbox = a.cells[columnIndex].querySelector('input[type="checkbox"]');
                const bCheckbox = b.cells[columnIndex].querySelector('input[type="checkbox"]');
                aValue = aCheckbox && aCheckbox.checked ? 1 : 0;
                bValue = bCheckbox && bCheckbox.checked ? 1 : 0;
            }
            // Handle Score column (numeric)
            else if (columnIndex === 4) {
                aValue = parseInt(a.cells[columnIndex].textContent.trim());
                bValue = parseInt(b.cells[columnIndex].textContent.trim());
            }
            // Handle all other columns (text)
            else {
                aValue = a.cells[columnIndex].textContent.trim();
                bValue = b.cells[columnIndex].textContent.trim();
            }
            
            if (aValue < bValue) return -1 * sortDirection;
            if (aValue > bValue) return 1 * sortDirection;
            return 0;
        });
        
        // Reverse sort direction for next click
        sortDirection *= -1;
        
        // Re-append sorted rows
        rows.forEach(row => tbody.appendChild(row));
        
        updateStats();
    }
    
    // Export to CSV
    function exportToCSV() {
        const table = document.getElementById("matchTable");
        const rows = table.querySelectorAll("tr");
        let csv = [];
        
        // Header
        csv.push("Fathom_Name,Video_URLs,Airtable_Name,Email,Score,Member,Donor,Comments,APPROVED");
        
        // Data rows
        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const cells = row.cells;
            
            const fathomName = cells[0].textContent.trim();
            const videos = Array.from(cells[1].querySelectorAll('a')).map(a => a.href).join(' | ');
            const airtableName = cells[2].textContent.trim();
            const email = cells[3].textContent.trim();
            const score = cells[4].textContent.trim();
            const member = cells[5].textContent.trim();
            const donor = cells[6].textContent.trim();
            const comment = cells[7].querySelector('input').value.replace(/"/g, '""');
            const approved = cells[8].querySelector('input').checked ? 'YES' : 'NO';
            
            csv.push(`"${fathomName}","${videos}","${airtableName}","${email}","${score}","${member}","${donor}","${comment}","${approved}"`);
        }
        
        // Download
        const blob = new Blob([csv.join('\\n')], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'phase4b1_approvals_' + new Date().toISOString().slice(0,10) + '.csv';
        a.click();
        URL.revokeObjectURL(url);
    }
    
    // Filter functions
    function toggleApproved() {
        const rows = document.querySelectorAll('#tableBody tr');
        rows.forEach(row => {
            const checkbox = row.querySelector('input[type="checkbox"]');
            row.style.display = checkbox.checked ? '' : 'none';
        });
        updateStats();
    }
    
    function toggleRejected() {
        const rows = document.querySelectorAll('#tableBody tr');
        rows.forEach(row => {
            const checkbox = row.querySelector('input[type="checkbox"]');
            row.style.display = !checkbox.checked ? '' : 'none';
        });
        updateStats();
    }
    
    function showAll() {
        const rows = document.querySelectorAll('#tableBody tr');
        rows.forEach(row => row.style.display = '');
        updateStats();
    }
    
    // Update stats
    function updateStats() {
        const rows = Array.from(document.querySelectorAll('#tableBody tr'));
        const visible = rows.filter(r => r.style.display !== 'none');
        const approved = visible.filter(r => r.querySelector('input[type="checkbox"]').checked).length;
        const rejected = visible.length - approved;
        
        document.getElementById('filterStats').textContent = 
            `| Showing: ${visible.length} rows | Approved: ${approved} | Rejected: ${rejected}`;
    }
    
    // Initialize
    window.addEventListener('load', () => {
        updateStats();
        
        // Add change listeners to checkboxes
        document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
            cb.addEventListener('change', updateStats);
        });
    });
    </script>
</body>
</html>
""")
    
    print(f"✅ Approval table saved: {html_path}")
    print(f"   📋 Open in browser to review")
    print(f"   ✏️  Edit: check/uncheck boxes, add comments, click headers to sort")
    print(f"   💾 Click 'Export to CSV' button when done")
    print(f"   🔄 Re-run script - it will read the exported CSV")
    return html_path


def parse_approval_table(table_path):
    """Parse edited approval table (HTML or CSV) to get approved matches and comments."""
    print(f"\n📖 Parsing approval table: {table_path}")
    
    if not table_path.exists():
        print(f"❌ ERROR: Approval table not found: {table_path}")
        print("   Please ensure the approval table file exists.")
        sys.exit(1)
    
    approved_matches = {}
    
    # Check file type
    if str(table_path).endswith('.csv'):
        # Parse CSV
        print("   Format: CSV")
        import csv
        with open(table_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            for row in rows:
                fathom_name = row['Fathom_Name']
                comment = row['Comments']
                approved = row['APPROVED'].upper() == 'YES'
                
                if approved:
                    approved_matches[fathom_name] = {
                        'approved': True,
                        'comment': comment
                    }
        
        print(f"✅ Parsed CSV approval table")
        print(f"   - Total rows: {len(rows)}")
        print(f"   - Approved matches: {len(approved_matches)}")
    
    else:
        # Parse HTML
        print("   Format: HTML")
        with open(table_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Simple HTML parsing - find all table rows
        import re
        
        # Find all <tr> tags with data-fathom-name attribute
        tr_pattern = r'<tr[^>]*data-fathom-name="([^"]*)"[^>]*>(.*?)</tr>'
        rows = re.findall(tr_pattern, html_content, re.DOTALL)
        
        for fathom_name_html, row_content in rows:
            # Unescape HTML entities
            fathom_name = fathom_name_html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            
            # Find comment input value
            comment_match = re.search(r'<input type="text" value="([^"]*)"', row_content)
            comment = comment_match.group(1) if comment_match else ''
            
            # Find checkbox state
            checkbox_match = re.search(r'<input type="checkbox"([^>]*)', row_content)
            is_checked = checkbox_match and 'checked' in checkbox_match.group(1)
            
            if is_checked:
                approved_matches[fathom_name] = {
                    'approved': True,
                    'comment': comment
                }
        
        print(f"✅ Parsed HTML approval table")
        print(f"   - Total rows found: {len(rows)}")
        print(f"   - Approved matches: {len(approved_matches)}")
    
    return approved_matches


def generate_final_report(matches, stats, corrections, fathom_participants, airtable_people, user_comments):
    """Generate final confirmation report AFTER modifications."""
    print(f"\n📝 Generating final report: {REPORT_PATH}")
    
    with open(REPORT_PATH, 'w') as f:
        f.write("# Phase 4B-1 Enrichment Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        # Executive Summary
        f.write("## Executive Summary\n\n")
        f.write(f"- **Fathom participants (unique):** {len(fathom_participants)}\n")
        f.write(f"- **Airtable people:** {len(airtable_people)}\n")
        f.write(f"- **Successfully matched:** {len(matches)} ({len(matches)/len(fathom_participants)*100:.1f}% of Fathom)\n")
        f.write(f"- **Total records updated:** {stats['total_updated']}\n")
        f.write(f"- **Names corrected:** {stats['name_corrections']}\n")
        f.write(f"- **Members identified:** {stats['members_identified']}\n")
        f.write(f"- **Donors identified:** {stats['donors_identified']}\n")
        f.write(f"- **Emails added:** {stats['emails_added']}\n\n")
        
        # User comments section
        if user_comments:
            f.write("## User Review Comments\n\n")
            for name, comment in user_comments.items():
                if comment:
                    f.write(f"- **{name}:** {comment}\n")
            f.write("\n")
        
        # Name Corrections
        f.write("## Name Corrections (AI Errors Fixed)\n\n")
        f.write("Airtable spelling is ground truth. These corrections fix AI misidentifications:\n\n")
        
        if corrections:
            f.write("| Fathom (AI) | → | Airtable (Correct) | Match Score |\n")
            f.write("|-------------|---|-------------------|-------------|\n")
            for c in sorted(corrections, key=lambda x: x['score'], reverse=True):
                f.write(f"| {c['fathom']} | → | {c['airtable']} | {c['score']}% |\n")
        else:
            f.write("✅ No name corrections needed - all names matched exactly.\n")
        
        f.write("\n")
        
        # Match Quality
        f.write("## Match Quality Distribution\n\n")
        score_buckets = defaultdict(int)
        for match_data in matches.values():
            score = match_data['score']
            if score == 100:
                score_buckets['100% (Exact)'] += 1
            elif score >= 95:
                score_buckets['95-99% (Excellent)'] += 1
            elif score >= 90:
                score_buckets['90-94% (Very Good)'] += 1
            elif score >= 85:
                score_buckets['85-89% (Good)'] += 1
            else:
                score_buckets[f'{MATCH_THRESHOLD}-84% (Acceptable)'] += 1
        
        for bucket in ['100% (Exact)', '95-99% (Excellent)', '90-94% (Very Good)', '85-89% (Good)', f'{MATCH_THRESHOLD}-84% (Acceptable)']:
            if bucket in score_buckets:
                f.write(f"- **{bucket}:** {score_buckets[bucket]} matches\n")
        
        f.write("\n")
        
        # Member/Donor Breakdown
        f.write("## Enrichment Breakdown\n\n")
        f.write(f"- **Members identified:** {stats['members_identified']}\n")
        f.write(f"- **Donors identified:** {stats['donors_identified']}\n")
        f.write(f"- **Both member AND donor:** {sum(1 for m in matches.values() if m['airtable_person']['era_member'] and m['airtable_person']['is_donor'])}\n")
        f.write(f"- **Email addresses added:** {stats['emails_added']}\n")
        f.write(f"- **Project info added:** {stats['projects_added']}\n\n")
        
        # Sample Enriched Records
        f.write("## Sample Enriched Records (First 20)\n\n")
        for i, (fathom_name, match_data) in enumerate(list(matches.items())[:20]):
            airtable_person = match_data['airtable_person']
            f.write(f"### {i+1}. {airtable_person['name']}\n\n")
            if fathom_name != airtable_person['name']:
                f.write(f"- **Corrected from:** {fathom_name}\n")
            f.write(f"- **Match score:** {match_data['score']}%\n")
            f.write(f"- **Member:** {'Yes' if airtable_person['era_member'] else 'No'}\n")
            f.write(f"- **Donor:** {'Yes' if airtable_person['is_donor'] else 'No'}\n")
            if airtable_person['email']:
                f.write(f"- **Email:** {airtable_person['email']}\n")
            f.write(f"- **Records updated:** {match_data['fathom_data']['record_count']}\n")
            f.write("\n")
        
        # Unmatched Fathom (for Phase 4B-2 review)
        unmatched_fathom = [name for name in fathom_participants.keys() if name not in matches]
        f.write(f"## Unmatched Fathom Participants ({len(unmatched_fathom)})\n\n")
        f.write("These Fathom participants did not match any Airtable person (< 80% similarity).\n")
        f.write("**Action required:** Review in Phase 4B-2 to determine if they are:\n")
        f.write("- Real people not in Airtable yet (KEEP)\n")
        f.write("- Severe AI misspellings that need manual matching (MERGE)\n")
        f.write("- Complete phantoms (DELETE)\n\n")
        
        if len(unmatched_fathom) <= 50:
            for name in sorted(unmatched_fathom):
                f.write(f"- {name} ({fathom_participants[name]['record_count']} records)\n")
        else:
            f.write(f"(Too many to list - {len(unmatched_fathom)} total)\n")
            f.write(f"See database query: `SELECT DISTINCT name FROM participants WHERE data_source = 'fathom_ai'`\n")
        
        f.write("\n---\n\n")
        f.write("## Next Steps\n\n")
        f.write("1. ✅ Review this report\n")
        f.write("2. ✅ Verify name corrections look correct\n")
        f.write("3. ✅ Check member/donor counts match expectations\n")
        f.write("4. ➡️  Proceed to Phase 4B-2: Review unmatched Fathom participants\n")
        f.write("5. ➡️  Then Phase 4B-3: Add Airtable-only people to database\n")
    
    print(f"✅ Report saved: {REPORT_PATH}")


def main(csv_path=None):
    print()
    print("=" * 60)
    print("PHASE 4B-1: ENRICH FATHOM PARTICIPANTS WITH AIRTABLE DATA")
    print("=" * 60)
    print()
    print("What this does:")
    print("  ✅ Fuzzy match Fathom → Airtable")
    print("  ✅ UPDATE Fathom records with Airtable data")
    print("  ✅ Correct AI misspellings (Airtable is ground truth)")
    print("  ✅ Add member/donor/email/project data")
    print("  ✅ DELETE 'drop' entries from Fathom")
    print("  ❌ Does NOT insert new people (Phase 4B-3)")
    print()
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # STEP 1: Connect to database (read-only for now)
    conn = get_db_connection()
    
    # STEP 2: Verify integrity
    verify_database_integrity(conn)
    
    # STEP 3: Load data
    airtable_people = load_airtable_data()
    fathom_participants = load_fathom_participants(conn)
    
    # STEP 4: Fuzzy match (no modifications yet)
    matches = fuzzy_match_names(fathom_participants, airtable_people)
    
    # STEP 5: Generate EDITABLE approval table
    approval_table_path = generate_editable_approval_table(matches, fathom_participants, airtable_people)
    
    # STEP 6: PAUSE - User edits approval table
    print()
    print("=" * 60)
    print("⏸️  REVIEW & EDIT REQUIRED")
    print("=" * 60)
    print()
    print(f"📊 Approval table: {approval_table_path}")
    print()
    print("Instructions:")
    print("  1. Open the approval table in your editor")
    print("  2. Click Fathom video links ([*]) to verify people")
    print("  3. Check ☑ boxes to approve good matches")
    print("  4. Uncheck ☐ or add comments for bad matches")
    print("  5. SAVE the file when done")
    print()
    input("Press ENTER when you've edited and saved the approval table...")
    print()
    
    # STEP 7: Parse user's approvals
    approvals = parse_approval_table(approval_table_path)
    
    if not approvals:
        print()
        print("❌ No matches approved - aborting")
        print("   Database unchanged")
        print(f"   Approval table: {approval_table_path}")
        conn.close()
        sys.exit(0)
    
    # STEP 8: Filter matches to only approved ones
    approved_matches = {name: match_data for name, match_data in matches.items() 
                       if name in approvals}
    
    # Extract user comments for final report
    user_comments = {name: approvals[name]['comment'] for name in approved_matches.keys()}
    
    print()
    print("=" * 60)
    print("PROCEEDING WITH APPROVED MATCHES")
    print("=" * 60)
    print(f"  - Total matches found: {len(matches)}")
    print(f"  - User approved: {len(approved_matches)}")
    print(f"  - Will be updated: {len(approved_matches)}")
    print()
    
    # Update matches to only approved ones
    matches = approved_matches
    
    # STEP 9: NOW create backup (only if user approved)
    require_backup()
    
    # STEP 10: Add columns if needed
    try:
        conn.execute("BEGIN TRANSACTION")
        add_enrichment_columns(conn)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"❌ ERROR adding columns: {e}")
        conn.close()
        sys.exit(1)
    
    # STEP 11: Enrich participants
    try:
        conn.execute("BEGIN TRANSACTION")
        stats, corrections = enrich_participants(conn, matches)
        conn.commit()
        print("\n✅ Database modifications committed successfully")
    except Exception as e:
        conn.rollback()
        print(f"\n❌ ERROR during enrichment: {e}")
        print("Transaction rolled back - database unchanged")
        print("\n💡 Database restored to pre-modification state")
        conn.close()
        sys.exit(1)
    finally:
        conn.close()
    
    # STEP 12: Generate FINAL report with user comments
    generate_final_report(matches, stats, corrections, fathom_participants, airtable_people, user_comments)
    
    print()
    print("=" * 60)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    print(f"📊 Approval table: {approval_table_path}")
    print(f"📊 Final report: {REPORT_PATH}")
    print()
    print("🎯 Next step: Review final report, then proceed to Phase 4B-2")


if __name__ == "__main__":
    main()
