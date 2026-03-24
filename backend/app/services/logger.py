import json
from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import models


async def log_action(
    db: AsyncSession,
    action: str,
    level: str = "info",
    message: Optional[str] = None,
    user_id: Optional[int] = None,
    target_type: Optional[str] = None,
    target_id: Optional[int] = None,
    details: Optional[dict] = None,
    ip_address: Optional[str] = None,
):
    """Log an action to the system logs table"""
    log_entry = models.SystemLog(
        level=level,
        action=action,
        message=message,
        user_id=user_id,
        target_type=target_type,
        target_id=target_id,
        details=json.dumps(details) if details else None,
        ip_address=ip_address,
    )
    db.add(log_entry)
    await db.commit()
    return log_entry