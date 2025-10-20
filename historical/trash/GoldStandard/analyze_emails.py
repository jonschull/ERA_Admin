import os
import csv
import sqlite3
from bs4 import BeautifulSoup

# --- Configuration ---
# Construct an absolute path to the TSV file
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir) # Go up one level from FathomInventory_Clean
MASTER_TSV_FILE = os.path.join(project_root, 'GoldStandard', 'all_fathom_calls.tsv')
DB_FILE = "fathom_emails.db"

def get_tsv_ids():
    """Reads the master TSV and returns a set of unique Fathom call IDs."""
    if not os.path.exists(MASTER_TSV_FILE):
        print(f"Error: Master TSV file not found at {MASTER_TSV_FILE}")
        return set()
    
    ids = set()
    with open(MASTER_TSV_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        try:
            header = [h.strip() for h in next(reader)]
            hyperlink_index = header.index('Hyperlink')
        except (StopIteration, ValueError):
            return set()

        for row in reader:
            if len(row) > hyperlink_index:
                link = row[hyperlink_index].strip()
                if link and 'fathom.video/calls/' in link:
                    call_id = link.split('/')[-1]
                    ids.add(call_id)
    return ids

def extract_fathom_id_from_html(body_html):
    """Extracts the Fathom call/share ID from the email body HTML."""
    if not body_html:
        return None
    soup = BeautifulSoup(body_html, 'html.parser')
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if 'fathom.video/share/' in href:
            return href.split('/')[-1].split('?')[0]
    return None

def get_emails_from_db():
    """Fetches all email bodies from the local SQLite database."""
    if not os.path.exists(DB_FILE):
        return []
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT body_html FROM emails')
    emails = cursor.fetchall()
    conn.close()
    return emails

def main():
    """Analyzes emails from the local database and compares them to the master TSV."""
    # 1. Read IDs from the master TSV file
    print(f"Reading call IDs from {MASTER_TSV_FILE}...")
    tsv_ids = get_tsv_ids()
    print(f"Found {len(tsv_ids)} unique call IDs in the master TSV.")
    if tsv_ids:
        print("  - First 5 TSV IDs:", sorted(list(tsv_ids))[:5])

    # 2. Read emails from the local database and extract unique IDs
    print(f"Reading emails from local database ('{DB_FILE}')...")
    local_emails = get_emails_from_db()
    if not local_emails:
        print("No emails found in the local database. Run download_emails.py first.")
        return

    print(f"Found {len(local_emails)} emails. Extracting unique call IDs...")
    email_ids = set()
    for i, row in enumerate(local_emails):
        body_html = row[0]
        if body_html:
            call_id = extract_fathom_id_from_html(body_html)
            if call_id:
                email_ids.add(call_id)
    print("ID extraction complete.")
    if email_ids:
        print("  - First 5 Email IDs:", sorted(list(email_ids))[:5])

    # 3. Save the extracted IDs to separate files
    print("\n--- Analysis Complete ---")
    print(f"Found {len(tsv_ids)} unique Call IDs in the master TSV.")
    print(f"Found {len(email_ids)} unique Share IDs in the emails.")

    # Save TSV IDs
    with open('tsv_call_ids.txt', 'w') as f:
        for call_id in sorted(list(tsv_ids)):
            f.write(f"{call_id}\n")
    print(f"Saved TSV Call IDs to 'tsv_call_ids.txt'")

    # Save Email IDs
    with open('email_share_ids.txt', 'w') as f:
        for share_id in sorted(list(email_ids)):
            f.write(f"{share_id}\n")
    print(f"Saved Email Share IDs to 'email_share_ids.txt'")

    print("\nNote: The Call IDs from the TSV and the Share IDs from emails are different formats and cannot be directly compared.")

if __name__ == '__main__':
    main()
