#!/bin/bash

# Generate batch data
echo "Generating batch data..."
python3 generate_batch_data.py

# Generate HTML table and capture output
echo "Generating HTML table..."
OUTPUT=$(python3 generate_phase4b2_table.py 2>&1)
echo "$OUTPUT"

# Extract filename from output
FILENAME=$(echo "$OUTPUT" | grep "📁 Filename:" | sed 's/.*📁 Filename: //')

if [ -n "$FILENAME" ]; then
    echo ""
    echo "Opening: $FILENAME"
    open "$FILENAME"
else
    echo "⚠️ Could not find filename in output"
    # Fallback: open the actual latest file
    LATEST=$(ls -t phase4b2_TEST_APPROVALS_*.html 2>/dev/null | head -1)
    if [ -n "$LATEST" ]; then
        echo "Opening fallback: $LATEST"
        open "$LATEST"
    fi
fi
