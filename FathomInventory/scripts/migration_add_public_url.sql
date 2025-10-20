-- Add public_share_url column to calls table
-- Safe to run multiple times (IF NOT EXISTS not supported for columns, but won't error if already exists via scripting)

BEGIN;

-- Add the column (will error if already exists, but that's safe to ignore in the script)
ALTER TABLE calls ADD COLUMN public_share_url TEXT;

COMMIT;
