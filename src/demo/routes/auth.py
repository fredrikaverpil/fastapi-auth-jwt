from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from demo.lib.jwt import create_access_token
from demo.lib.models import User
from demo.lib.password import verify_password

from .users import IN_MEMORY_USERS_DB

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


async def authenticate_user(
    username: str,
    password: str,
) -> User | None:
    user = None
    user_password = None
    for record in IN_MEMORY_USERS_DB:
        if record["username"] == username:
            user_record = record.copy()
            user_password = user_record["password"]
            user_record.pop("password")
            user = User(**user_record)
            break

    if not user or not user_password:
        return None
    if not await verify_password(password, user_password):
        return None

    return user


@router.post(
    "/token",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
    },
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> dict[str, str]:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    token = await create_access_token(
        username=user.username,
        user_id=user.id,
        expires_delta=timedelta(minutes=20),
    )
    return {"access_token": token, "token_type": "bearer"}
