import pickle

import redis
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.repository.users import get_user_by_email, set_refresh_token
from src.services.auth import Auth


class LoginHandler(Auth):
    def __init__(self, db: AsyncSession, cache: redis.Redis, auth_service: Auth):
        self.db = db
        self.cache = cache
        self.auth_service = auth_service

    async def get_user(self, username: str):
        user = await get_user_by_email(username, self.db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not registered."
            )
        return user

    async def is_confirmed(self, user: User):
        if not user.confirmed:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed."
            )

    async def create_tokens(self, user: User):
        access_token = await self.auth_service.create_access_token(data={"sub": user.email})
        refresh_token = await self.auth_service.create_refresh_token(data={"sub": user.email})
        await set_refresh_token(user, refresh_token, self.db)
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def handle_cache(self, user_hash: str, user_data: dict):
        user_data_bytes = pickle.dumps(user_data)
        self.cache.set(user_hash, user_data_bytes, ex=60)

