#!/usr/bin/env python3
"""
Parse analysis_results.txt and convert to structured CSV format.

This script extracts participant information from Fathom AI analysis results
and creates a CSV with columns: Name, Location, Affiliation, Collaborating_People, 
Collaborating_Organizations, Source_Call_Title, Source_Call_URL

Preserves duplicates (same person in multiple calls gets multiple rows).
"""

import re
import csv
import sys
from typing import List, Dict, Optional

class AnalysisResultsParser:
    def __init__(self, input_file: str = "analysis_results.txt", output_file: str = "participants.csv"):
        self.input_file = input_file
        self.output_file = output_file
        self.participants = []
        self.current_call_title = ""
        self.current_call_url = ""
        
    def parse_file(self):
        """Parse the analysis results file and extract participant data."""
        print(f"📖 Parsing {self.input_file}...")
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into individual call analysis blocks
        blocks = content.split('=' * 40)
        
        print(f"📊 Found {len(blocks)} analysis blocks")
        
        for i, block in enumerate(blocks):
            if not block.strip():
                continue
                
            self._parse_block(block, i)
        
        print(f"✅ Extracted {len(self.participants)} participant records")
        return self.participants
    
    def _parse_block(self, block: str, block_num: int):
        """Parse a single analysis block for one call."""
        lines = block.strip().split('\n')
        
        # Extract call information
        call_title = ""
        call_url = ""
        
        for line in lines:
            if line.startswith("## Call:"):
                call_title = line.replace("## Call:", "").strip()
            elif line.startswith("URL:"):
                call_url = line.replace("URL:", "").strip()
                break
        
        if not call_url:
            print(f"⚠️  Block {block_num}: No URL found, skipping")
            return
        
        # Find the AI response section
        ai_response_start = -1
        for i, line in enumerate(lines):
            if "--- Fathom AI Response ---" in line:
                ai_response_start = i + 1
                break
        
        if ai_response_start == -1:
            print(f"⚠️  Block {block_num}: No AI response found, skipping")
            return
        
        # Parse participant data from AI response
        ai_response = '\n'.join(lines[ai_response_start:])
        participants = self._extract_participants(ai_response, call_title, call_url)
        
        self.participants.extend(participants)
        
        if participants:
            print(f"✅ Block {block_num}: Extracted {len(participants)} participants from '{call_title}'")
        else:
            print(f"⚠️  Block {block_num}: No participants found in '{call_title}'")
    
    def _extract_participants(self, ai_response: str, call_title: str, call_url: str) -> List[Dict]:
        """Extract individual participants from AI response text."""
        participants = []
        
        # Split by "Name:" to get individual participant blocks
        name_blocks = re.split(r'\nName:', ai_response)
        
        for i, block in enumerate(name_blocks):
            if not block.strip():
                continue
            
            # Add back "Name:" prefix (except for first block which might already have it)
            if i > 0:
                block = "Name:" + block
            
            participant = self._parse_participant_block(block, call_title, call_url)
            if participant:
                participants.append(participant)
        
        return participants
    
    def _parse_participant_block(self, block: str, call_title: str, call_url: str) -> Optional[Dict]:
        """Parse a single participant's information block."""
        participant = {
            'Name': '',
            'Location': '',
            'Affiliation': '',
            'Collaborating_People': '',
            'Collaborating_Organizations': '',
            'Source_Call_Title': call_title,
            'Source_Call_URL': call_url
        }
        
        lines = block.strip().split('\n')
        current_field = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for field headers
            if line.startswith('Name:'):
                current_field = 'Name'
                participant['Name'] = line.replace('Name:', '').strip()
            elif line.startswith('Location:'):
                current_field = 'Location'
                participant['Location'] = line.replace('Location:', '').strip()
            elif line.startswith('Affiliation:'):
                current_field = 'Affiliation'
                participant['Affiliation'] = line.replace('Affiliation:', '').strip()
            elif line.startswith('Collaborating with People:'):
                current_field = 'Collaborating_People'
                people = line.replace('Collaborating with People:', '').strip()
                # Convert comma-separated to semicolon-separated for CSV safety
                participant['Collaborating_People'] = people.replace(',', ';')
            elif line.startswith('Collaborating with Organizations:'):
                current_field = 'Collaborating_Organizations'
                orgs = line.replace('Collaborating with Organizations:', '').strip()
                # Convert comma-separated to semicolon-separated for CSV safety
                participant['Collaborating_Organizations'] = orgs.replace(',', ';')
            elif current_field and line:
                # Continuation of previous field (multi-line content)
                if current_field == 'Collaborating_People':
                    if participant['Collaborating_People']:
                        participant['Collaborating_People'] += '; ' + line.replace(',', ';')
                    else:
                        participant['Collaborating_People'] = line.replace(',', ';')
                elif current_field == 'Collaborating_Organizations':
                    if participant['Collaborating_Organizations']:
                        participant['Collaborating_Organizations'] += '; ' + line.replace(',', ';')
                    else:
                        participant['Collaborating_Organizations'] = line.replace(',', ';')
                else:
                    # For other fields, append with space
                    if participant[current_field]:
                        participant[current_field] += ' ' + line
                    else:
                        participant[current_field] = line
        
        # Only return participant if we have at least a name
        if participant['Name']:
            return participant
        else:
            return None
    
    def write_csv(self):
        """Write participants data to CSV file."""
        if not self.participants:
            print("❌ No participants to write")
            return
        
        print(f"📝 Writing {len(self.participants)} participants to {self.output_file}...")
        
        fieldnames = [
            'Name', 
            'Location', 
            'Affiliation', 
            'Collaborating_People', 
            'Collaborating_Organizations', 
            'Source_Call_Title', 
            'Source_Call_URL'
        ]
        
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.participants)
        
        print(f"✅ CSV written successfully: {self.output_file}")
    
    def print_summary(self):
        """Print summary statistics."""
        if not self.participants:
            return
        
        unique_names = set(p['Name'] for p in self.participants)
        unique_calls = set(p['Source_Call_URL'] for p in self.participants)
        
        print(f"\n📊 PARSING SUMMARY:")
        print(f"- Total participant records: {len(self.participants)}")
        print(f"- Unique names: {len(unique_names)}")
        print(f"- Unique calls: {len(unique_calls)}")
        print(f"- Average participants per call: {len(self.participants) / len(unique_calls):.1f}")
        
        # Sample of names
        print(f"\n👥 Sample names extracted:")
        for name in sorted(unique_names)[:10]:
            print(f"   - {name}")
        if len(unique_names) > 10:
            print(f"   ... and {len(unique_names) - 10} more")

def main():
    parser = AnalysisResultsParser()
    
    try:
        parser.parse_file()
        parser.write_csv()
        parser.print_summary()
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find {parser.input_file}")
        print("   Make sure you're running this script in the analysis/ directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
