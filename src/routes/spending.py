from pathlib import Path
from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_database
from src.schemas.spending import SpendingResponseSchema, SpendingSchema, SpendingUpdateSchema
from src.repository.spending import add_spending, get_spending_by_id, get_spending_by_section, edit_spending_by_id, \
    delete_spending_by_id
from src.services.auth import auth_service
from src.services.error_handler import handle_errors

router = APIRouter(prefix='/spending', tags=['spending'])


@router.post("/", response_model=SpendingResponseSchema, status_code=status.HTTP_201_CREATED)
@handle_errors
async def create_spending(body: SpendingSchema, db: AsyncSession = Depends(get_database), user=Depends(auth_service.get_current_user)):
    return await add_spending(body, db)


@router.get("/{idx}", response_model=SpendingResponseSchema, status_code=status.HTTP_200_OK)
@handle_errors
async def get_spending(idx: int = Path(ge=1), db: AsyncSession = Depends(get_database), user=Depends(auth_service.get_current_user)):
    return await get_spending_by_id(idx, db)


@router.get("/all/{section_idx}", response_model=List[SpendingResponseSchema], status_code=status.HTTP_200_OK)
@handle_errors
async def get_spendings_by_section(section_idx: int = Path(ge=1), db: AsyncSession = Depends(get_database), user=Depends(auth_service.get_current_user)):
    return await get_spending_by_section(section_idx, db)


@router.put("/{idx}", response_model=SpendingResponseSchema, status_code=status.HTTP_200_OK)
@handle_errors
async def edit_spending(body: SpendingUpdateSchema, idx: int = Path(ge=1), db: AsyncSession = Depends(get_database), user=Depends(auth_service.get_current_user)):
    return await edit_spending_by_id(body, idx, db)


@router.delete("/{idx}", status_code=status.HTTP_204_NO_CONTENT)
@handle_errors
async def delete_spending(idx: int = Path(ge=1), db: AsyncSession = Depends(get_database), user=Depends(auth_service.get_current_user)):
    return await delete_spending_by_id(idx, db)
