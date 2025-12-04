from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import models
from app.schemas import Rule, RuleCreate, RuleUpdate
from app.api import deps
from app.core.builtin_rules import BUILTIN_RULES

router = APIRouter()

@router.get("/", response_model=List[Rule])
async def read_rules(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    result = await db.execute(select(models.ScanRule).offset(skip).limit(limit))
    return result.scalars().all()

@router.post("/", response_model=Rule)
async def create_rule(
    *,
    db: AsyncSession = Depends(deps.get_db),
    rule_in: RuleCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    db_obj = models.ScanRule(**rule_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.post("/reset-builtin")
async def reset_builtin_rules(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Reset built-in rules to default"""
    # Delete existing system rules
    result = await db.execute(select(models.ScanRule).where(models.ScanRule.is_system == True))
    existing_rules = result.scalars().all()
    for rule in existing_rules:
        await db.delete(rule)
    
    # Add built-in rules
    for rule_data in BUILTIN_RULES:
        db_obj = models.ScanRule(**rule_data)
        db.add(db_obj)
    
    await db.commit()
    return {"message": f"Reset {len(BUILTIN_RULES)} built-in rules"}

@router.put("/{id}", response_model=Rule)
async def update_rule(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    rule_in: RuleUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    result = await db.execute(select(models.ScanRule).where(models.ScanRule.id == id))
    rule = result.scalars().first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    # Update fields
    for field, value in rule_in.model_dump(exclude_unset=True).items():
        setattr(rule, field, value)
    
    await db.commit()
    await db.refresh(rule)
    return rule

@router.delete("/{id}", response_model=Rule)
async def delete_rule(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    result = await db.execute(select(models.ScanRule).where(models.ScanRule.id == id))
    rule = result.scalars().first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    # Allow deleting system rules now
    await db.delete(rule)
    await db.commit()
    return rule
