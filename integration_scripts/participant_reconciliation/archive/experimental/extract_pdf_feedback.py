#!/usr/bin/env python3
"""
Extract feedback from the PDF file.
"""

from pypdf import PdfReader
import re

pdf_path = "/Users/admin/Downloads/Claude's AI Recommendations - Phase 4B-2.pdf"
output_path = "/tmp/pdf_feedback.txt"

# Read the PDF
reader = PdfReader(pdf_path)

# Extract text from all pages
full_text = ""
for page in reader.pages:
    full_text += page.extract_text() + "\n"

# Save extracted text
with open(output_path, 'w') as f:
    f.write(full_text)

print(f"✅ Extracted {len(reader.pages)} pages from PDF")
print(f"📄 Saved to: {output_path}")
print(f"📊 Total characters: {len(full_text)}")
print("\n" + "="*80)
print("First 2000 characters:")
print("="*80)
print(full_text[:2000])
