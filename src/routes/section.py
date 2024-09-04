from pathlib import Path
from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_database
from src.database.models import User
from src.schemas.section import SectionResponseSchema, SectionSchema, SectionUpdateSchema
from src.services.auth import auth_service
from src.repository.section import add_section, get_sections, edit_section_body, get_section_by_id, remove_section
from src.services.error_handler import handle_errors

router = APIRouter(prefix='/section', tags=['section'])


@router.post("/", response_model=SectionResponseSchema, status_code=status.HTTP_201_CREATED)
@handle_errors
async def create_section(body: SectionSchema, db: AsyncSession = Depends(get_database),
                         user: User = Depends(auth_service.get_current_user)):

    return await add_section(body, db, user)


@router.get("/sections", response_model=List[SectionResponseSchema], status_code=status.HTTP_200_OK)
@handle_errors
async def get_all_sections(db: AsyncSession = Depends(get_database),
                           user: User = Depends(auth_service.get_current_user)):

    return await get_sections(db, user)


@router.get("/{section_id}", response_model=SectionResponseSchema, status_code=status.HTTP_200_OK)
@handle_errors
async def get_section_by_idx(section_id: int = Path(ge=1), db: AsyncSession = Depends(get_database),
                             user: User = Depends(auth_service.get_current_user)):

    return await get_section_by_id(section_id, db)


@router.put("/{section_id}", response_model=SectionResponseSchema, status_code=status.HTTP_200_OK)
@handle_errors
async def edit_section(body: SectionUpdateSchema, section_id: int = Path(ge=1), db: AsyncSession = Depends(get_database),
                       user: User = Depends(auth_service.get_current_user)):

    return await edit_section_body(body, section_id, db, user)


@router.delete("/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_errors
async def delete_section(section_id: int = Path(ge=1), db: AsyncSession = Depends(get_database),
                         user: User = Depends(auth_service.get_current_user)):

    return await remove_section(section_id, db, user)
