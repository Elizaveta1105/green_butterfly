from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_database
from src.database.models import Section
from src.schemas.section import SectionSchema
from src.services.auth import auth_service


async def add_section(body: SectionSchema, db: AsyncSession = Depends(get_database), user=Depends(auth_service.get_current_user)):
    try:
        section = Section(**body.dict(), user_id=user.id)
        db.add(section)
        await db.commit()
        await db.refresh(section)
        return section
    except ValueError as e:
        await db.rollback()
        raise ValueError(e)


