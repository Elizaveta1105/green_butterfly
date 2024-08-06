from pathlib import Path
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_database
from src.schemas.spending import SpendingResponseSchema, SpendingSchema, SpendingUpdateSchema
from src.repository.spending import add_spending, get_spending_by_id, get_spending_by_section, edit_spending_by_id
from src.services.auth import auth_service

router = APIRouter(prefix='/spending', tags=['spending'])


@router.post("/", response_model=SpendingResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_spending(body: SpendingSchema, db: AsyncSession = Depends(get_database), user=Depends(auth_service.get_current_user)):
    try:
        spending = await add_spending(body, db)
        return spending
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{idx}", response_model=SpendingResponseSchema, status_code=status.HTTP_200_OK)
async def get_spending(idx: int = Path(ge=1), db: AsyncSession = Depends(get_database), user=Depends(auth_service.get_current_user)):
    try:
        spending = await get_spending_by_id(idx, db)
        if not spending:
            raise HTTPException(status_code=404, detail="Spending not found")
        return spending
    except (ValueError, TypeError, AttributeError, SyntaxError, KeyError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all/{section_idx}", response_model=List[SpendingResponseSchema], status_code=status.HTTP_200_OK)
async def get_spendings_by_section(section_idx: int = Path(ge=1), db: AsyncSession = Depends(get_database), user=Depends(auth_service.get_current_user)):
    try:
        spendings = await get_spending_by_section(section_idx, db)
        return spendings
    except (ValueError, TypeError, AttributeError, SyntaxError, KeyError) as e: # replace with several exceptions
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{idx}", response_model=SpendingResponseSchema, status_code=status.HTTP_200_OK)
async def edit_spending(body: SpendingUpdateSchema, idx: int = Path(ge=1), db: AsyncSession = Depends(get_database), user=Depends(auth_service.get_current_user)):
    try:
        spending = await edit_spending_by_id(body, idx, db)
        return spending
    except (ValueError, TypeError, AttributeError, SyntaxError, KeyError) as e:
        raise HTTPException(status_code=400, detail=str(e))
