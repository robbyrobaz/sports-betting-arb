#!/bin/bash

# Setup automated daily pipeline via cron

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRAPER="$REPO_DIR/scripts/scraper.py"
DETECTOR="$REPO_DIR/scripts/detector.py"
REPORT="$REPO_DIR/scripts/report.py"
LOG_FILE="$REPO_DIR/logs/pipeline.log"

echo "🔧 Setting up automated pipeline..."
echo ""

# Create log directory
mkdir -p "$REPO_DIR/logs"
mkdir -p "$REPO_DIR/reports"

# Create cron job
CRON_JOB="0 8,14,20 * * * cd $REPO_DIR && python3 $SCRAPER >> $LOG_FILE 2>&1 && python3 $DETECTOR >> $LOG_FILE 2>&1 && python3 $REPORT >> $LOG_FILE 2>&1"

# Check if already installed
if crontab -l 2>/dev/null | grep -q "sports-betting-arb"; then
    echo "✓ Cron job already installed"
else
    echo "Adding new cron job..."
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✓ Cron job installed"
fi

echo ""
echo "📋 Cron Schedule:"
echo "   08:00 - Morning scan"
echo "   14:00 - Afternoon scan"
echo "   20:00 - Evening scan"
echo ""

echo "📂 Locations:"
echo "   Scripts: $REPO_DIR/scripts/"
echo "   Reports: $REPO_DIR/reports/"
echo "   Logs: $LOG_FILE"
echo ""

echo "📊 View your opportunities:"
echo "   cat $REPO_DIR/reports/daily_report_*.json | jq '.summary'"
echo ""

echo "✅ Setup complete!"
