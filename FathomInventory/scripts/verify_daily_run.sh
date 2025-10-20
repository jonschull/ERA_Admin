#!/bin/bash

LOG_FILE="$HOME/Library/Logs/fathom_daily_check.log"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TODAY=$(date +%Y-%m-%d)

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if the script ran today
check_todays_run() {
    if grep -q "$(date '+%b %_d')" "$SCRIPT_DIR/cron.log"; then
        log "Fathom inventory script has already run today."
        return 0
    else
        log "Fathom inventory script has NOT run today. Last run was:"
        grep "^===" "$SCRIPT_DIR/cron.log" | tail -n 1 | tee -a "$LOG_FILE"
        return 1
    fi
}

# Run the main script if it hasn't run today
run_if_needed() {
    if ! check_todays_run; then
        log "Attempting to run Fathom inventory script..."
        if [ -f "$SCRIPT_DIR/run_all.sh" ]; then
            cd "$SCRIPT_DIR"
            ./run_all.sh
            if [ $? -eq 0 ]; then
                log "Fathom inventory script completed successfully."
            else
                log "ERROR: Fathom inventory script failed with status $?"
                # Send notification (uncomment and configure if you want email notifications)
                # echo "Fathom inventory script failed. Check $LOG_FILE for details." | mail -s "Fathom Script Failure" your-email@example.com
                return 1
            fi
        else
            log "ERROR: run_all.sh not found in $SCRIPT_DIR"
            return 1
        fi
    fi
}

# Main execution
log "=== Starting Fathom Daily Check ==="
run_if_needed
log "=== Fathom Daily Check Complete ==="

exit 0
