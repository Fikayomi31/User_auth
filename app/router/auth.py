from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.jwt import create_access_token
from app.core.security import verify_password, hash_password
from app.dependencies import get_db, get_current_user
from app.model.user import User, UserRole
from app.schemas.user_schema import UserRegister, UserLogin, UserResponse



router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)

async def register(
        user_data: UserRegister,
        db: AsyncSession = Depends(get_db),
):

    # Check if the user already exists
    existing_user = await db.scalar(
        select(User).where(
            (User.username == user_data.username)
            | (User.email == str(user_data.email).lower())
        )
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username or email already exists.",
        )

    #Bcrypt accepts a maximum of 12 password bytes
    if len(user_data.password.encode("utf-8")) > 12:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must be 12 characters or less.",
        )

    new_user = User(
        username=user_data.username,
        email=str(user_data.email).lower(),
        hashed_password=hash_password(user_data.password),
        role=UserRole.USER,
    )
    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists.",
        )
    return new_user


@router.post("/login")
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    user = await db.scalar(
        select(User).where(
            User.email == str(user_data.email).lower()
        )
    )

    # Use the same reasonse for wrong email and password
    if user is None or not verify_password(
        user_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=str(user.id))

    return {
        "access_token": access_token,
        "token_type": "bearer",
        }


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
