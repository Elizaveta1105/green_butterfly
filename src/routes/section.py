from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_database
from src.database.models import User
from src.schemas.section import SectionResponseSchema, SectionSchema
from src.services.auth import auth_service
from src.repository.section import add_section

router = APIRouter(prefix='/section', tags=['section'])


@router.post("/", response_model=SectionResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_section(body: SectionSchema, db: AsyncSession = Depends(get_database), user: User = Depends(auth_service.get_current_user)):
    section = await add_section(body, db, user)
    return section

