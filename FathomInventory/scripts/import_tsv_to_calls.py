#!/usr/bin/env python3
"""
Import records from all_fathom_calls.tsv into the standalone `calls` table.

Idempotent: uses INSERT OR REPLACE on primary key (hyperlink).
Safe: does not modify other tables.

Usage:
  python scripts/import_tsv_to_calls.py --db fathom_emails.db --tsv all_fathom_calls.tsv
"""
from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path

DEFAULT_TSV = "all_fathom_calls.tsv"
DEFAULT_DB = "fathom_emails.db"


def ensure_calls_table(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS calls (
            hyperlink TEXT PRIMARY KEY,
            title TEXT,
            date TEXT,
            duration TEXT,
            share_status TEXT DEFAULT '',
            shared_with TEXT,
            share_timestamp TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_calls_created_at ON calls(created_at);
        """
    )


def import_tsv(conn: sqlite3.Connection, tsv_path: Path) -> int:
    if not tsv_path.exists():
        print(f"TSV not found: {tsv_path}")
        return 0

    with tsv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)

    cur = conn.cursor()
    inserted = 0
    for r in rows:
        hyperlink = (r.get("Hyperlink") or "").strip()
        if not hyperlink:
            continue
        cur.execute(
            """
            INSERT OR REPLACE INTO calls (hyperlink, title, date, duration, share_status, shared_with, share_timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                hyperlink,
                (r.get("Title") or "").strip(),
                (r.get("Date") or "").strip(),
                (r.get("Duration") or "").strip(),
                (r.get("shareStatus") or "").strip(),
                (r.get("sharedWith") or "").strip(),
                (r.get("shareTimestamp") or "").strip(),
            ),
        )
        inserted += 1
    conn.commit()
    return inserted


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DEFAULT_DB, help="Path to SQLite DB (will be created if missing)")
    ap.add_argument("--tsv", default=DEFAULT_TSV, help="Path to TSV file to import")
    args = ap.parse_args()

    db_path = Path(args.db)
    tsv_path = Path(args.tsv)

    conn = sqlite3.connect(db_path)
    try:
        ensure_calls_table(conn)
        n = import_tsv(conn, tsv_path)
        print(f"Imported {n} rows from {tsv_path} into calls table in {db_path}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
