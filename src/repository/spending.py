from datetime import date, datetime

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_database
from src.database.models import Spendings, Section
from src.schemas.spending import SpendingSchema
from src.services.currency import currency
from src.repository.section import get_section_by_id


async def add_spending(body: SpendingSchema, db: AsyncSession = Depends(get_database)):
    try:
        section = await get_section_by_id(body.section_id, db)
        spending = Spendings(**body.dict())
        if spending.sum:
            currency_sum = await currency.get_currency_usd(datetime.now().date().strftime("%d.%m.%Y"))
            spending.sum_currency = round(spending.sum / currency_sum, 2)
            section.sum += spending.sum
            section.sum_currency += spending.sum_currency
        db.add(spending)
        await db.commit()
        await db.refresh(spending)
        return spending
    except ValueError as e:
        await db.rollback()
        raise ValueError(e)


async def get_spending_by_id(idx: int, db: AsyncSession = Depends(get_database)):
    try:
        stmt = select(Spendings).filter_by(id=idx)
        result = await db.execute(stmt)
        spending = result.scalar_one_or_none()
        return spending
    except ValueError as e:
        raise ValueError(e)


async def get_spending_by_section(idx: int, db: AsyncSession = Depends(get_database)):
    try:
        stmt = select(Spendings).where(Spendings.section_id == idx)
        result = await db.execute(stmt)
        spendings = result.scalars().all()
        return spendings
    except ValueError as e:
        raise ValueError(e)
