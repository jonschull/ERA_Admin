#!/usr/bin/env python3
"""
Final extraction - get exactly 206 cases from conversation, handling corrections.
Strategy: Extract batches in order, apply corrections as we encounter them.
"""

import re
import json

def main():
    with open('/Users/admin/Downloads/Database Reconciliation Audit.md', 'r') as f:
        content = f.read()
    
    # Extract ALL JSON blocks in order
    pattern = r'```json(.*?)```'
    all_json_blocks = []
    
    for match in re.finditer(pattern, content, re.DOTALL):
        try:
            data = json.loads(match.group(1))
            all_json_blocks.append(data)
        except:
            pass
    
    print(f"Found {len(all_json_blocks)} valid JSON blocks")
    
    # Process blocks to build the 206 cases
    # Strategy: Take arrays of 10, handle single corrections
    final_cases = []
    corrections = {}  # variant -> case data
    
    for block in all_json_blocks:
        if isinstance(block, list):
            # Array of cases - likely a batch
            if block and 'variant' in block[0]:
                print(f"Batch: {len(block)} cases starting with {block[0]['variant']}")
                final_cases.extend(block)
        elif isinstance(block, dict) and 'variant' in block:
            # Single case - likely a correction
            print(f"Correction: {block['variant']}")
            corrections[block['variant']] = block
    
    print(f"\nExtracted {len(final_cases)} cases, {len(corrections)} corrections")
    
    # Apply corrections
    for i, case in enumerate(final_cases):
        variant = case['variant']
        if variant in corrections:
            # Update with correction
            final_cases[i] = corrections[variant]
            print(f"Applied correction to: {variant}")
    
    # Add case numbers
    for i, case in enumerate(final_cases, 1):
        case['case'] = i
    
    print(f"\nFinal count: {len(final_cases)} cases")
    
    # Convert JSON to Python syntax
    json_str = json.dumps(final_cases, indent=2)
    python_str = (json_str
                  .replace(': null', ': None')
                  .replace(': true', ': True')
                  .replace(': false', ': False'))
    
    # Save as Python file
    with open('all_206_categorizations.py', 'w') as f:
        f.write('#!/usr/bin/env python3\n')
        f.write('"""All categorizations from conversation (with corrections)"""\n\n')
        f.write('CATEGORIZATIONS = ')
        f.write(python_str)
        f.write('\n\nif __name__ == "__main__":\n')
        f.write('    import json\n')
        f.write('    # Convert None back to null for JSON\n')
        f.write('    import copy\n')
        f.write('    data = copy.deepcopy(CATEGORIZATIONS)\n')
        f.write('    for case in data:\n')
        f.write('        for key, val in case.items():\n')
        f.write('            if val is None:\n')
        f.write('                case[key] = None  # JSON null\n')
        f.write('    with open("all_206_categorizations.json", "w") as f:\n')
        f.write('        json.dump(data, f, indent=2)\n')
        f.write('    print(f"Saved {len(data)} cases")\n')
    
    print(f"Saved to all_206_categorizations.py")
    print(f"\nFirst: {final_cases[0]['variant'] if final_cases else 'none'}")
    print(f"Last: {final_cases[-1]['variant'] if final_cases else 'none'}")

if __name__ == "__main__":
    main()
