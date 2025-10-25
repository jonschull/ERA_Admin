#!/usr/bin/env python3
import json
import sqlite3
from pathlib import Path

DB_PATH = Path('/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db')

print("="*80)
print("COMPREHENSIVE VALIDATION OF ALL 280 CASES")
print("="*80)

# Load both sets of categorizations
with open('all_206_categorizations.json', 'r') as f:
    batch_174 = json.load(f)

with open('batch_106_approved_cases.json', 'r') as f:
    batch_106 = json.load(f)

all_cases = batch_174 + batch_106
print(f"\nTotal cases to validate: {len(all_cases)}")

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Validation checks
issues = []
warnings = []
successes = 0

print("\nValidating each case...")

for i, case in enumerate(all_cases, 1):
    variant = case['variant']
    target = case.get('target')
    action = case['action']
    
    # Check variant should not exist (unless MARK_VALIDATED or ADD_TO_AIRTABLE)
    cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (variant,))
    variant_exists = cursor.fetchone()[0] > 0
    
    if action in ['MERGE', 'REMOVE']:
        if variant_exists:
            issues.append(f"Case {i}: '{variant}' still exists (should be {action}ed)")
    elif action in ['MARK_VALIDATED', 'ADD_TO_AIRTABLE']:
        if not variant_exists:
            issues.append(f"Case {i}: '{variant}' missing (should exist with action {action})")
        else:
            # Check it's validated
            cursor.execute("SELECT validated_by_airtable FROM participants WHERE name = ?", (variant,))
            result = cursor.fetchone()
            validated = result[0] if result else 0
            if not validated:
                warnings.append(f"Case {i}: '{variant}' exists but not validated")
    
    # For MERGE actions, check target exists
    if action == 'MERGE' and target:
        cursor.execute("SELECT COUNT(*) FROM participants WHERE name = ?", (target,))
        target_exists = cursor.fetchone()[0] > 0
        if not target_exists:
            issues.append(f"Case {i}: Target '{target}' missing for variant '{variant}'")
        else:
            successes += 1
    elif action == 'REMOVE':
        if not variant_exists:
            successes += 1
    elif action in ['MARK_VALIDATED', 'ADD_TO_AIRTABLE']:
        if variant_exists:
            successes += 1
    
    # Progress indicator
    if i % 50 == 0:
        print(f"  Validated {i}/{len(all_cases)}...")

print(f"  Validated {len(all_cases)}/{len(all_cases)} ✓")

# Report results
print("\n" + "="*80)
print("VALIDATION RESULTS")
print("="*80)

print(f"\n✅ Successful: {successes}/{len(all_cases)}")
print(f"⚠️  Warnings: {len(warnings)}")
print(f"❌ Issues: {len(issues)}")

if warnings:
    print("\n⚠️  WARNINGS:")
    for w in warnings[:20]:
        print(f"  - {w}")
    if len(warnings) > 20:
        print(f"  ... and {len(warnings) - 20} more")

if issues:
    print("\n❌ ISSUES FOUND:")
    for issue in issues[:20]:
        print(f"  - {issue}")
    if len(issues) > 20:
        print(f"  ... and {len(issues) - 20} more")
else:
    print("\n🎉 NO ISSUES FOUND - All cases validated successfully!")

# Summary statistics
cursor.execute("""
    SELECT 
        COUNT(DISTINCT name) as total,
        SUM(CASE WHEN validated_by_airtable = 1 THEN 1 ELSE 0 END) as validated
    FROM (SELECT DISTINCT name, validated_by_airtable FROM participants)
""")
total, validated = cursor.fetchone()

print("\n" + "="*80)
print("FINAL DATABASE STATE")
print("="*80)
print(f"Total participants: {total}")
print(f"Validated: {validated} ({100.0*validated/total:.1f}%)")
print(f"Unvalidated: {total - validated}")

conn.close()
