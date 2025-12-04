import re
import json
from datetime import datetime
from sqlalchemy import text, inspect
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from app.db import models
from app.schemas import Task, Rule
from app.services.connector import DbConnector
from app.db.session import AsyncSessionLocal

class Scanner:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def run_scan(self, task_id: int):
        # New session for background task
        async with AsyncSessionLocal() as session:
            task = await session.get(models.ScanTask, task_id)
            if not task:
                return
            
            task.status = models.TaskStatus.RUNNING
            await session.commit()
            
            try:
                # Get connection details
                connection = await session.get(models.DbConnection, task.connection_id)
                if not connection:
                    raise Exception("Connection not found")
                
                # Parse selected tables if provided
                selected_tables = None
                if task.selected_tables:
                    selected_tables = json.loads(task.selected_tables)
                
                # Parse selected rules if provided
                selected_rule_ids = None
                if task.selected_rules:
                    selected_rule_ids = json.loads(task.selected_rules)
                
                # Get all rules
                result = await session.execute(text("SELECT * FROM scan_rules"))
                all_rules = result.fetchall()
                
                # Filter rules if specific rules were selected
                if selected_rule_ids:
                    rules = [rule for rule in all_rules if rule.id in selected_rule_ids]
                else:
                    rules = all_rules
                
                # Connect to target DB
                target_engine = DbConnector.create_engine(connection)
                
                # Summary statistics
                summary_stats = {
                    'total_tables_scanned': 0,
                    'total_rows_scanned': 0,
                    'total_issues_found': 0,
                    'tables_with_issues': [],
                    'rules_triggered': {}
                }
                
                async with target_engine.connect() as target_conn:
                    # Get tables
                    # Async inspection is tricky, usually run_sync
                    def get_tables(sync_conn):
                        inspector = inspect(sync_conn)
                        return inspector.get_table_names()
                    
                    all_tables = await target_conn.run_sync(get_tables)
                    
                    # Filter tables if selection provided
                    tables_to_scan = selected_tables if selected_tables else all_tables
                    
                    for table in tables_to_scan:
                        if table not in all_tables:
                            continue  # Skip if table doesn't exist
                        
                        summary_stats['total_tables_scanned'] += 1
                        table_issues = 0
                        
                        # Scan each table
                        # Simple implementation: Select * limit 1000 (or pagination)
                        # For now, just scan first 100 rows
                        result = await target_conn.execute(text(f"SELECT * FROM {table} LIMIT 100"))
                        rows = result.fetchall()
                        columns = result.keys()
                        
                        summary_stats['total_rows_scanned'] += len(rows)
                        
                        for row in rows:
                            for idx, col_name in enumerate(columns):
                                cell_value = str(row[idx])
                                for rule in rules:
                                    # rule is a Row object, access by index or name? 
                                    # SQLAlchemy 1.4+ Row is like a named tuple
                                    rule_content = rule.content
                                    rule_type = rule.rule_type
                                    rule_name = rule.name
                                    
                                    match = False
                                    if rule_type == "regex":
                                        if re.search(rule_content, cell_value):
                                            match = True
                                    elif rule_type == "keyword":
                                        if rule_content in cell_value:
                                            match = True
                                            
                                    if match:
                                        # Found sensitive info
                                        scan_result = models.ScanResult(
                                            task_id=task.id,
                                            table_name=table,
                                            column_name=col_name,
                                            sensitive_content_masked=cell_value, # Store raw content for highlighting
                                            rule_name=rule_name
                                        )
                                        session.add(scan_result)
                                        
                                        # Update summary stats
                                        summary_stats['total_issues_found'] += 1
                                        table_issues += 1
                                        if rule_name not in summary_stats['rules_triggered']:
                                            summary_stats['rules_triggered'][rule_name] = 0
                                        summary_stats['rules_triggered'][rule_name] += 1
                        
                        if table_issues > 0:
                            summary_stats['tables_with_issues'].append({
                                'table_name': table,
                                'issue_count': table_issues
                            })
                
                task.status = models.TaskStatus.COMPLETED
                task.end_time = datetime.utcnow()
                task.scan_summary = json.dumps(summary_stats)
                await session.commit()
                
            except Exception as e:
                task.status = models.TaskStatus.FAILED
                task.summary = str(e)
                task.end_time = datetime.utcnow()
                await session.commit()

