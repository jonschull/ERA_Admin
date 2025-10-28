#!/usr/bin/env python3
"""
Create V7 by removing APPROVED entries from V6.
"""

import re
from pathlib import Path

V6_FILE = Path(__file__).parent / 'ERA_MEMBERS_LACKING_BIOS_V6.md'
V7_FILE = Path(__file__).parent / 'ERA_MEMBERS_LACKING_BIOS_V7.md'

def main():
    with open(V6_FILE, 'r') as f:
        content = f.read()
    
    # Split into sections
    lines = content.split('\n')
    
    # Find where members section starts
    members_start = None
    for i, line in enumerate(lines):
        if line.startswith('# Members Without Bios'):
            members_start = i
            break
    
    if members_start is None:
        print("Could not find members section")
        return
    
    # Extract header and members
    header = '\n'.join(lines[:members_start])
    members_section = '\n'.join(lines[members_start:])
    
    # Split members by ## headers
    member_pattern = r'(## \d+\. .+?)(?=\n## \d+\. |\Z)'
    members = re.findall(member_pattern, members_section, re.DOTALL)
    
    # Filter out APPROVED members
    non_approved = []
    approved_count = 0
    
    for member in members:
        if ' APPROVED' in member.split('\n')[0]:
            approved_count += 1
        else:
            non_approved.append(member)
    
    print(f"V6 had {len(members)} total members")
    print(f"Removing {approved_count} APPROVED members")
    print(f"V7 will have {len(non_approved)} remaining members")
    
    # Update header stats
    header = header.replace('Version 6', 'Version 7')
    header = header.replace('- **Total ERA Members Needing Bios:** 46', 
                          f'- **Total ERA Members Needing Bios:** {len(non_approved)}')
    header = header.replace('- **Removed This Iteration:** 5 APPROVED + 4 non-members',
                          f'- **Removed This Iteration:** {approved_count} APPROVED (processed to database)')
    
    # Add V7 recent changes
    v7_changes = """## Recent Changes (V7 - October 27, 2025)

- ✅ **V6 Processing Complete** - 16 APPROVED members processed to database
  - 6 ERA Africa participants tagged (Emmanuel Uramutse, Fadja Robert, Hashim Yussif, Mtokani Saleh, Mutasa Brian, Theopista Abalo)
  - 5 database corruptions fixed (Kaluki Paul Mutuku, Minot Weld, Roberto Forte, Roberto Pedraza Ruiz, Scott Schulte)
  - 2 non-members corrected (Fred Ogden, Scott Schulte - era_member set to 0)
  - 1 duplicate merged (nding'a ndikon merged into Joshua Laizer)
- 📊 **V7 ready** - {remaining} members remaining (non-APPROVED entries from V6)

---

## Recent Changes (V6)
""".format(remaining=len(non_approved))
    
    header = header.replace('## Recent Changes\n\n', v7_changes)
    
    # Reconstruct V7
    v7_content = header + '\n\n# Members Without Bios\n\n' + '\n\n---\n\n'.join(non_approved)
    
    # Write V7
    with open(V7_FILE, 'w') as f:
        f.write(v7_content)
    
    print(f"\n✅ Created {V7_FILE}")
    print(f"   {len(non_approved)} members remaining")

if __name__ == '__main__':
    main()
