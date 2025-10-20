#!/bin/bash
# Database backup script - run before any modification operations
# Creates timestamped SQLite backup + compressed CSV exports

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FATHOM_DIR="$(dirname "$SCRIPT_DIR")"
DB_FILE="$FATHOM_DIR/fathom_emails.db"
BACKUP_DIR="$FATHOM_DIR/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M)

# Create backup directory if needed
mkdir -p "$BACKUP_DIR"

echo "🔒 Creating database backup..."

# 1. SQLite database backup (full copy)
BACKUP_DB="$BACKUP_DIR/fathom_emails.backup_$TIMESTAMP.db"
cp "$DB_FILE" "$BACKUP_DB"
echo "✅ Database copied: $BACKUP_DB"

# 2. Export tables to CSV and compress
TEMP_DIR=$(mktemp -d)
CSV_ARCHIVE="$BACKUP_DIR/fathom_tables_$TIMESTAMP.zip"

echo "📊 Exporting tables to CSV..."

# Export participants
sqlite3 "$DB_FILE" -header -csv \
  "SELECT * FROM participants;" > "$TEMP_DIR/participants.csv"
echo "  - participants: $(wc -l < "$TEMP_DIR/participants.csv") rows"

# Export calls
sqlite3 "$DB_FILE" -header -csv \
  "SELECT * FROM calls;" > "$TEMP_DIR/calls.csv"
echo "  - calls: $(wc -l < "$TEMP_DIR/calls.csv") rows"

# Export emails
sqlite3 "$DB_FILE" -header -csv \
  "SELECT * FROM emails;" > "$TEMP_DIR/emails.csv"
echo "  - emails: $(wc -l < "$TEMP_DIR/emails.csv") rows"

# Compress CSVs
cd "$TEMP_DIR"
zip -q "$CSV_ARCHIVE" *.csv
cd - > /dev/null
rm -rf "$TEMP_DIR"

echo "✅ CSV archive created: $CSV_ARCHIVE"
echo ""

# Show sizes
DB_SIZE=$(du -h "$BACKUP_DB" | cut -f1)
CSV_SIZE=$(du -h "$CSV_ARCHIVE" | cut -f1)
echo "📦 Backup sizes: DB=$DB_SIZE, CSV=$CSV_SIZE"

# Integrity check
echo "🔍 Checking database integrity..."
if sqlite3 "$DB_FILE" "PRAGMA integrity_check;" | grep -q "ok"; then
    echo "✅ Database integrity OK"
else
    echo "❌ WARNING: Database integrity check failed!"
    exit 1
fi

echo ""
echo "✅ Backup complete: $TIMESTAMP"
echo "   Database: $BACKUP_DB"
echo "   CSVs: $CSV_ARCHIVE"
echo ""
echo "💡 To restore database:"
echo "   cp $BACKUP_DB fathom_emails.db"
echo ""

# Optional: Upload to Google Drive
if [ "$UPLOAD_TO_DRIVE" = "true" ]; then
    echo "☁️  Uploading to Google Drive..."
    "$SCRIPT_DIR/upload_backup_to_drive.py"
    if [ $? -eq 0 ]; then
        echo "✅ Backup uploaded to Google Drive"
    else
        echo "⚠️  Drive upload failed (backup still saved locally)"
    fi
fi
