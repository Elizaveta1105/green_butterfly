from pathlib import Path
from typing import List

import cloudinary.uploader
from fastapi import APIRouter, Depends, status, File, UploadFile, Form, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.config import config
from src.database.db import get_database
from src.database.models import User
from src.repository.images import add_image, get_images_by_sectionid
from src.schemas.images import ImageResponseSchema, ImageSchema
from src.services.auth import auth_service

router = APIRouter(prefix="/image", tags=["images"])

cloudinary.config(
    cloud_name=config.CLD_NAME,
    api_key=config.CLD_API_KEY,
    api_secret=config.CLD_API_SECRET,
    secure=True,
)


@router.post(
    "/", response_model=ImageResponseSchema, status_code=status.HTTP_201_CREATED
)
async def post_image(
        title: str = Form(...),
        description: str = Form(...),
        section_id: int = Form(...),
        file: UploadFile = File(),
        db: AsyncSession = Depends(get_database),
        user: User = Depends(auth_service.get_current_user)
):
    public_id = f"users/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(version=res.get("version"))

    body = ImageSchema(title=title, description=description, section_id=section_id, images_url=res_url)

    image = await add_image(body, db)
    return image


@router.get(
    "/{section_id}", response_model=List[ImageResponseSchema], status_code=status.HTTP_200_OK
)
async def get_images_by_section(
        section_id: int = Path(ge=1),
        db: AsyncSession = Depends(get_database),
        user: User = Depends(auth_service.get_current_user)
):
    try:
        images = await get_images_by_sectionid(section_id, db)
        return images
    except (ValueError, TypeError, AttributeError, SyntaxError, KeyError) as e:
        raise HTTPException(status_code=400, detail=str(e))
