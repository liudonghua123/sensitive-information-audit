from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.db import models
from app.api import deps
from app.schemas import Connection, ConnectionCreate
from app.services.connector import DbConnector

router = APIRouter()

@router.get("/", response_model=List[Connection])
async def read_connections(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    result = await db.execute(select(models.DbConnection))
    connections = result.scalars().all()
    return connections

@router.post("/", response_model=Connection)
async def create_connection(
    connection_in: ConnectionCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    # Convert password to password_encrypted
    conn_data = connection_in.model_dump()
    if 'password' in conn_data:
        conn_data['password_encrypted'] = conn_data.pop('password')
    
    db_connection = models.DbConnection(**conn_data)
    db.add(db_connection)
    await db.commit()
    await db.refresh(db_connection)
    return db_connection

@router.post("/test")
async def test_connection(
    connection_in: ConnectionCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """Test a database connection without saving it"""
    try:
        connector = DbConnector()
        engine = connector.get_engine(
            db_type=connection_in.db_type,
            host=connection_in.host,
            port=connection_in.port,
            username=connection_in.username,
            password=connection_in.password,
            db_name=connection_in.db_name
        )
        
        # Try to connect
        async with engine.connect() as conn:
            await conn.execute(select(1))
        
        await engine.dispose()
        return {"success": True, "message": "Connection successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{connection_id}", response_model=Connection)
async def update_connection(
    connection_id: int,
    connection_in: ConnectionCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Update an existing database connection"""
    # Get existing connection
    result = await db.execute(select(models.DbConnection).where(models.DbConnection.id == connection_id))
    connection = result.scalars().first()
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    # Update fields
    conn_data = connection_in.model_dump(exclude_unset=True)
    if 'password' in conn_data and conn_data['password']:
        conn_data['password_encrypted'] = conn_data.pop('password')
    elif 'password' in conn_data:
        conn_data.pop('password')  # Don't update if empty
    
    for key, value in conn_data.items():
        setattr(connection, key, value)
    
    await db.commit()
    await db.refresh(connection)
    return connection


@router.delete("/{connection_id}")
async def delete_connection(
    connection_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Delete a database connection. Associated tasks will have connection_id set to NULL."""
    # Get the connection
    result = await db.execute(select(models.DbConnection).where(models.DbConnection.id == connection_id))
    connection = result.scalars().first()
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    # Delete the connection (tasks will have connection_id set to NULL automatically)
    await db.delete(connection)
    await db.commit()
    return {"ok": True}


