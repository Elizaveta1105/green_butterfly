from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=25)
    email: str = None


class UserSchema(UserBase):
    password: str = Field(..., min_length=6, max_length=10)


class UserResponseSchema(UserBase):
    id: int = 1

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True
