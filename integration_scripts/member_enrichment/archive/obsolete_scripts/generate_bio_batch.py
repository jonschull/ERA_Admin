#!/usr/bin/env python3
"""
Generate a batch of bio review files for human review.

Workflow:
1. Script generates bio + review page for each member
2. Human reviews, edits bios directly, adds comments
3. Human marks status: APPROVED / NEEDS_REVISION / PENDING
4. process_batch_feedback.py collects approved bios
"""

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
AGGREGATED_DATA = SCRIPT_DIR / "batches" / "aggregated_data"
BATCH_REVIEW_DIR = SCRIPT_DIR / "batches" / "batch_reviews"
BATCH_REVIEW_DIR.mkdir(exist_ok=True, parents=True)

def load_member_data(name_slug):
    """Load aggregated JSON for member."""
    json_path = AGGREGATED_DATA / f"{name_slug}.json"
    if not json_path.exists():
        return None
    with open(json_path) as f:
        return json.load(f)

def create_review_page(member_name, bio, char_count, data_concerns, batch_num):
    """Create review page for human to edit/approve."""
    
    name_slug = member_name.replace(' ', '_').lower()
    member_data = load_member_data(name_slug)
    
    if not member_data:
        print(f"⚠️  No aggregated data found for {member_name}")
        return None
    
    review_file = BATCH_REVIEW_DIR / f"batch{batch_num}_{name_slug}.md"
    
    content = []
    content.append(f"# BIO REVIEW: {member_name}")
    content.append("")
    content.append(f"**Batch:** {batch_num}")
    content.append(f"**Status:** PENDING")
    content.append("")
    content.append("---")
    content.append("")
    content.append("## PROPOSED BIO")
    content.append("")
    content.append("*(Edit directly below. Keep 600-950 chars)*")
    content.append("")
    content.append(bio)
    content.append("")
    content.append(f"**Character count:** {char_count}")
    content.append("")
    content.append("---")
    content.append("")
    content.append("## REVIEW CHECKLIST")
    content.append("")
    content.append("- [ ] Accurate (verified against sources)")
    content.append("- [ ] Right tone (professional but warm)")
    content.append("- [ ] Right length (600-950 chars)")
    content.append("- [ ] ERA connection clear")
    content.append("- [ ] Story not resume")
    content.append("")
    content.append("---")
    content.append("")
    content.append("## DATA CONCERNS")
    content.append("")
    content.append(data_concerns)
    content.append("")
    content.append("---")
    content.append("")
    content.append("## CONTACT INFO")
    content.append("")
    db = member_data.get('database', {})
    at = member_data.get('airtable', {})
    
    content.append(f"**Email:** {db.get('email') or at.get('email') or 'None'}")
    content.append(f"**Location:** {db.get('location', 'Unknown')}")
    content.append(f"**Affiliation:** {db.get('affiliation', 'Unknown')}")
    
    phone_info = member_data.get('phone_info')
    if phone_info and phone_info.get('phones'):
        phones = ', '.join([p['number'] for p in phone_info['phones']])
        content.append(f"**Phone:** {phones}")
    
    content.append("")
    content.append("---")
    content.append("")
    content.append("## AFFILIATED ORGS")
    content.append("")
    content.append(f"*(From Airtable: {at.get('affiliated_orgs', 'None')})*")
    content.append("")
    content.append("**Orgs to link:** *(add/edit as needed)*")
    content.append("")
    
    content.append("---")
    content.append("")
    content.append("## COMMENTS / INSTRUCTIONS")
    content.append("")
    content.append("*(Add any notes for AI here)*")
    content.append("")
    content.append("---")
    content.append("")
    content.append("## APPROVAL")
    content.append("")
    content.append("**Change status above to one of:**")
    content.append("- `APPROVED` - Ready for Airtable")
    content.append("- `NEEDS_REVISION` - See comments section")
    content.append("- `PENDING` - Still reviewing")
    content.append("")
    
    with open(review_file, 'w') as f:
        f.write('\n'.join(content))
    
    return review_file

def main():
    """Generate batch review files."""
    
    if len(sys.argv) < 3:
        print("Usage: python3 generate_bio_batch.py <batch_num> <name1> <name2> ...")
        print("Example: python3 generate_bio_batch.py 4 'Alice Smith' 'Bob Jones'")
        sys.exit(1)
    
    batch_num = sys.argv[1]
    member_names = sys.argv[2:]
    
    print("=" * 80)
    print(f"GENERATING BIO BATCH {batch_num} REVIEW FILES")
    print("=" * 80)
    print()
    
    # First, generate bios using sub-agent pattern
    print("STEP 1: Generate bios (sub-agent mode)")
    print()
    print("For each member, I will:")
    print("1. Read their aggregated data")
    print("2. Write bio following standards")
    print("3. Create review page")
    print()
    
    review_files = []
    
    for member_name in member_names:
        print(f"Processing: {member_name}")
        print("-" * 80)
        
        # Load data
        name_slug = member_name.replace(' ', '_').lower()
        member_data = load_member_data(name_slug)
        
        if not member_data:
            print(f"❌ No aggregated data found - run aggregate_member_info.py first")
            print()
            continue
        
        # This is where we'd call sub-agent (for now, placeholder)
        print(f"   ⏳ Waiting for bio from sub-agent...")
        print(f"   Tell Claude: 'Write bio for {member_name} from aggregated data'")
        print()
        
        # For now, create placeholder review file
        # User will see this and know we need the bio
        
    print("=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print()
    print(f"1. For each member, tell Claude:")
    print(f"   'Write bio for [name] using batch {batch_num} standards'")
    print()
    print(f"2. Claude writes bio with char count and data concerns")
    print()
    print(f"3. Run: python3 create_batch_reviews.py {batch_num} (after all bios written)")
    print()

if __name__ == "__main__":
    main()
