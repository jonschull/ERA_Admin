#!/bin/bash
# Rollback script - restore documentation from archive
# Created: 2025-10-20 22:19:27
# Archive: historical/docs_archive_20251020_221927

set -e

echo "🔄 Rolling back documentation to archive from 20251020_221927"
echo ""


if [ -f "historical/docs_archive_20251020_221927/README.md" ]; then
    cp -v "historical/docs_archive_20251020_221927/README.md" "README.md"
    echo "✅ Restored: README.md"
else
    echo "⚠️  Archive missing: README.md"
fi

if [ -f "historical/docs_archive_20251020_221927/CONTEXT_RECOVERY.md" ]; then
    cp -v "historical/docs_archive_20251020_221927/CONTEXT_RECOVERY.md" "CONTEXT_RECOVERY.md"
    echo "✅ Restored: CONTEXT_RECOVERY.md"
else
    echo "⚠️  Archive missing: CONTEXT_RECOVERY.md"
fi

if [ -f "historical/docs_archive_20251020_221927/AI_HANDOFF_GUIDE.md" ]; then
    cp -v "historical/docs_archive_20251020_221927/AI_HANDOFF_GUIDE.md" "AI_HANDOFF_GUIDE.md"
    echo "✅ Restored: AI_HANDOFF_GUIDE.md"
else
    echo "⚠️  Archive missing: AI_HANDOFF_GUIDE.md"
fi

if [ -f "historical/docs_archive_20251020_221927/WORKING_PRINCIPLES.md" ]; then
    cp -v "historical/docs_archive_20251020_221927/WORKING_PRINCIPLES.md" "WORKING_PRINCIPLES.md"
    echo "✅ Restored: WORKING_PRINCIPLES.md"
else
    echo "⚠️  Archive missing: WORKING_PRINCIPLES.md"
fi

if [ -f "historical/docs_archive_20251020_221927/FathomInventory/README.md" ]; then
    cp -v "historical/docs_archive_20251020_221927/FathomInventory/README.md" "FathomInventory/README.md"
    echo "✅ Restored: FathomInventory/README.md"
else
    echo "⚠️  Archive missing: FathomInventory/README.md"
fi

if [ -f "historical/docs_archive_20251020_221927/FathomInventory/CONTEXT_RECOVERY.md" ]; then
    cp -v "historical/docs_archive_20251020_221927/FathomInventory/CONTEXT_RECOVERY.md" "FathomInventory/CONTEXT_RECOVERY.md"
    echo "✅ Restored: FathomInventory/CONTEXT_RECOVERY.md"
else
    echo "⚠️  Archive missing: FathomInventory/CONTEXT_RECOVERY.md"
fi

if [ -f "historical/docs_archive_20251020_221927/FathomInventory/authentication/README.md" ]; then
    cp -v "historical/docs_archive_20251020_221927/FathomInventory/authentication/README.md" "FathomInventory/authentication/README.md"
    echo "✅ Restored: FathomInventory/authentication/README.md"
else
    echo "⚠️  Archive missing: FathomInventory/authentication/README.md"
fi

if [ -f "historical/docs_archive_20251020_221927/airtable/README.md" ]; then
    cp -v "historical/docs_archive_20251020_221927/airtable/README.md" "airtable/README.md"
    echo "✅ Restored: airtable/README.md"
else
    echo "⚠️  Archive missing: airtable/README.md"
fi

if [ -f "historical/docs_archive_20251020_221927/integration_scripts/README.md" ]; then
    cp -v "historical/docs_archive_20251020_221927/integration_scripts/README.md" "integration_scripts/README.md"
    echo "✅ Restored: integration_scripts/README.md"
else
    echo "⚠️  Archive missing: integration_scripts/README.md"
fi

if [ -f "historical/docs_archive_20251020_221927/integration_scripts/AI_WORKFLOW_GUIDE.md" ]; then
    cp -v "historical/docs_archive_20251020_221927/integration_scripts/AI_WORKFLOW_GUIDE.md" "integration_scripts/AI_WORKFLOW_GUIDE.md"
    echo "✅ Restored: integration_scripts/AI_WORKFLOW_GUIDE.md"
else
    echo "⚠️  Archive missing: integration_scripts/AI_WORKFLOW_GUIDE.md"
fi

echo ""
echo "✅ Rollback complete!"
echo ""
echo "To verify, run: git diff"
