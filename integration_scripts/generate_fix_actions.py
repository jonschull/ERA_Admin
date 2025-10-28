#!/usr/bin/env python3
"""
Generate CSV files with fix actions (Airtable API lacks update permissions).

PRINCIPLE: ERA Member = Attended Town Hall

Generates:
1. spelling_fixes.csv - Name corrections
2. remove_era_member_flags.csv - Remove ERA member from non-attendees
3. delete_duplicates.csv - Duplicate records to delete
4. jon_should_unpublish.csv - Published non-members
