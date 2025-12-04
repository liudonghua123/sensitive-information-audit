-- Migration script to add rules_used column to scan_tasks table

-- Add rules_used column to store JSON array of rules used in scan
ALTER TABLE scan_tasks ADD COLUMN rules_used TEXT;
