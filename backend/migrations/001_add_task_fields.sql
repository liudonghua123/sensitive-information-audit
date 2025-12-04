-- Migration script to add new columns to scan_tasks table
-- Run this if you have an existing database

-- Add selected_tables column to store JSON array of table names
ALTER TABLE scan_tasks ADD COLUMN selected_tables TEXT;

-- Add scan_summary column to store JSON summary statistics
ALTER TABLE scan_tasks ADD COLUMN scan_summary TEXT;

-- Update existing records to have NULL values (default)
-- No action needed as SQLite allows NULL by default
