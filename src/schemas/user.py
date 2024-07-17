from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=25)
    email: str = EmailStr


class UserSchema(UserBase):
    password: str = Field(..., min_length=6, max_length=10)


class UserResponseSchema(UserBase):
    id: int = 1

    class Config:
        from_attributes = True
