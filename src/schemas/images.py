from typing import Optional

from pydantic import BaseModel


class ImageSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    section_id: int
    images_url: Optional[str] = None


class ImageResponseSchema(BaseModel):
    id: int
    section_id: int
    images_url: str
    title: str | None
    description: str | None

    class Config:
        from_attributes = True
