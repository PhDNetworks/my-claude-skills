#!/bin/bash
#
# Google Ads Daily Monitor Runner
# PhD Networks & Systems Ltd
#
# This script runs the scheduled monitor and alert system.
# Called by launchd daily at 8am.
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/../logs"
OUTPUT_DIR="${SCRIPT_DIR}/../data"

# Create directories if they don't exist
mkdir -p "$LOG_DIR"
mkdir -p "$OUTPUT_DIR"

# Log start time
echo "======================================" >> "$LOG_DIR/daily_run.log"
echo "Daily Monitor Run: $(date)" >> "$LOG_DIR/daily_run.log"
echo "======================================" >> "$LOG_DIR/daily_run.log"

# Change to script directory
cd "$SCRIPT_DIR"

# Run the scheduled monitor
echo "Running scheduled monitor..." >> "$LOG_DIR/daily_run.log"
python3 scheduled_monitor.py --output-dir "$OUTPUT_DIR" >> "$LOG_DIR/daily_run.log" 2>&1

# Check if monitoring succeeded
if [ $? -eq 0 ]; then
    echo "Monitor completed successfully" >> "$LOG_DIR/daily_run.log"

    # Run alert system (email only by default, add --webhook-url if configured)
    echo "Running alert system..." >> "$LOG_DIR/daily_run.log"
    python3 alert_system.py \
        --output-dir "$OUTPUT_DIR" \
        --email "daniel.doherty@phdnetworks.co.uk" \
        >> "$LOG_DIR/daily_run.log" 2>&1

    # Uncomment below to add Make.com webhook
    # python3 alert_system.py \
    #     --output-dir "$OUTPUT_DIR" \
    #     --email "daniel.doherty@phdnetworks.co.uk" \
    #     --webhook-url "https://hook.eu2.make.com/YOUR_WEBHOOK_ID" \
    #     >> "$LOG_DIR/daily_run.log" 2>&1
else
    echo "Monitor failed!" >> "$LOG_DIR/daily_run.log"
fi

echo "Run completed at: $(date)" >> "$LOG_DIR/daily_run.log"
echo "" >> "$LOG_DIR/daily_run.log"
