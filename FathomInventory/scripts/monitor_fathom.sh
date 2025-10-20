#!/bin/bash

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/cron.log"
MONITOR_LOG="$SCRIPT_DIR/monitor.log"
MAX_RUNTIME=1200  # 20 minutes in seconds

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$MONITOR_LOG"
}

# Check if the script is already running
is_running() {
    if pgrep -f "$SCRIPT_DIR/run_all.sh" > /dev/null; then
        # Get the start time of the process
        PID=$(pgrep -f "$SCRIPT_DIR/run_all.sh")
        START_TIME=$(ps -o lstart= -p $PID 2>/dev/null | xargs -I {} date -j -f "%a %b %d %H:%M:%S %Y" "{}" +%s 2>/dev/null)
        if [ -n "$START_TIME" ]; then
            CURRENT_TIME=$(date +%s)
            RUNTIME=$((CURRENT_TIME - START_TIME))
            
            if [ $RUNTIME -gt $MAX_RUNTIME ]; then
                log "⚠️  Fathom script has been running for $((RUNTIME/60)) minutes (PID: $PID), which exceeds the maximum allowed runtime of $((MAX_RUNTIME/60)) minutes"
                # Kill the stuck process
                kill -9 $PID
                log "Terminated stuck process (PID: $PID)"
                return 1
            else
                log "Fathom script is already running (PID: $PID, running for $((RUNTIME/60))m $((RUNTIME%60))s)"
                return 0
            fi
        fi
    fi
    return 1
}

# Check if the script ran today
ran_today() {
    if [ -f "$LOG_FILE" ]; then
        if grep -q "$(date '+%b %_d')" "$LOG_FILE"; then
            log "Fathom script has already run today"
            return 0
        fi
    fi
    return 1
}

# Main monitoring function
monitor() {
    log "=== Starting Fathom Monitor ==="
    
    # Check if already running
    if is_running; then
        log "Fathom script is already running, nothing to do"
        return 0
    fi
    
    # Check if already ran today
    if ran_today; then
        log "Fathom script already ran today, nothing to do"
        return 0
    fi
    
    # If we get here, we need to run the script
    log "Starting Fathom script..."
    nohup "$SCRIPT_DIR/run_all.sh" >> "$SCRIPT_DIR/cron.log" 2>&1 &
    log "Started Fathom script with PID $!"
    
    # Wait a bit and check if it's still running
    sleep 10
    if ! pgrep -f "$SCRIPT_DIR/run_all.sh" > /dev/null; then
        log "❌ Error: Fathom script failed to start or crashed immediately"
        return 1
    fi
    
    log "Fathom script started successfully"
    return 0
}

# Run the monitor
monitor

# Log completion
log "=== Fathom Monitor Completed ===\n"

exit 0
