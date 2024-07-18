from pathlib import Path
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_database
from src.schemas.spending import SpendingResponseSchema, SpendingSchema
from src.repository.spending import add_spending, get_spending_by_id, get_spending_by_section
from src.services.auth import auth_service

router = APIRouter(prefix='/spending', tags=['spending'])


@router.post("/", response_model=SpendingResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_spending(body: SpendingSchema, db: AsyncSession = Depends(get_database), user=Depends(auth_service.get_current_user)):
    spending = await add_spending(body, db)
    return spending


@router.get("/{idx}", response_model=SpendingResponseSchema, status_code=status.HTTP_201_CREATED)
async def get_spending(idx: int = Path(ge=1), db: AsyncSession = Depends(get_database), user=Depends(auth_service.get_current_user)):
    spending = await get_spending_by_id(idx, db)
    if not spending:
        raise HTTPException(status_code=404, detail="Spending not found")
    return spending


@router.get("/all/{section_idx}", response_model=List[SpendingResponseSchema], status_code=status.HTTP_201_CREATED)
async def get_spendings_by_section(section_idx: int = Path(ge=1), db: AsyncSession = Depends(get_database), user=Depends(auth_service.get_current_user)):
    spendings = await get_spending_by_section(section_idx, db)
    if not spendings:
        return []
    return spendings
