from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from app.schemas import Connection
from app.db.models import DbType

class DbConnector:
    @staticmethod
    def get_database_url(connection: Connection) -> str:
        if connection.db_type == DbType.SQLITE:
            # For SQLite, use host as the file path
            db_path = connection.host
            if db_path:
                # Convert Windows backslashes to forward slashes
                db_path = db_path.replace('\\', '/')
                # SQLite URL format: sqlite+aiosqlite:///path/to/db
                if db_path.startswith('/'):
                    return f"sqlite+aiosqlite://{db_path}"
                else:
                    return f"sqlite+aiosqlite:///{db_path}"
            return "sqlite+aiosqlite:///:memory:"
        elif connection.db_type == DbType.MYSQL:
            return f"mysql+aiomysql://{connection.username}:{connection.password_encrypted}@{connection.host}:{connection.port}/{connection.db_name}"
        elif connection.db_type == DbType.POSTGRESQL:
            return f"postgresql+asyncpg://{connection.username}:{connection.password_encrypted}@{connection.host}:{connection.port}/{connection.db_name}"
        elif connection.db_type == DbType.ORACLE:
            port = connection.port or 1521
            return f"oracle+oracledb_async://{connection.username}:{connection.password_encrypted}@{connection.host}:{port}/?service_name={connection.db_name}"
        else:
            raise ValueError("Unsupported database type")

    @staticmethod
    def create_engine(connection: Connection) -> AsyncEngine:
        url = DbConnector.get_database_url(connection)
        return create_async_engine(url, echo=False)
    
    @staticmethod
    def get_engine(db_type: str, host: str = None, port: int = None, 
                   username: str = None, password: str = None, db_name: str = None):
        """Create engine for testing connections"""
        if db_type == "sqlite":
            # For SQLite, use host as the file path
            db_path = host or db_name
            if db_path:
                # Convert Windows backslashes to forward slashes
                db_path = db_path.replace('\\', '/')
                # SQLite URL format: sqlite+aiosqlite:///path/to/db or sqlite+aiosqlite:///C:/path/to/db
                if db_path.startswith('/'):
                    url = f"sqlite+aiosqlite://{db_path}"
                else:
                    url = f"sqlite+aiosqlite:///{db_path}"
            else:
                url = "sqlite+aiosqlite:///:memory:"
        elif db_type == "mysql":
            port = port or 3306
            url = f"mysql+aiomysql://{username}:{password}@{host}:{port}/{db_name}"
        elif db_type == "postgresql":
            port = port or 5432
            url = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}"
        elif db_type == "oracle":
            port = port or 1521
            url = f"oracle+oracledb_async://{username}:{password}@{host}:{port}/?service_name={db_name}"
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
        return create_async_engine(url, echo=False)
    
    @staticmethod
    async def get_database_metadata(engine: AsyncEngine, db_type: str):
        """Extract metadata from database including tables, views, columns, row counts, and sizes"""
        from sqlalchemy import inspect, text
        
        metadata_list = []
        
        async with engine.connect() as conn:
            # Get table and view names
            def get_table_info(sync_conn):
                inspector = inspect(sync_conn)
                tables = []
                for table_name in inspector.get_table_names():
                    tables.append({'name': table_name, 'type': 'table'})
                try:
                    for view_name in inspector.get_view_names():
                        tables.append({'name': view_name, 'type': 'view'})
                except:
                    pass  # Some databases don't support views
                return tables
            
            tables_info = await conn.run_sync(get_table_info)
            
            for table_info in tables_info:
                table_name = table_info['name']
                table_type = table_info['type']
                
                # Get column information
                def get_columns(sync_conn):
                    inspector = inspect(sync_conn)
                    return inspector.get_columns(table_name)
                
                columns_raw = await conn.run_sync(get_columns)
                columns = [
                    {
                        'name': col['name'],
                        'type': str(col['type']),
                        'nullable': col.get('nullable', True)
                    }
                    for col in columns_raw
                ]
                
                # Get row count
                row_count = None
                try:
                    result = await conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    row_count = result.scalar()
                except:
                    pass  # Some views or tables might not support COUNT
                
                # Estimate size (database-specific)
                size_bytes = None
                try:
                    if db_type == 'mysql':
                        result = await conn.execute(text(
                            f"SELECT (data_length + index_length) as size FROM information_schema.TABLES "
                            f"WHERE table_name = '{table_name}'"
                        ))
                        size_bytes = result.scalar()
                    elif db_type == 'postgresql':
                        result = await conn.execute(text(
                            f"SELECT pg_total_relation_size('{table_name}') as size"
                        ))
                        size_bytes = result.scalar()
                    elif db_type == 'sqlite':
                        # SQLite: estimate using page count
                        result = await conn.execute(text(
                            f"SELECT page_count * page_size as size FROM pragma_page_count('{table_name}'), pragma_page_size()"
                        ))
                        size_bytes = result.scalar()
                except:
                    pass
                
                metadata_list.append({
                    'name': table_name,
                    'type': table_type,
                    'row_count': row_count,
                    'size_bytes': size_bytes,
                    'columns': columns
                })
        
        return metadata_list

