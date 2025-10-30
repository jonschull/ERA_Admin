#!/bin/bash
# Guided workflow to refresh Zeffy authentication cookies
# ADAPTED FROM: /Users/admin/ERA_Admin/Other_Data_Sources/REFERENCE_refresh_auth.sh
# PATTERN: Browser Cookie Authentication Pattern

echo "=========================================="
echo "Zeffy Cookie Refresh Workflow"
echo "=========================================="
echo ""
echo "This script will guide you through refreshing your Zeffy authentication."
echo ""

# Step 1: Backup existing cookies
if [ -f "zeffy_cookies.json" ]; then
    echo "📦 Backing up existing cookies..."
    mkdir -p backups
    timestamp=$(date +%Y%m%d_%H%M%S)
    cp zeffy_cookies.json "backups/zeffy_cookies_${timestamp}.json"
    echo "✅ Backup saved to backups/zeffy_cookies_${timestamp}.json"
    echo ""
fi

# Step 2: Instructions for cookie export
echo "📋 STEP 1: Export cookies using Cookie-Editor extension"
echo "-------------------------------------------"
echo "PREFERRED METHOD (Easiest):"
echo "1. Install 'Cookie-Editor' extension in Edge if not already installed"
echo "2. Navigate to: https://www.zeffy.com"
echo "3. Log in with your account (jschull@gmail.com)"
echo "4. Switch profile to 'ERA Inc.' if needed"
echo "5. Click the Cookie-Editor extension icon"
echo "6. Click 'Export' button (bottom right)"
echo "7. Copy the JSON output"
echo "8. Paste into zeffy_cookies.json file"
echo ""
echo "ALTERNATIVE METHOD (Edge DevTools):"
echo "1. Press F12 → Application → Cookies → https://www.zeffy.com"
echo "2. Ctrl+A, Ctrl+C to copy all cookies"
echo "3. Run: python3 convert_edge_cookies.py"
echo ""
read -p "Press Enter when you have pasted cookies into zeffy_cookies.json..."
echo ""

# Step 3: Sanitize cookies
if [ -f "zeffy_cookies.json" ]; then
    echo "🧹 STEP 2: Sanitize cookies for Playwright"
    echo "-------------------------------------------"
    python3 sanitize_cookies.py
    echo ""
    
    echo "✅ Cookie refresh complete!"
    echo ""
    echo "Next steps:"
    echo "1. Test authentication with your download script"
    echo "2. If it works, you're done!"
    echo "3. If not, check the troubleshooting section in README.md"
else
    echo "❌ zeffy_cookies.json not found"
    echo "   Please create the file and paste cookie-editor JSON into it"
    exit 1
fi
