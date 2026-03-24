from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import models
from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas import Token
from app.services.logger import log_action

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
async def login_access_token(
    request: Request,
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    result = await db.execute(select(models.User).where(models.User.username == form_data.username))
    user = result.scalars().first()

    ip_address = request.client.host if request.client else None

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        # Log failed login attempt
        await log_action(
            db,
            action="user_login",
            level="warning",
            message=f"Failed login attempt for username: {form_data.username}",
            user_id=user.id if user else None,
            ip_address=ip_address,
            details={"username": form_data.username, "success": False},
        )
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not user.is_active:
        await log_action(
            db,
            action="user_login",
            level="warning",
            message=f"Inactive user login attempt: {form_data.username}",
            user_id=user.id,
            ip_address=ip_address,
            details={"username": form_data.username, "success": False, "reason": "inactive_user"},
        )
        raise HTTPException(status_code=400, detail="Inactive user")

    # Log successful login
    await log_action(
        db,
        action="user_login",
        level="info",
        message=f"User logged in: {user.username}",
        user_id=user.id,
        ip_address=ip_address,
        details={"username": user.username, "success": True},
    )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.username, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
