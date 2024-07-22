from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_database
from src.database.models import Section, User
from src.schemas.section import SectionSchema
from src.services.auth import auth_service


async def add_section(body: SectionSchema, db: AsyncSession = Depends(get_database), user=Depends(auth_service.get_current_user)):
    try:
        section = Section(**body.dict(), user_id=user.id)
        db.add(section)
        await db.commit()
        await db.refresh(section)
        return section
    except IntegrityError as e:
        await db.rollback()
        if 'duplicate key value violates unique constraint' in str(e):
            raise ValueError("A section with this name already exists.")
        else:
            raise ValueError(e)
    except (ValueError, TypeError) as e:
        await db.rollback()
        raise ValueError(e)


async def get_section_by_id(section_id: int, db: AsyncSession) -> Section:
    result = await db.execute(select(Section).where(Section.id == section_id))
    section = result.scalar_one_or_none()
    return section


async def get_sections(db: AsyncSession, user: User):
    result = await db.execute(select(Section).filter_by(user=user))
    sections = result.scalars().all()
    if sections is None:
        return []
    return sections


