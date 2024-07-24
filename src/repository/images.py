from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models import User, Images
from src.schemas.images import ImageSchema


async def add_image(body: ImageSchema, db: AsyncSession):
    try:
        image = Images(**body.dict())
        db.add(image)
        await db.commit()
        await db.refresh(image)
        return image
    except Exception as e:
        await db.rollback()
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to upload image: {str(e)}")


async def get_images_by_sectionid(section_id: int, db: AsyncSession):
    try:
        image = await db.execute(select(Images).where(Images.section_id == section_id))
        result = image.scalars().all()
        if result is None:
            raise ValueError("No images found")
        return result
    except (ValueError, TypeError, AttributeError, SyntaxError, KeyError) as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to get images: {str(e)}")
