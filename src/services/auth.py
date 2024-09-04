from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt  # noqa
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.config import config

from passlib.context import CryptContext

from src.database.db import get_database
from src.repository import users


class Auth:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

    SECRET_KEY = config.SECRET_KEY_JWT
    ALGORITHM = config.ALGORITHM

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    async def verify_password(self, password: str, hashed_password: str):
        is_valid = self.pwd_context.verify(password, hashed_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid data."
            )
        return is_valid

    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        copied = data.copy()
        if expires_delta:
            expiration = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expiration = datetime.utcnow() + timedelta(minutes=15)

        copied.update({'iat': datetime.utcnow(), 'exp': expiration, "scope": "access_token"})
        encoded_access_token = jwt.encode(copied, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return encoded_access_token

    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        copied = data.copy()
        if expires_delta:
            expiration = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expiration = datetime.utcnow() + timedelta(days=7)

        copied.update({'iat': datetime.utcnow(), 'exp': expiration, "scope": "access_token"})
        encoded_refresh_token = jwt.encode(copied, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return encoded_refresh_token

    async def create_email_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM)
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid token for email verification",
            )

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_database)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM)
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            print(e)
            raise credentials_exception

        user = await users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user


auth_service = Auth()
