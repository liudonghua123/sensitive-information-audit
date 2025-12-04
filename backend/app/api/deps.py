from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.core.config import settings
from app.core import security
from app.db import models
from app.schemas import TokenData

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY.get_secret_value(), algorithms=[settings.ALGORITHM]
        )
        token_data = TokenData(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    # Eager load roles and permissions
    from sqlalchemy.orm import selectinload
    result = await db.execute(
        select(models.User)
        .where(models.User.username == token_data.sub)
        .options(selectinload(models.User.roles).options(selectinload(models.Role.permissions)))
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

def check_permission(permission_code: str):
    async def dependency(current_user: models.User = Depends(get_current_user)):
        if current_user.is_superuser:
            return current_user
        
        for role in current_user.roles:
            for permission in role.permissions:
                if permission.code == permission_code:
                    return current_user
        
        raise HTTPException(
            status_code=403,
            detail=f"User does not have permission: {permission_code}"
        )
    return dependency
