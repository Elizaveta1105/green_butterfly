from datetime import date, datetime

from fastapi import Depends
from fastapi.exceptions import ResponseValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_database
from src.database.models import Spendings, Section
from src.schemas.spending import SpendingSchema, SpendingUpdateSchema
from src.services.currency import currency
from src.repository.section import get_section_by_id


async def add_spending(body: SpendingSchema, db: AsyncSession = Depends(get_database)):
    try:
        section = await get_section_by_id(body.section_id, db)
        if not section:
            raise ValueError("Section not found")
        spending = Spendings(**body.dict())

        if spending.sum:
            date_value = spending.date if body.date else datetime.now().date()
            currency_val = spending.currency if body.currency else "USD"
            spending.date = date_value

            currency_sum = await currency.get_currency_rate(date_value.strftime("%d.%m.%Y"), currency_val)
            spending.sum_currency = round(spending.sum / currency_sum, 2)
            section.sum += spending.sum
            section.sum_currency += spending.sum_currency
        db.add(spending)
        await db.commit()
        await db.refresh(spending)
        return spending
    except (ValueError, TypeError) as e:
        await db.rollback()
        raise


async def get_spending_by_id(idx: int, db: AsyncSession = Depends(get_database)):
    try:
        stmt = select(Spendings).filter_by(id=idx)
        result = await db.execute(stmt)
        spending = result.scalar_one_or_none()
        return spending
    except (ValueError, ResponseValidationError) as e:
        raise ValueError(e)


async def get_spending_by_section(idx: int, db: AsyncSession = Depends(get_database)):
    try:
        stmt = select(Spendings).where(Spendings.section_id == idx)
        result = await db.execute(stmt)
        spendings = result.scalars().all()
        if not spendings:
            return []
        return spendings
    except ValueError as e:
        raise ValueError(e)


async def edit_spending_by_id(body: SpendingUpdateSchema, idx: int, db: AsyncSession = Depends(get_database)):
    try:
        stmt = select(Spendings).filter_by(id=idx)
        result = await db.execute(stmt)
        spending = result.scalar_one_or_none()
        if not spending:
            raise ValueError("Spending not found")
        for key, value in body.dict().items():
            if value:
                setattr(spending, key, value)
        await db.commit()
        await db.refresh(spending)
        return spending
    except ValueError as e:
        raise ValueError(e)


async def delete_spending_by_id(idx: int, db: AsyncSession = Depends(get_database)):
    try:
        stmt = select(Spendings).filter_by(id=idx)
        result = await db.execute(stmt)
        spending = result.scalar_one_or_none()
        if spending:
            await db.delete(spending)
            await db.commit()
            return spending
        else:
            raise ValueError("Spending not found")
    except ValueError as e:
        raise ValueError(e)
