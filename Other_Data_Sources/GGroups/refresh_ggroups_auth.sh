#!/bin/bash
#
# Google Groups Authentication Refresh Script
# Adapted from: /Other_Data_Sources/REFERENCE_refresh_auth.sh
#
# Usage: ./refresh_ggroups_auth.sh

echo "🔄 GOOGLE GROUPS AUTHENTICATION REFRESH"
echo "=========================================="

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
cd "$SCRIPT_DIR"

# Set up Python (try venv first, fall back to system)
PYTHON="/Users/admin/ERA_Admin_venv/bin/python3"
if [ ! -f "$PYTHON" ]; then
    echo "⚠️  Virtual environment Python not found, using system Python"
    PYTHON="python3"
fi

# Backup existing cookies
if [ -f "ggroups_cookies.json" ]; then
    echo "📦 Backing up existing cookies..."
    mkdir -p backups
    cp ggroups_cookies.json "backups/ggroups_cookies.json.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✅ Backup created in backups/"
fi

echo ""
echo "📋 INSTRUCTIONS:"
echo "1. Open Microsoft Edge"
echo "2. Go to https://groups.google.com"
echo "3. Make sure you're logged in to the correct Google account"
echo "4. Press F12 → Application tab → Cookies → https://groups.google.com"
echo "5. Select all cookies (Ctrl+A) and copy (Ctrl+C)"
echo "6. Come back here and paste when prompted"
echo ""

# Run the converter
"$PYTHON" convert_edge_cookies.py

# Test if successful
if [ -f "ggroups_cookies.json" ]; then
    echo ""
    echo "✅ Cookies exported successfully!"
    echo ""
    echo "Next step:"
    echo "  python download_members.py"
else
    echo ""
    echo "❌ Cookie export failed. Please try again."
fi
