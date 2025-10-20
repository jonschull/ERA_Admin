#!/bin/bash
# Test harness to debug why run_all.sh stops after Step 3
# Isolates the Step 3 → Step 3.5 transition

set -e  # Exit on error (same as run_all.sh)

# Setup (mimicking run_all.sh environment)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PRIMARY_LOG="/tmp/test_primary.log"
CONSOLE_LOG="/tmp/test_console.log"
PYTHON="python3"

# Check if venv exists
if [ -d "../ERA_Admin_venv" ]; then
    PYTHON="../ERA_Admin_venv/bin/python3"
    echo "Using venv: $PYTHON"
else
    echo "Using system python3"
fi

echo "==================================="
echo "Test Harness: Step 3 → Step 3.5"
echo "==================================="
echo ""

# Simulate Step 3 completing successfully
echo "📧 SIMULATED STEP 3: EMAIL DOWNLOAD"
echo "✅ scripts/download_emails.py completed successfully. (0 new emails)"
echo ""

# Now try Step 3.5 exactly as run_all.sh does it
echo "🤖 STEP 3.5: ERA MEETING ANALYSIS"
echo "--- Running analysis/analyze_new_era_calls.py ---"

set +e
"$PYTHON" -u analysis/analyze_new_era_calls.py 2>&1 | tee -a "${PRIMARY_LOG}" >> "${CONSOLE_LOG}"
ANALYSIS_EXIT_CODE=${PIPESTATUS[0]}
set -e

echo ""
echo "DEBUG: Analysis exit code: $ANALYSIS_EXIT_CODE"

if [ $ANALYSIS_EXIT_CODE -ne 0 ]; then
    echo "⚠️  Warning: analysis/analyze_new_era_calls.py failed with exit code $ANALYSIS_EXIT_CODE."
    echo "   (Non-critical - continuing with daily report)"
else
    echo "✅ ERA meeting analysis completed successfully."
fi

echo ""
echo "==================================="
echo "✅ TEST HARNESS REACHED END"
echo "==================================="
echo ""
echo "If you see this message, Step 3.5 didn't cause an early exit."
echo ""

# Try Step 4 as well
echo "📧 STEP 4: SENDING DAILY REPORT"
echo "--- Running scripts/send_daily_report.py ---"

set +e
"$PYTHON" -u scripts/send_daily_report.py 2>&1 | tee -a "${PRIMARY_LOG}" >> "${CONSOLE_LOG}"
REPORT_EXIT_CODE=${PIPESTATUS[0]}
set -e

echo ""
echo "DEBUG: Report exit code: $REPORT_EXIT_CODE"

if [ $REPORT_EXIT_CODE -ne 0 ]; then
    echo "❌ Error: scripts/send_daily_report.py failed with exit code $REPORT_EXIT_CODE."
else
    echo "✅ Daily report sent successfully."
fi

echo ""
echo "==================================="
echo "✅ TEST COMPLETE - REACHED ABSOLUTE END"
echo "==================================="
