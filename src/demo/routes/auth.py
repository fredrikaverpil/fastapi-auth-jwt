from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from .users import IN_MEMORY_USERS_DB, bcrypt_context

router = APIRouter()

# WARNING: don't store the secret key like this!
# Generated with: openssl rand -hex 32
SECRET_KEY = "fc5fe393d93d0f1c980eb88aafb56f90d1ae4cdfaaf4060455ef8e635157fd36"
ALGORITHM = "HS256"


async def authenticate_user(
    username: str,
    password: str,
):
    user_record = None
    for record in IN_MEMORY_USERS_DB:
        if record["username"] == username:
            user_record = record.copy()
            user_password = user_record["password"]
            user_record.pop("password")  # NOTE: don't return the password hash
            break

    if not user_record:
        return False
    if not bcrypt_context.verify(password, user_password):
        return False

    return user_record


async def create_access_token(
    username: str,
    user_id: int,
    expires_delta: timedelta,
):
    expires_at = datetime.now(tz=timezone.utc) + expires_delta
    to_encode = {"sub": username, "id": user_id, "exp": expires_at}
    return jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        return "Failed to authenticate user"

    token = await create_access_token(
        username=user["username"],
        user_id=user["id"],
        expires_delta=timedelta(minutes=20),
    )
    return {"access_token": token, "token_type": "bearer"}
