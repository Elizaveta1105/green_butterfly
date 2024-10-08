from fastapi import Depends
from fastapi.exceptions import ResponseValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_database
from src.database.models import Section, User
from src.error_messages.messages import ERROR_SECTION_NOT_FOUND
from src.exceptions.custom_exceptions import NotFoundException
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
    if section is None:
        raise NotFoundException(ERROR_SECTION_NOT_FOUND)
    return section


async def get_sections(db: AsyncSession, user: User):
    result = await db.execute(select(Section).filter_by(user=user))
    sections = result.scalars().all()
    if not sections:
        return []
    return sections


async def edit_section_body(body: SectionSchema, section_id: int, db: AsyncSession, user: User):
    stmt = select(Section).filter_by(id=section_id, user=user)
    result = await db.execute(stmt)
    section = result.scalar_one_or_none()
    if section is None:
        raise NotFoundException(ERROR_SECTION_NOT_FOUND)
    for key, value in body.dict().items():
        if value:
            setattr(section, key, value)
    await db.commit()
    await db.refresh(section)
    return section


async def remove_section(section_id: int, db: AsyncSession, user: User):
    try:
        stmt = select(Section).filter_by(id=section_id, user_id=user.id)
        result = await db.execute(stmt)
        section = result.scalar_one_or_none()
        if section is None:
            raise NotFoundException(ERROR_SECTION_NOT_FOUND)
        elif section:
            await db.delete(section)
            await db.commit()
            return section
        return None
    except ValueError as e:
        await db.rollback()
        raise ValueError(e)
