"""TSV input/output utilities for the legacy master list."""
from __future__ import annotations

import csv
import os
from typing import List, Dict

MASTER_TSV_FILE = "all_fathom_calls.tsv"
CANONICAL_HEADER = ['Title', 'Date', 'Duration', 'Hyperlink', 'shareStatus', 'sharedWith', 'shareTimestamp']


def read_master_tsv(path: str = MASTER_TSV_FILE) -> List[Dict[str, str]]:
    if not os.path.exists(path):
        return []
    with open(path, 'r', newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def write_master_tsv(records: List[Dict[str, str]], path: str = MASTER_TSV_FILE) -> None:
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CANONICAL_HEADER, delimiter='\t', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(records)
