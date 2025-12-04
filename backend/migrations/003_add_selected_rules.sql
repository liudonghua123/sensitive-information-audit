-- Migration script to add selected_rules column to scan_tasks table

-- Add selected_rules column to store JSON array of rule IDs selected for scan
ALTER TABLE scan_tasks ADD COLUMN selected_rules TEXT;
