from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app import schemas
from app.api import deps
from app.db import models

router = APIRouter()

@router.get("/", response_model=List[schemas.Role])
async def read_roles(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser), # Only admins can view roles for now
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve roles.
    """
    result = await db.execute(
        select(models.Role)
        .options(selectinload(models.Role.permissions))
        .offset(skip)
        .limit(limit)
    )
    roles = result.scalars().all()
    return roles

@router.post("/", response_model=schemas.Role)
async def create_role(
    *,
    db: AsyncSession = Depends(deps.get_db),
    role_in: schemas.RoleCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new role.
    """
    result = await db.execute(select(models.Role).where(models.Role.name == role_in.name))
    role = result.scalars().first()
    if role:
        raise HTTPException(
            status_code=400,
            detail="The role with this name already exists.",
        )
    
    role = models.Role(
        name=role_in.name,
        description=role_in.description,
    )
    
    if role_in.permission_ids:
        result = await db.execute(select(models.Permission).where(models.Permission.id.in_(role_in.permission_ids)))
        permissions = result.scalars().all()
        role.permissions = permissions
        
    db.add(role)
    await db.commit()
    await db.refresh(role)
    
    # Reload with permissions
    result = await db.execute(
        select(models.Role)
        .where(models.Role.id == role.id)
        .options(selectinload(models.Role.permissions))
    )
    role = result.scalars().first()
    return role

@router.put("/{role_id}", response_model=schemas.Role)
async def update_role(
    *,
    db: AsyncSession = Depends(deps.get_db),
    role_id: int,
    role_in: schemas.RoleCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a role.
    """
    result = await db.execute(
        select(models.Role)
        .where(models.Role.id == role_id)
        .options(selectinload(models.Role.permissions))
    )
    role = result.scalars().first()
    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )
        
    role.name = role_in.name
    role.description = role_in.description
    
    if role_in.permission_ids is not None:
        result = await db.execute(select(models.Permission).where(models.Permission.id.in_(role_in.permission_ids)))
        permissions = result.scalars().all()
        role.permissions = permissions
        
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role

@router.delete("/{role_id}", response_model=Any)
async def delete_role(
    *,
    db: AsyncSession = Depends(deps.get_db),
    role_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a role.
    """
    result = await db.execute(select(models.Role).where(models.Role.id == role_id))
    role = result.scalars().first()
    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )
    if role.name in ["Admin", "User"]:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete system roles",
        )
        
    await db.delete(role)
    await db.commit()
    return {"ok": True}

@router.get("/permissions", response_model=List[schemas.Permission])
async def read_permissions(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve permissions.
    """
    result = await db.execute(select(models.Permission).offset(skip).limit(limit))
    permissions = result.scalars().all()
    return permissions
