from typing import Optional

from pydantic import BaseModel


class SectionSchema(BaseModel):
    name: str
    description: Optional[str] = None
    sum: Optional[float] = 0
    sum_currency: Optional[float] = 0


class SectionResponseSchema(SectionSchema):
    id: int = 1

    class Config:
        from_attributes = True
