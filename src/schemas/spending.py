import datetime
from typing import Optional

from pydantic import BaseModel


class SpendingSchema(BaseModel):
    section_id: int
    name: str
    description: Optional[str] = None
    date: Optional[datetime.date] = None
    currency: Optional[str] = None
    sum: float
    sum_currency: Optional[float] = 0


class SpendingUpdateSchema(SpendingSchema):
    section_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime.date] = None
    sum: Optional[float] = None


class SpendingResponseSchema(SpendingSchema):
    id: int = 1

    class Config:
        from_attributes = True
