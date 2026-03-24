from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc, and_
from app.db import models
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[dict])
async def read_logs(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 50,
    level: Optional[str] = Query(None, description="Filter by log level: info, warning, error"),
    action: Optional[str] = Query(None, description="Filter by action"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    target_type: Optional[str] = Query(None, description="Filter by target type"),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Get system logs with optional filters"""
    query = select(models.SystemLog).order_by(desc(models.SystemLog.created_at))

    filters = []
    if level:
        filters.append(models.SystemLog.level == level)
    if action:
        filters.append(models.SystemLog.action.like(f"%{action}%"))
    if user_id:
        filters.append(models.SystemLog.user_id == user_id)
    if target_type:
        filters.append(models.SystemLog.target_type == target_type)

    if filters:
        query = query.where(and_(*filters))

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    logs = result.scalars().all()

    return [
        {
            "id": log.id,
            "level": log.level,
            "action": log.action,
            "message": log.message,
            "user_id": log.user_id,
            "username": log.user.username if log.user else None,
            "target_type": log.target_type,
            "target_id": log.target_id,
            "details": log.details,
            "ip_address": log.ip_address,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        }
        for log in logs
    ]


@router.get("/actions", response_model=List[str])
async def get_log_actions(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Get list of unique log actions"""
    result = await db.execute(
        select(models.SystemLog.action).distinct().order_by(models.SystemLog.action)
    )
    actions = result.scalars().all()
    return list(actions)