#!/usr/bin/env python3
"""
PILOT: Test Claude as BioWriter sub-agent via file protocol

Tests Deep Agents pattern: Orchestrator delegates to sub-agent with clean context.

Workflow:
1. Script prepares task files (data + prompt)
2. Script tells user: "Read task_N.txt and write bio"
3. Claude (sub-agent) reads task, writes bio
4. User pastes bio response into response_N.txt
5. Script collects all responses, creates comparison

NO API COSTS - uses Claude via Windsurf, tests the PATTERN.
"""

import json
import os
import sys
from pathlib import Path

# Setup
SCRIPT_DIR = Path(__file__).parent
AGGREGATED_DATA = SCRIPT_DIR / "batches" / "aggregated_data"
TASK_DIR = SCRIPT_DIR / "batches" / "bio_tasks"
TASK_DIR.mkdir(exist_ok=True, parents=True)

def load_member_data(name_slug):
    """Load aggregated JSON data for member."""
    json_path = AGGREGATED_DATA / f"{name_slug}.json"
    with open(json_path) as f:
        return json.load(f)

def extract_linkedin_text(name_slug):
    """Extract LinkedIn full_text if available."""
    linkedin_path = SCRIPT_DIR / "batches" / "linkedin_profiles" / f"{name_slug}.json"
    if linkedin_path.exists():
        with open(linkedin_path) as f:
            data = json.load(f)
            return data['extracted'].get('full_text', '')
    return None

def build_prompt(member_data, linkedin_text=None):
    """Build prompt with data consistency checks and examples."""
    
    name = member_data['name']
    db = member_data.get('database', {})
    at = member_data.get('airtable', {})
    linkedin = member_data.get('linkedin_matches', [])
    transcripts = member_data.get('transcript_mentions', [])
    phone = member_data.get('phone_info', {})
    
    # Build context from sources
    context = f"""
You are writing a professional bio for {name}, a member of the EcoRestoration Alliance (ERA).

## DATA SOURCES (Must verify internal consistency)

### Database Info:
- Location: {db.get('location', 'Unknown')}
- Affiliation: {db.get('affiliation', 'Unknown')}
- Email: {db.get('email', 'Unknown')}
- ERA Member: {db.get('era_member', 'Unknown')}
- Town Halls attended: {len(db.get('call_history', []))}

### LinkedIn (verify this matches the person):
"""
    
    if linkedin:
        match = linkedin[0]
        context += f"""
- Name: {match['linkedin_name']} (Match: {match['score']}% {match['type']})
- Position: {match['data']['position']}
- Company: {match['data']['company']}
- URL: {match['data']['url']}
"""
    else:
        context += "- No LinkedIn connection found\n"
    
    if linkedin_text:
        context += f"\n### LinkedIn Full Profile:\n{linkedin_text[:2000]}...\n"
    
    # Add transcript context
    if transcripts:
        context += f"\n### Town Hall Participation:\n"
        context += f"- Found in {len(transcripts)} transcript mentions\n"
        # Include first mention for context
        if transcripts:
            first = transcripts[0]
            context += f"\nSample mention:\n{first['context'][:500]}...\n"
    
    if phone:
        context += f"\n### Phone: {phone['phones'][0]['number']}\n"
    
    prompt = f"""{context}

## YOUR TASK

Write a professional bio (600-950 characters) for {name}.

## CRITICAL: DATA CONSISTENCY CHECK
Before writing, verify:
1. Does LinkedIn match the person? (Check name, location, affiliation consistency)
2. Is the email domain consistent with affiliation?
3. Do Town Hall mentions match the professional background?
4. If anything is inconsistent, NOTE IT and work with most reliable source (database/transcripts > LinkedIn)

## BIO REQUIREMENTS

**Style:**
- Third person, conversational
- Professional but warm
- Narrative flow (not resume-style)

**Required Elements:**
1. Current work/role
2. Professional background (brief)
3. ERA connection/engagement (specific, not generic)
4. Unique value/perspective they bring
5. Optional: Philosophy or personal touch

**Length:** 600-950 characters (aim for ~800)

**Tone Examples from Existing ERA Bios:**

EXAMPLE 1 (Fred Jennings, 616 chars):
"Ecological Economist. Fred Jennings is from Ipswich, Massachusetts, USA, where he has spent most of his life. He is an ecological economist with a B.A. from Harvard and a Ph.D. from Stanford, both in economics. Fred is also an avid conservationist and fly fisherman. He enjoys the outdoors, and has written about natural processes and about economic theory. He has 40 years of teaching and research experience, first in academics and then in economic litigation. He also enjoys his seasonal practice as a saltwater fly fishing guide in Ipswich, MA. Fred joined Biodiversity for a Livable Climate in 2016."

EXAMPLE 2 (Ananda Fitzsimmons, 489 chars):
"Ananda Fitzsimmons is an advocate for soil and water, a speaker and author of two books, Hydrate the Earth and Restoring the Pillars of Life. She is the president of the Board of Regeneration Canada, a non profit organization advancing regenerative agriculture and the Vice President of the Board of the EcoRestoration Alliance. Ananda founded Concentric Agriculture, a company which manufactures soil amendments from beneficial microorganisms. She is currently in Uganda."

## OUTPUT FORMAT

Return ONLY:
1. Your bio (no preamble)
2. Character count
3. Any data consistency concerns you noticed

Format:
BIO:
[your bio text here]

CHAR COUNT: [number]

DATA CONCERNS: [any inconsistencies or uncertainties]
"""
    
    return prompt

