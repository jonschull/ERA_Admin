#!/bin/bash
# Test if double-tee piping causes script to hang

set -o pipefail

TEMP_OUTPUT="/tmp/test_output.log"
PRIMARY_LOG="/tmp/test_primary.log"
CONSOLE_LOG="/tmp/test_console.log"

echo "Starting test..."

# Simulate what Step 3 does
set +e
python3 -c "print('Script output line 1'); print('Script output line 2'); print('No new emails to download. Database is up to date.')" 2>&1 | tee "$TEMP_OUTPUT" | tee -a "${PRIMARY_LOG}" >> "${CONSOLE_LOG}"
DOWNLOAD_EXIT_CODE=${PIPESTATUS[0]}
set -e

echo "DEBUG: After pipe, exit code = $DOWNLOAD_EXIT_CODE"
echo "DEBUG: About to check exit code..."

if [ $DOWNLOAD_EXIT_CODE -ne 0 ]; then
    echo "ERROR: Non-zero exit"
    exit 1
fi

echo "DEBUG: Passed exit code check"

# Extract email count (same logic as run_all.sh lines 174-181)
# FIX: Add || true so grep doesn't trigger set -e when pattern not found
NEW_EMAILS=$(grep "Downloading.*new emails" "$TEMP_OUTPUT" 2>/dev/null | sed 's/.*Downloading \([0-9]*\) new emails.*/\1/' || true)
if [ -n "$NEW_EMAILS" ]; then
    echo "✅ Found $NEW_EMAILS new emails"
elif grep -q "No new emails to download" "$TEMP_OUTPUT" 2>/dev/null; then
    echo "✅ Completed successfully. (0 new emails)"
else
    echo "✅ Completed successfully."
fi

echo "DEBUG: Cleaning up temp file"
rm -f "$TEMP_OUTPUT"

echo ""
echo "======================================="
echo "✅ TEST COMPLETED - REACHED END"
echo "======================================="
