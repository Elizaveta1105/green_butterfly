from fastapi import APIRouter, status, Depends, Request, BackgroundTasks, HTTPException
from fastapi.security import HTTPBearer
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserSchema, UserResponseSchema, TokenSchema
from src.database.db import get_database
from src.repository.users import get_user_by_email, create_user, confirm_email
from src.services.auth import auth_service
from src.services.email import send_email

router = APIRouter(prefix="/auth", tags=["auth"])
get_refresh_token = HTTPBearer()


@router.post(
    "/signup",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RateLimiter(times=1, seconds=20))]
)
async def signup(
    body: UserSchema,
    bt: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_database),
):
    exist_user = await get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await create_user(body, db)
    bt.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user


@router.post(
    "/login",
    response_model=TokenSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(RateLimiter(times=1, seconds=5))]
)
async def login(
    body: UserSchema,
    db: AsyncSession = Depends(get_database),
):
    user = await get_user_by_email(body.email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not registered."
        )
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed."
        )
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid data."
        )

    access_token = auth_service.create_access_token(data={"sub": user.email})
    refresh_token = auth_service.create_refresh_token(data={"sub": user.email})

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get('/confirmed_email/{token}', status_code=status.HTTP_200_OK)
async def confirm_email_from_email(token: str, db: AsyncSession = Depends(get_database)):
    email = auth_service.get_email_from_token(token)
    user = await get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.confirmed:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Your email already confirmed")

    await confirm_email(user, db)

    return {"message": "Email confirmed successfully"}

