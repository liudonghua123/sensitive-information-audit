from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.db import models
from app.schemas import User, UserCreate, UserUpdate
from app.api import deps
from app.core import security

router = APIRouter()

@router.get("/", response_model=List[User])
async def read_users(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.check_permission("user:read")),
) -> Any:
    """
    Retrieve users.
    """
    result = await db.execute(
        select(models.User)
        .options(selectinload(models.User.roles).options(selectinload(models.Role.permissions)))
        .offset(skip)
        .limit(limit)
    )
    users = result.scalars().all()
    return users

@router.post("/", response_model=User)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate,
    current_user: models.User = Depends(deps.check_permission("user:create")),
) -> Any:
    """
    Create new user.
    """
    result = await db.execute(select(models.User).where(models.User.username == user_in.username))
    user = result.scalars().first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    
    user = models.User(
        username=user_in.username,
        hashed_password=security.get_password_hash(user_in.password),
        is_superuser=user_in.is_superuser,
    )
    
    if user_in.role_ids:
        result = await db.execute(select(models.Role).where(models.Role.id.in_(user_in.role_ids)))
        roles = result.scalars().all()
        user.roles = roles
        
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Reload with roles and permissions
    result = await db.execute(
        select(models.User)
        .where(models.User.id == user.id)
        .options(selectinload(models.User.roles).options(selectinload(models.Role.permissions)))
    )
    user = result.scalars().first()
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: models.User = Depends(deps.check_permission("user:update")),
) -> Any:
    """
    Update a user.
    """
    result = await db.execute(
        select(models.User)
        .where(models.User.id == user_id)
        .options(selectinload(models.User.roles).options(selectinload(models.Role.permissions)))
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
        
    update_data = user_in.dict(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        hashed_password = security.get_password_hash(update_data["password"])
        del update_data["password"]
        user.hashed_password = hashed_password
        
    if "role_ids" in update_data:
        role_ids = update_data["role_ids"]
        del update_data["role_ids"]
        if role_ids is not None:
            result = await db.execute(select(models.Role).where(models.Role.id.in_(role_ids)))
            roles = result.scalars().all()
            user.roles = roles
            
    for field, value in update_data.items():
        setattr(user, field, value)
        
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.delete("/{user_id}", response_model=Any)
async def delete_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    current_user: models.User = Depends(deps.check_permission("user:delete")),
) -> Any:
    """
    Delete a user.
    """
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Users cannot delete themselves",
        )
        
    # Delete user associations first if necessary (cascade might handle it but explicit is safer)
    # user_roles table handles cascade usually if configured, but here we just delete user
    await db.delete(user)
    await db.commit()
    return {"ok": True}

@router.get("/me", response_model=User)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
