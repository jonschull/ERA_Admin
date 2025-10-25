#!/usr/bin/env python3
"""
Extract all 206 categorizations from the exported conversation markdown.
This ensures complete fidelity by extracting exactly what was approved.
"""

import json
import re

def extract_categorizations():
    """Extract all categorizations from the markdown conversation export."""
    
    with open('/Users/admin/Downloads/Database Reconciliation Audit.md', 'r') as f:
        content = f.read()
    
    # Find all batch headers and their JSON blocks
    # Pattern: # Cases X-Y followed by JSON block
    batch_pattern = r'# Cases (\d+)-(\d+).*?```json\s*\[(.*?)\]```'
    
    all_cases = []
    case_counter = 1
    
    for match in re.finditer(batch_pattern, content, re.DOTALL):
        start_case = int(match.group(1))
        end_case = int(match.group(2))
        json_text = '[' + match.group(3) + ']'
        
        try:
            cases = json.loads(json_text)
            print(f"Batch {start_case}-{end_case}: found {len(cases)} cases")
            
            for i, case in enumerate(cases):
                if 'variant' in case:
                    # Add case number based on position
                    case_num = start_case + i
                    case['case'] = case_num
                    all_cases.append(case)
                    print(f"  Case {case_num}: {case['variant']}")
        except json.JSONDecodeError as e:
            print(f"ERROR parsing batch {start_case}-{end_case}: {e}")
            continue
    
    return all_cases

if __name__ == "__main__":
    print("Extracting all categorizations from markdown export...")
    print()
    
    categorizations = extract_categorizations()
    
    print()
    print(f"Total cases extracted: {len(categorizations)}")
    
    # Save to Python file
    with open('all_206_categorizations_EXTRACTED.py', 'w') as f:
        f.write('''#!/usr/bin/env python3
"""
All 206 participant categorizations extracted from conversation export.
Generated automatically from: Database Reconciliation Audit.md
Each case was reviewed and approved by user.
"""

CATEGORIZATIONS = ''')
        f.write(json.dumps(categorizations, indent=2))
        f.write('''

if __name__ == "__main__":
    import json
    print(f"Total cases: {len(CATEGORIZATIONS)}")
    with open('all_206_categorizations.json', 'w') as f:
        json.dump(CATEGORIZATIONS, f, indent=2)
    print("Saved to all_206_categorizations.json")
''')
    
    print(f"Saved to: all_206_categorizations_EXTRACTED.py")
    print()
    print("To generate JSON:")
    print("  python3 all_206_categorizations_EXTRACTED.py")
