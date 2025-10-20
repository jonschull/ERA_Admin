#!/bin/bash
# ERA Admin Airtable - Update All Data
# Runs all export scripts to get fresh data from Airtable

echo "🚀 ERA Admin Airtable Update"
echo "============================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    echo "✅ Virtual environment created and dependencies installed"
else
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
fi

echo ""
echo "📥 Step 1: Export complete People table..."
python export_people.py

echo ""
echo "🎯 Step 2: Export data optimized for Fathom matching..."
python export_for_fathom_matching.py

echo ""
echo "📊 Step 3: Generate summary statistics..."
if [ -f "airtable_summary.py" ]; then
    python airtable_summary.py
else
    echo "ℹ️  Summary script not yet created"
fi

echo ""
echo "🎉 Update completed!"
echo ""
echo "📁 Files updated:"
ls -la *.csv *.txt 2>/dev/null | head -10

echo ""
echo "💡 Next steps:"
echo "   - Review airtable_summary.txt for data health"
echo "   - Use people_for_matching.csv for cross-correlation"
echo "   - Run cross-correlation with Fathom data if needed"
