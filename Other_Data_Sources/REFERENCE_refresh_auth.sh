#!/bin/bash
#
# REFERENCE MODEL - DO NOT EDIT
#
# Fathom Authentication Refresh Script
# Streamlines the cookie refresh process
#
# SOURCE: /Users/admin/ERA_Admin/FathomInventory/scripts/refresh_fathom_auth.sh
# PROVEN: Production use in FathomInventory since October 2025
# STATUS: Stable reference implementation
#
# TO USE:
# 1. Copy this file to your project
# 2. Adapt paths, URLs, and service names
# 3. Keep workflow structure intact
#
# USAGE:
#     ./refresh_auth.sh
#
# PURPOSE:
# Provides guided workflow for refreshing browser cookies:
# - Backs up existing cookies
# - Guides user through export process
# - Converts cookies to JSON
# - Tests authentication
# - Confirms success or rollback

echo "🔄 FATHOM AUTHENTICATION REFRESH"
echo "=================================="

# Get script directory and change to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Set up virtual environment Python
PYTHON="/Users/admin/ERA_Admin_venv/bin/python3"
if [ ! -f "$PYTHON" ]; then
    echo "❌ Error: Virtual environment Python not found at $PYTHON"
    echo "   Falling back to system Python"
    PYTHON="python3"
fi

# Backup existing cookies
if [ -f "fathom_cookies.json" ]; then
    echo "📦 Backing up existing cookies..."
    mkdir -p backups/cookies
    cp fathom_cookies.json "backups/cookies/fathom_cookies.json.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✅ Backup created in backups/cookies/"
fi

echo ""
echo "📋 INSTRUCTIONS:"
echo "1. Open Microsoft Edge"
echo "2. Go to https://fathom.video/home (log in if needed)"
echo "3. Press F12 → Application tab → Cookies → https://fathom.video"
echo "4. Select all cookies (Ctrl+A) and copy (Ctrl+C)"
echo "5. Come back here and paste when prompted"
echo ""

# Run the converter
"$PYTHON" scripts/convert_edge_cookies.py

# Test the new cookies
if [ -f "fathom_cookies.json" ]; then
    echo ""
    echo "🧪 Testing new cookies..."
    cd authentication
    "$PYTHON" test_fathom_cookies.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 Cookie refresh completed successfully!"
        echo "✅ Ready to run ./run_all.sh"
        
        # Set calendar reminder for next week
        echo ""
        echo "📅 REMINDER: Set a calendar reminder to refresh cookies again in 7 days"
        echo "   (Some cookies expire daily, weekly refresh recommended)"
    else
        echo ""
        echo "❌ Cookie test failed. Check the authentication and try again."
        echo "   Your backup is available if needed."
    fi
else
    echo ""
    echo "❌ Cookie conversion failed. Your original cookies are unchanged."
fi
