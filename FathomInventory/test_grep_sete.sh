#!/bin/bash
# Test if grep failure with set -e causes exit

echo "=== Test 1: grep with set -e ==="
set -e
TEMP_FILE="/tmp/test_grep.txt"
echo "No new emails to download. Database is up to date." > "$TEMP_FILE"

echo "About to run grep that will fail..."
NEW_EMAILS=$(grep "Downloading.*new emails" "$TEMP_FILE" 2>/dev/null | sed 's/.*Downloading \([0-9]*\) new emails.*/\1/')
echo "After first grep (this won't print if set -e killed us)"

if [ -n "$NEW_EMAILS" ]; then
    echo "Found: $NEW_EMAILS"
elif grep -q "No new emails" "$TEMP_FILE" 2>/dev/null; then
    echo "No new emails case"
else
    echo "Other case"
fi

echo "REACHED END (this proves set -e didn't kill us)"
rm -f "$TEMP_FILE"
