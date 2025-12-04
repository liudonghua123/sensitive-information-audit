-- Migration script to fix database schema issues
-- 1. Drop redundant rules_used column
-- 2. Make connection_id nullable and add SET NULL on delete

-- Drop rules_used column (redundant with selected_rules)
-- Note: SQLite doesn't support DROP COLUMN directly, need to recreate table

-- Create new scan_tasks table with correct schema
CREATE TABLE scan_tasks_new (
    id INTEGER NOT NULL,
    connection_id INTEGER,
    status VARCHAR,
    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME,
    summary TEXT,
    selected_tables TEXT,
    scan_summary TEXT,
    selected_rules TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY(connection_id) REFERENCES db_connections (id) ON DELETE SET NULL
);

-- Copy data from old table
INSERT INTO scan_tasks_new (id, connection_id, status, start_time, end_time, summary, selected_tables, scan_summary, selected_rules)
SELECT id, connection_id, status, start_time, end_time, summary, selected_tables, scan_summary, selected_rules
FROM scan_tasks;

-- Drop old table
DROP TABLE scan_tasks;

-- Rename new table
ALTER TABLE scan_tasks_new RENAME TO scan_tasks;

-- Recreate index
CREATE INDEX ix_scan_tasks_id ON scan_tasks (id);
