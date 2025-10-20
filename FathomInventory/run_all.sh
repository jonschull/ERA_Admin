#!/bin/bash
# Main automation script - runs daily at 3 AM via launchd
# 🔧 Modifying this? Read DEVELOPMENT.md first (testing requirements, known issues)

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# Enable pipefail to catch errors in piped commands
set -o pipefail

# Define the log file paths
# Now that we're out of Dropbox, logs can stay in project
LOG_DIR="${SCRIPT_DIR}/logs"
PRIMARY_LOG="${LOG_DIR}/fathom_cron.log"
CONSOLE_LOG="${SCRIPT_DIR}/cron.log"  # Still keep one in root for quick access

# Ensure log directory exists
mkdir -p "${LOG_DIR}"

# Function to output to both console and log files
log_and_echo() {
    echo "$1" | tee -a "${PRIMARY_LOG}"
    # Also write to console log in root for quick access
    echo "$1" >> "${CONSOLE_LOG}" 2>/dev/null || true
}

# Function to wait for Dropbox path to be available (handles transient sync issues)
wait_for_path() {
    local path="$1"
    local max_attempts=5
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if [ -e "$path" ]; then
            return 0
        fi
        log_and_echo "⏳ Waiting for path to be available (attempt $attempt/$max_attempts): $path"
        sleep 10
        attempt=$((attempt + 1))
    done
    
    log_and_echo "❌ Path not available after $max_attempts attempts: $path"
    return 1
}

# Clear/create log files for this run
echo "==================================================" > "${PRIMARY_LOG}"
echo "Starting Fathom Inventory run at $(date)" >> "${PRIMARY_LOG}"
echo "==================================================" >> "${PRIMARY_LOG}"

# Console announcement
echo "🚀 FATHOM INVENTORY SYSTEM STARTING"
echo "📅 $(date)"
echo "📝 Primary log: ${PRIMARY_LOG}"
echo "📝 Console log: ${CONSOLE_LOG}"
echo ""

log_and_echo "=================================================="
log_and_echo "Starting Fathom Inventory run at $(date)"
log_and_echo "=================================================="

# Wait for script directory to be available (handles Dropbox sync delays)
if ! wait_for_path "$SCRIPT_DIR"; then
    log_and_echo "❌ Error: Script directory not accessible (Dropbox sync issue?)"
    exit 78  # EX_CONFIG - configuration error
fi

# Activate the virtual environment
# Note: venv kept outside Dropbox to avoid file locking issues
VENV_PATH="/Users/admin/ERA_Admin_venv/bin/activate"

# Wait for venv to be available
if ! wait_for_path "$VENV_PATH"; then
    log_and_echo "❌ Error: Virtual environment not found at $VENV_PATH"
    exit 78  # EX_CONFIG - configuration error
fi

log_and_echo "🐍 Activating virtual environment..."
source "$VENV_PATH"

# Set Python to use venv's python directly (external location)
PYTHON="/Users/admin/ERA_Admin_venv/bin/python3"

# Change to the script's directory to ensure relative paths in Python scripts work
cd "$SCRIPT_DIR"

# --- Step 1: Run the daily share script ---
echo ""
echo "📋 STEP 1: FATHOM CALL SHARING"
log_and_echo "--- Running run_daily_share.py (DATABASE MODE) ---"

# Run and capture output to temp file while streaming
set +e  # Temporarily disable exit on error
TEMP_OUTPUT="/tmp/fathom_share_$$.log"
"$PYTHON" -u run_daily_share.py --use-db 2>&1 | tee "$TEMP_OUTPUT" | tee -a "${PRIMARY_LOG}" >> "${CONSOLE_LOG}"
SHARE_EXIT_CODE=${PIPESTATUS[0]}  # Get Python's exit code, not tee's
set -e  # Re-enable exit on error

if [ $SHARE_EXIT_CODE -ne 0 ]; then
    log_and_echo "❌ Error: run_daily_share.py failed with exit code $SHARE_EXIT_CODE."
    log_and_echo "   This usually indicates authentication failure or network issues."
    log_and_echo "   Check logs above for timeout or authentication errors."
    log_and_echo "Run finished with errors at $(date)"
    rm -f "$TEMP_OUTPUT"
    exit 1
fi

# Extract new calls count from output
NEW_CALLS=$(grep "New calls added this run:" "$TEMP_OUTPUT" 2>/dev/null | sed 's/.*New calls added this run: //')
if [ -n "$NEW_CALLS" ]; then
    log_and_echo "✅ run_daily_share.py completed successfully. ($NEW_CALLS new calls)"
else
    log_and_echo "✅ run_daily_share.py completed successfully."
fi
rm -f "$TEMP_OUTPUT"

# --- Step 2: Wait for a few minutes ---
WAIT_SECONDS=300  # 5 minutes
TIMEOUT_SECONDS=600  # 10 minutes max for the entire script
START_TIME=$(date +%s)