def prepare_task_file(member_name, task_number):
    """Prepare task file for sub-agent to read."""
    
    print(f"Preparing task for: {member_name}")
    print("=" * 80)
    
    # Load data
    name_slug = member_name.replace(' ', '_').lower()
    member_data = load_member_data(name_slug)
    linkedin_text = extract_linkedin_text(name_slug)
    
    # Build prompt
    prompt = build_prompt(member_data, linkedin_text)
    
    # Save task file
    task_file = TASK_DIR / f"task_{task_number}_{name_slug}.txt"
    with open(task_file, 'w') as f:
        f.write("# BIO WRITER SUB-AGENT TASK\n\n")
        f.write(f"**Task ID:** {task_number}\n")
        f.write(f"**Member:** {member_name}\n\n")
        f.write("---\n\n")
        f.write(prompt)
    
    print(f"✅ Task file created: {task_file.name}")
    print()
    
    return task_file

def wait_for_response(task_number, name_slug):
    """Wait for user to paste sub-agent response."""
    
    response_file = TASK_DIR / f"response_{task_number}_{name_slug}.txt"
    
    print(f"📝 Waiting for sub-agent response...")
    print(f"   Expected file: {response_file.name}")
    print()
    
    if response_file.exists():
        with open(response_file) as f:
            return f.read()
    else:
        return f"PENDING: Response file not created yet - {response_file.name}"

