from pathlib import Path
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_database
from src.database.models import User
from src.schemas.section import SectionResponseSchema, SectionSchema
from src.services.auth import auth_service
from src.repository.section import add_section, get_sections, edit_section_body, get_section_by_id

router = APIRouter(prefix='/section', tags=['section'])


@router.post("/", response_model=SectionResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_section(body: SectionSchema, db: AsyncSession = Depends(get_database), user: User = Depends(auth_service.get_current_user)):
    try:
        section = await add_section(body, db, user)
        return section
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sections", response_model=List[SectionResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_sections(db: AsyncSession = Depends(get_database), user: User = Depends(auth_service.get_current_user)):
    try:
        sections = await get_sections(db, user)
        return sections
    except (ValueError, TypeError, AttributeError, SyntaxError, KeyError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{section_id}", response_model=SectionResponseSchema, status_code=status.HTTP_201_CREATED)
async def get_section_by_idx(section_id: int = Path(ge=1), db: AsyncSession = Depends(get_database), user: User = Depends(auth_service.get_current_user)):
    try:
        section = await get_section_by_id(section_id, db)
        return section
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{section_id}", response_model=SectionResponseSchema, status_code=status.HTTP_201_CREATED)
async def edit_section(body: SectionSchema, section_id: int = Path(ge=1), db: AsyncSession = Depends(get_database), user: User = Depends(auth_service.get_current_user)):
    try:
        section = await edit_section_body(body, section_id, db, user)
        return section
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