echo ""
echo "⏱️  STEP 2: WAITING FOR EMAIL PROCESSING"
echo "⏳ Starting ${WAIT_SECONDS}-second wait to allow emails to be sent and received..."
log_and_echo "--- Waiting for ${WAIT_SECONDS} seconds for emails to be processed ---"

# Function to check if we've exceeded the maximum allowed time
check_timeout() {
    local current_time=$(date +%s)
    local elapsed_seconds=$((current_time - START_TIME))
    
    if [ $elapsed_seconds -gt $TIMEOUT_SECONDS ]; then
        log_and_echo "❌ Error: Script exceeded maximum runtime of ${TIMEOUT_SECONDS} seconds"
        exit 124  # Exit with timeout status code
    fi
}

# Show countdown with timeout checks
for ((i=WAIT_SECONDS; i>0; i-=10)); do
    check_timeout
    
    # Log progress every 30 seconds or less if we're near the end
    if [ $((i % 30)) -eq 0 ] || [ $i -le 30 ]; then
        minutes=$((i / 60))
        seconds=$((i % 60))
        status="⏳ ${i}s remaining (${minutes}m ${seconds}s)"
        log_and_echo "$status"
        echo "$status"
    fi
    
    # Sleep in smaller chunks to be more responsive to timeouts
    sleep 10
done

# --- Step 3: Run the email download script ---
echo ""
echo "📧 STEP 3: EMAIL DOWNLOAD AND PROCESSING"
log_and_echo "--- Running scripts/download_emails.py ---"

set +e
TEMP_OUTPUT="/tmp/fathom_download_$$.log"
"$PYTHON" -u scripts/download_emails.py 2>&1 | tee "$TEMP_OUTPUT" | tee -a "${PRIMARY_LOG}" >> "${CONSOLE_LOG}"
DOWNLOAD_EXIT_CODE=${PIPESTATUS[0]}
set -e

if [ $DOWNLOAD_EXIT_CODE -ne 0 ]; then
    log_and_echo "❌ Error: scripts/download_emails.py failed with exit code $DOWNLOAD_EXIT_CODE."
    log_and_echo "Run finished with errors at $(date)"
    rm -f "$TEMP_OUTPUT"
    exit 1
fi

# Extract email count from output
NEW_EMAILS=$(grep "Downloading.*new emails" "$TEMP_OUTPUT" 2>/dev/null | sed 's/.*Downloading \([0-9]*\) new emails.*/\1/' || true)
if [ -n "$NEW_EMAILS" ]; then
    log_and_echo "✅ scripts/download_emails.py completed successfully. ($NEW_EMAILS new emails)"
elif grep -q "No new emails to download" "$TEMP_OUTPUT" 2>/dev/null; then
    log_and_echo "✅ scripts/download_emails.py completed successfully. (0 new emails)"
else
    log_and_echo "✅ scripts/download_emails.py completed successfully."
fi
rm -f "$TEMP_OUTPUT"

# --- Step 3.5: Analyze new ERA meetings ---
echo ""
echo "🤖 STEP 3.5: ERA MEETING ANALYSIS"
log_and_echo "--- Running analysis/analyze_new_era_calls.py ---"

set +e
"$PYTHON" -u analysis/analyze_new_era_calls.py 2>&1 | tee -a "${PRIMARY_LOG}" >> "${CONSOLE_LOG}"
ANALYSIS_EXIT_CODE=${PIPESTATUS[0]}
set -e

if [ $ANALYSIS_EXIT_CODE -ne 0 ]; then
    log_and_echo "⚠️  Warning: analysis/analyze_new_era_calls.py failed with exit code $ANALYSIS_EXIT_CODE."
    log_and_echo "   (Non-critical - continuing with daily report)"
else
    log_and_echo "✅ ERA meeting analysis completed successfully."
fi

# --- Step 4: Send daily report email ---
echo ""
echo "📧 STEP 4: SENDING DAILY REPORT"
log_and_echo "--- Running scripts/send_daily_report.py ---"

set +e
"$PYTHON" -u scripts/send_daily_report.py 2>&1 | tee -a "${PRIMARY_LOG}" >> "${CONSOLE_LOG}"
REPORT_EXIT_CODE=${PIPESTATUS[0]}
set -e

if [ $REPORT_EXIT_CODE -ne 0 ]; then
    log_and_echo "⚠️  Warning: scripts/send_daily_report.py failed with exit code $REPORT_EXIT_CODE."
    log_and_echo "   (Non-critical - run completed successfully)"
else
    log_and_echo "✅ Daily report sent successfully."
fi

echo ""
echo "🎉 SUCCESS: FATHOM INVENTORY RUN COMPLETED"
log_and_echo "=================================================="
log_and_echo "Fathom Inventory run finished successfully at $(date)"
log_and_echo "=================================================="

exit 0