def main():
    """Run pilot - prepare tasks and wait for sub-agent responses."""
    
    # Get batch members from command line or use default
    if len(sys.argv) > 1 and sys.argv[1] == '--batch3':
        members = [
            ("Jacob Denlinger", "jacob_denlinger"),
            ("Mary Minton", "mary_minton"),
            ("Mark Luckenbach", "mark_luckenbach"),
            ("Rayan Naraqi Farhoumand", "rayan_naraqi_farhoumand")
        ]
        batch_name = "Batch 3"
    else:
        # Default: compare with approved bios
        members = [
            ("Ben Rubin", "ben_rubin"),
            ("Noura Angulo", "noura_angulo")
        ]
        batch_name = "Comparison with Approved"
    
    print("=" * 80)
    print(f"BIO WRITER SUB-AGENT PILOT - {batch_name}")
    print("=" * 80)
    print()
    print("Testing Deep Agents pattern: Orchestrator → Sub-Agent delegation")
    print()
    
    # Prepare all task files
    task_files = []
    for i, (member_name, slug) in enumerate(members, 1):
        task_file = prepare_task_file(member_name, i)
        task_files.append((i, member_name, slug, task_file))
    
    print("=" * 80)
    print("✅ ALL TASK FILES READY")
    print("=" * 80)
    print()
    print("INSTRUCTIONS FOR USER (Orchestrator):")
    print()
    for i, member_name, slug, task_file in task_files:
        print(f"{i}. Tell Claude: 'Read {task_file.name} and write the bio'")
        print(f"   Claude responds with bio")
        print(f"   Copy Claude's response to: response_{i}_{slug}.txt")
        print()
    
    print("Then run: python3 bio_writer_pilot.py --collect")
    print()
    
    # Check if we're in collection mode
    if '--collect' in sys.argv:
        collect_responses(members, batch_name)

def collect_responses(members, batch_name):
    """Collect sub-agent responses and create comparison."""
    
    print("=" * 80)
    print("COLLECTING SUB-AGENT RESPONSES")
    print("=" * 80)
    print()
    
    results = []
    
    for i, (member_name, slug) in enumerate(members, 1):
        response = wait_for_response(i, slug)
        results.append({
            'name': member_name,
            'subagent_output': response
        })
    
    # Save comparison file
    output = []
    output.append(f"# BIO WRITER SUB-AGENT PILOT - {batch_name}")
    output.append("")
    output.append("**Date:** October 26, 2025")
    output.append("**Sub-Agent:** Claude (via Windsurf)")
    output.append("**Pattern:** Deep Agents - Orchestrator → Sub-Agent with clean context")
    output.append("")
    output.append("=" * 80)
    output.append("")
    
    # If comparing with approved bios, load them
    approved_content = None
    approved_path = SCRIPT_DIR / "batches" / "approved_bios.md"
    if approved_path.exists():
        with open(approved_path) as f:
            approved_content = f.read()
    
    for result in results:
        output.append(f"## {result['name']}")
        output.append("")
        output.append("### Sub-Agent Output (Claude with clean context):")
        output.append("")
        output.append(result['subagent_output'])
        output.append("")
        
        # If we have approved bios, show comparison
        if approved_content and result['name'] in approved_content:
            output.append("### Original Bio (Claude with full conversation context):")
            output.append("")
            
            # Extract human version from approved_bios.md
            start = approved_content.find(f"## {result['name']}")
            if start > 0:
                section = approved_content[start:start+2000]
                lines = section.split('\n')
                bio_lines = []
                found_bio = False
                for line in lines[2:]:  # Skip name and blank
                    if line.strip() and not line.startswith('**'):
                        bio_lines.append(line)
                        found_bio = True
                    elif found_bio and line.startswith('**'):
                        break
                
                original_bio = '\n'.join(bio_lines)
                output.append(original_bio)
            
            output.append("")
            output.append("### Analysis:")
            output.append("- Does sub-agent version match quality of full-context version?")
            output.append("- Which has better mission connection?")
            output.append("- Which feels more like a story vs. LinkedIn summary?")
        
        output.append("")
        output.append("-" * 80)
        output.append("")
    
    # Save
    comparison_path = SCRIPT_DIR / "batches" / "bio_pilot_comparison.md"
    with open(comparison_path, 'w') as f:
        f.write('\n'.join(output))
    
    print("=" * 80)
    print(f"✅ Comparison saved: {comparison_path}")
    print()
    print("Review to assess:")
    print("  - Sub-agent pattern working? (clean context → quality output)")
    print("  - Accuracy (data consistency)")
    print("  - Tone (professional but warm?)")
    print("  - Mission connection (ERA engagement clear?)")
    print("  - Story vs. credentials (narrative flow?)")

if __name__ == "__main__":
    main()
