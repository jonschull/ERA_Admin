#!/usr/bin/env python3
"""
Generate documentation tree from NAVIGATION_WIREFRAME.md

Parses ## FILE: sections and creates actual documentation files.
"""

import re
import os
from pathlib import Path
from typing import List, Tuple

def parse_wireframe(wireframe_path: str) -> List[Tuple[str, str]]:
    """
    Parse wireframe and extract file sections.
    
    Returns: List of (file_path, content) tuples
    """
    with open(wireframe_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by ## FILE: markers
    file_sections = re.split(r'^## FILE: (.+?)$', content, flags=re.MULTILINE)[1:]  # Skip before first FILE
    
    sections = []
    # Process pairs: (filename, content)
    for i in range(0, len(file_sections), 2):
        if i + 1 < len(file_sections):
            file_path = file_sections[i].strip()
            file_content = file_sections[i + 1]
            
            # Find the actual content start (after **Path:** and blank line, before next section marker)
            # Stop at ## FILE: or ## Script Extraction Pattern or ---\n\n##
            stop_pattern = r'(?=^---\s*\n\s*\n## FILE:|^## Script Extraction Pattern)'
            content_match = re.split(stop_pattern, file_content, maxsplit=1, flags=re.MULTILINE)
            file_content = content_match[0] if content_match else file_content
            
            # Remove the **Path:** line and any leading whitespace
            file_content = re.sub(r'^\s*\*\*Path:\*\* `.+?`\s*\n\s*\n', '', file_content, flags=re.MULTILINE)
            
            # Clean up trailing whitespace and separator lines
            file_content = file_content.strip()
            file_content = re.sub(r'\n\s*---\s*$', '', file_content)
            
            if file_content:  # Only add if there's actual content
                sections.append((file_path, file_content))
    
    return sections


def convert_links(content: str, current_file: str) -> str:
    """
    Convert #file-* anchor links to actual relative paths.
    
    Example: [README](#file-readmemd) -> [README](../README.md)
    """
    # Map anchor IDs to file paths
    link_map = {
        'file-readmemd': 'README.md',
        'file-context_recoverymd': 'CONTEXT_RECOVERY.md',
        'file-ai_handoff_guidemd': 'AI_HANDOFF_GUIDE.md',
        'file-working_principlesmd': 'WORKING_PRINCIPLES.md',
        'file-fathominventoryreadmemd': 'FathomInventory/README.md',
        'file-fathominventorycontext_recoverymd': 'FathomInventory/CONTEXT_RECOVERY.md',
        'file-fathominventoryauthenticationreadmemd': 'FathomInventory/authentication/README.md',
        'file-airtablereadmemd': 'airtable/README.md',
        'file-integration_scriptsreadmemd': 'integration_scripts/README.md',
        'file-integration_scriptsai_workflow_guidemd': 'integration_scripts/AI_WORKFLOW_GUIDE.md',
    }
    
    def replace_link(match):
        link_text = match.group(1)
        anchor = match.group(2)
        
        if anchor in link_map:
            target_path = link_map[anchor]
            
            # Use Path to calculate proper relative path
            from pathlib import Path
            current_path = Path(current_file)
            target = Path(target_path)
            
            # Get directory of current file
            current_dir = current_path.parent
            
            # Calculate relative path from current directory to target
            try:
                rel_path = os.path.relpath(target, current_dir)
            except ValueError:
                # Different drives or something - just use absolute
                rel_path = target_path
            
            return f'[{link_text}]({rel_path})'
        else:
            # Keep original if not found in map
            return match.group(0)
    
    # Pattern: [text](#anchor)
    pattern = r'\[([^\]]+)\]\(#([^\)]+)\)'
    return re.sub(pattern, replace_link, content)


def generate_files(sections: List[Tuple[str, str]], output_dir: str):
    """
    Generate actual files from parsed sections.
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print(f"Generating documentation tree in: {output_dir}\n")
    
    for file_path, content in sections:
        # Convert internal links
        content_with_links = convert_links(content, file_path)
        
        # Add title with relative path at the top
        # Convert path to title-case display
        if file_path == 'README.md':
            title = "# ERA Admin - System Overview\n\n"
        else:
            # Use the file path as the title for disambiguation
            title = f"# {file_path}\n\n"
        
        # Combine title + content
        final_content = title + content_with_links
        
        # Create full path
        full_path = output_path / file_path
        
        # Create parent directories
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print(f"✅ Created: {file_path}")
    
    print(f"\n🎉 Generated {len(sections)} files successfully!")


def main():
    """Main execution."""
    wireframe_path = 'NAVIGATION_WIREFRAME.md'
    output_dir = '../docs_generated'
    
    print("=" * 60)
    print("Documentation Generator from NAVIGATION_WIREFRAME.md")
    print("=" * 60)
    print()
    
    # Parse wireframe
    print(f"📖 Parsing: {wireframe_path}")
    sections = parse_wireframe(wireframe_path)
    print(f"✅ Found {len(sections)} file sections\n")
    
    # Show what will be created
    print("Files to be created:")
    for file_path, _ in sections:
        print(f"  - {file_path}")
    print()
    
    # Generate files
    generate_files(sections, output_dir)
    
    print()
    print("=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("1. Navigate to docs_generated/ directory")
    print("2. Test README.md and navigation links")
    print("3. Compare with originals")
    print("4. If satisfied, can replace originals")
    print()


if __name__ == '__main__':
    main()
