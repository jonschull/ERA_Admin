#!/bin/bash
# Helper script to regenerate production docs from wireframe
# Usage: ./docs/update_docs.sh

set -e  # Exit on any error

echo "============================================================"
echo "Documentation Regeneration from Wireframe"
echo "============================================================"
echo ""

# Ensure we're in the right place
if [ ! -f "docs/NAVIGATION_WIREFRAME.md" ]; then
    echo "❌ Error: Must run from ERA_Admin root directory"
    echo "   (Can't find docs/NAVIGATION_WIREFRAME.md)"
    exit 1
fi

# Clean old generation
echo "📁 Cleaning old generated docs..."
if [ -d "docs_generated" ]; then
    rm -rf docs_generated
    echo "   ✅ Removed docs_generated/"
else
    echo "   ℹ️  No docs_generated/ to clean"
fi

# Regenerate
echo ""
echo "🔄 Regenerating from NAVIGATION_WIREFRAME.md..."
cd docs
python3 generate_from_wireframe.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Generation failed! Check errors above."
    exit 1
fi

cd ..

# Test navigation integrity
echo ""
echo "🧪 Testing navigation integrity..."
python3 docs/test_navigation.py docs_generated

NAV_TEST_EXIT=$?

if [ $NAV_TEST_EXIT -ne 0 ]; then
    echo ""
    echo "⚠️  Navigation integrity issues detected!"
    echo "   Set SKIP_NAV_TEST=1 to bypass (not recommended)"
    
    if [ "${SKIP_NAV_TEST}" != "1" ]; then
        echo ""
        echo "❌ Fix navigation issues before deploying."
        echo "   Or run: SKIP_NAV_TEST=1 ./docs/update_docs.sh"
        exit 1
    else
        echo "   ⚠️  Skipping navigation test (SKIP_NAV_TEST=1)"
    fi
fi

# Copy to production
echo ""
echo "📋 Copying to production locations..."
cp -r docs_generated/* .

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Copy failed!"
    exit 1
fi

echo ""
echo "============================================================"
echo "✅ Documentation regenerated successfully!"
echo "============================================================"
echo ""
echo "📊 Review changes with:"
echo "   git status"
echo "   git diff"
echo "   git diff --stat"
echo ""
echo "📝 If satisfied, commit:"
echo "   git add -A"
echo "   git commit -m 'Update documentation from wireframe'"
echo ""
echo "⚠️  Remember: This is incremental workflow for normal edits."
echo "   For major overhauls, use: python3 docs/archive_and_replace.py"
echo ""
