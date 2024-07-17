from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt  # noqa
from src.config.config import config

from passlib.context import CryptContext


class Auth:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

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
            expiration = datetime.now() + timedelta(seconds=expires_delta)
        else:
            expiration = datetime.now() + timedelta(minutes=15)

        copied.update({'iat': datetime.now(), 'exp': expiration, "scope": "access_token"})
        encoded_access_token = jwt.encode(copied, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return encoded_access_token

    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        copied = data.copy()
        if expires_delta:
            expiration = datetime.now() + timedelta(seconds=expires_delta)
        else:
            expiration = datetime.now() + timedelta(days=7)

        copied.update({'iat': datetime.now(), 'exp': expiration, "scope": "access_token"})
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


auth_service = Auth()
