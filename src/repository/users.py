from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_database
from src.database.models import User
from src.schemas.user import UserSchema
from src.services.auth import auth_service


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_database)):
    stmt = select(User).filter_by(email=email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise ValueError("Verification error")

    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_database)):
    new_user = User(**body.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def confirm_email(user: User, db: AsyncSession = Depends(get_database)):
    user.confirmed = True
    await db.commit()


async def set_refresh_token(user: User, token: str, db: AsyncSession = Depends(get_database)):
    user.refresh_token = token
    await db.commit()


async def change_password(email: str, new_password: str, db: AsyncSession = Depends(get_database)):
    user = await get_user_by_email(email, db)
    user.password = auth_service.get_password_hash(new_password)
    await db.commit()

