import csv
import subprocess
import sys
import os
import re
import argparse

# --- Configuration ---
INPUT_CSV = 'era connections.tsv'
OUTPUT_FILE = 'analysis_results.txt'
QUESTION = """I'd like information on each participant in the following format

Name: John Smith
Location: Unknown
Affiliation: ecorestoration alliance
Collaborating with People: <name>, <name>, <name>, etc.
Collaborating with Organizations: <organization>, <organization>, <organization>, etc."""

def get_completed_urls(filename):
    """Parses the output file to find URLs that have already been successfully analyzed."""
    completed_urls = set()
    if not os.path.exists(filename):
        return completed_urls
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all successfully processed calls by looking for the separator
        blocks = content.split('='*40)
        for block in blocks:
            if "Navigating to:" in block and "--- Fathom AI Response ---" in block:
                match = re.search(r"URL: (https://fathom.video/calls/\d+)", block)
                if match:
                    completed_urls.add(match.group(1))
    except Exception as e:
        print(f"Warning: Could not parse existing results file. Will re-run all analyses. Error: {e}")

    return completed_urls

def main(limit=None):
    """Reads a TSV file, and for rows marked for analysis, runs the ask_fathom_ai.py script.
    
    Args:
        limit: Maximum number of calls to analyze (for testing). None = no limit.
    """
    completed_urls = get_completed_urls(OUTPUT_FILE)
    if completed_urls:
        print(f"Found {len(completed_urls)} previously completed analyses. Resuming...")
    
    if limit:
        print(f"⚠️  LIMIT MODE: Will analyze maximum {limit} calls")

    try:
        with open(INPUT_CSV, 'r', encoding='utf-8') as infile, open(OUTPUT_FILE, 'a', encoding='utf-8') as outfile:
            reader = csv.reader(infile, delimiter='\t')
            
            try:
                header = next(reader)
            except StopIteration:
                print(f"Error: Input file '{INPUT_CSV}' is empty.")
                return

            # Write header if the file is new
            if os.path.getsize(OUTPUT_FILE) == 0:
                outfile.write(f"Fathom AI Analysis Results\nQuestion: {QUESTION}\n{'='*40}\n\n")

            # Find column indices dynamically
            try:
                title_col = header.index('Title')
                analyze_col = header.index('Analyze')
                hyperlink_col = header.index('Hyperlink')
                date_col = header.index('Date')
            except ValueError as e:
                print(f"Error: Missing expected column in {INPUT_CSV}: {e}")
                return

            print(f"Starting batch analysis. New results will be appended to {OUTPUT_FILE}")

            analyzed_count = 0
            for i, row in enumerate(reader):
                if limit and analyzed_count >= limit:
                    print(f"\n⚠️  Reached limit of {limit} analyses. Stopping.")
                    break
                if len(row) <= max(title_col, analyze_col, hyperlink_col):
                    print(f"Skipping malformed row {i+2}: not enough columns.")
                    continue

                analyze_flag = row[analyze_col].strip()
                hyperlink = row[hyperlink_col].strip()
                title = row[title_col].strip()
                date = row[date_col].strip()

                if analyze_flag.strip() and hyperlink:  # Accept any non-empty value (x, 1, etc.)
                    if hyperlink in completed_urls:
                        print(f"Skipping already analyzed call from {date}: '{title}' ({hyperlink})")
                        continue

                    print(f"Analyzing call: '{title}' ({hyperlink})...")
                    
                    output_buffer = []
                    try:
                        command = [
                            sys.executable,
                            '-u',
                            'ask_fathom_ai.py',
                            hyperlink,
                            QUESTION
                        ]
                        
                        process = subprocess.Popen(
                            command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True,
                            encoding='utf-8'
                        )

                        for line in iter(process.stdout.readline, ''):
                            print(line, end='')
                            output_buffer.append(line)
                        
                        process.wait()
                        if process.returncode != 0:
                            raise subprocess.CalledProcessError(process.returncode, command, "".join(output_buffer))

                        # If successful, write the entire buffered output to the file
                        outfile.write(f"## Call: {title}\nURL: {hyperlink}\n\n")
                        outfile.writelines(output_buffer)
                        outfile.write(f"\n{'='*40}\n\n")
                        outfile.flush()
                        print("\nAnalysis successful. Results saved.")
                        analyzed_count += 1

                    except (subprocess.CalledProcessError, FileNotFoundError) as e:
                        print(f"\nFailed to analyze '{title}'. This call will be retried on the next run. Error: {e}")

    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_CSV}' not found.")

    print("Batch analysis complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Batch analyze Fathom calls')
    parser.add_argument('--limit', type=int, help='Maximum number of calls to analyze (for testing)')
    args = parser.parse_args()
    
    main(limit=args.limit)
