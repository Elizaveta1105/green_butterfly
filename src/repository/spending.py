from datetime import date, datetime

from fastapi import Depends
from fastapi.exceptions import ResponseValidationError, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_database
from src.database.models import Spendings
from src.error_messages.messages import ERROR_SPENDING_NOT_FOUND, ERROR_TYPE_ERROR, ERROR_INVALID_INPUT, \
    ERROR_SECTION_NOT_FOUND
from src.exceptions.custom_exceptions import NotFoundException
from src.schemas.spending import SpendingSchema, SpendingUpdateSchema
from src.services.currency import currency_service
from src.repository.section import get_section_by_id


async def add_spending(body: SpendingSchema, db: AsyncSession = Depends(get_database)):
    try:
        section = await get_section_by_id(body.section_id, db)
        if not section:
            raise NotFoundException(ERROR_SECTION_NOT_FOUND)

        spending = Spendings(**body.dict())

        if spending.sum:
            date_value = spending.date if body.date else datetime.now().date()
            currency_val = spending.currency if body.currency else "USD"
            if not spending.currency:
                spending.currency = currency_val
            spending.date = date_value

            spending.sum_currency = await currency_service.set_currency_sum(spending.sum, date_value, currency_val)

            section.sum += spending.sum
            section.sum_currency += spending.sum_currency

        db.add(spending)
        await db.commit()
        await db.refresh(spending)
        return spending
    except ValueError as e:
        await db.rollback()
        raise ERROR_INVALID_INPUT.format(details=str(e))
    except TypeError as e:
        await db.rollback()
        raise ERROR_TYPE_ERROR.format(e)


async def get_spending_by_id(idx: int, db: AsyncSession = Depends(get_database)):
    try:
        stmt = select(Spendings).filter_by(id=idx)
        result = await db.execute(stmt)
        spending = result.scalar_one_or_none()
        if spending is None:
            raise NotFoundException(ERROR_SPENDING_NOT_FOUND)
        return spending
    except ValueError as e:
        raise ERROR_INVALID_INPUT.format(details=str(e))
    except ResponseValidationError as e:
        raise ERROR_INVALID_INPUT.format(details=str(e))


async def get_spending_by_section(idx: int, db: AsyncSession = Depends(get_database)):
    try:
        stmt = select(Spendings).where(Spendings.section_id == idx)
        result = await db.execute(stmt)
        spendings = result.scalars().all()
        if not spendings:
            return []
        return spendings
    except ValueError as e:
        raise ERROR_INVALID_INPUT.format(details=str(e))


async def edit_spending_by_id(body: SpendingUpdateSchema, idx: int, db: AsyncSession = Depends(get_database)):
    try:
        stmt = select(Spendings).filter_by(id=idx)
        result = await db.execute(stmt)
        spending = result.scalar_one_or_none()

        if spending is None:
            raise NotFoundException(ERROR_SPENDING_NOT_FOUND)

        for key, value in body.dict().items():
            if value:
                setattr(spending, key, value)
                if key == "sum":
                    spending.sum = value
                    spending.sum_currency = await currency_service.set_currency_sum(spending.sum, spending.date,
                                                                                    spending.currency)
        await db.commit()
        await db.refresh(spending)
        return spending
    except ValueError as e:
        raise ERROR_INVALID_INPUT.format(details=str(e))


async def delete_spending_by_id(idx: int, db: AsyncSession = Depends(get_database)):
    try:
        stmt = select(Spendings).filter_by(id=idx)
        result = await db.execute(stmt)
        spending = result.scalar_one_or_none()
        section = await get_section_by_id(spending.section_id, db)

        if section is None:
            raise NotFoundException(ERROR_SECTION_NOT_FOUND)

        if spending is None:
            raise NotFoundException(ERROR_SPENDING_NOT_FOUND)

        s_sum = spending.sum
        s_currency = spending.sum_currency
        section.sum -= s_sum
        section.sum_currency -= s_currency

        await db.delete(spending)
        await db.commit()
        return spending
    except ValueError as e:
        raise ERROR_INVALID_INPUT.format(details=str(e))
