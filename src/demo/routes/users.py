from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt

from demo.lib.jwt import ALGORITHM, SECRET_KEY
from demo.lib.models import User
from demo.lib.oauth2 import oauth2_bearer
from demo.lib.password import bcrypt_context

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


IN_MEMORY_USERS_DB = [
    {
        "id": 1,
        "username": "foo",
        "password": bcrypt_context.hash("bar"),
    },
]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
) -> User:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        ) from err

    username: str | None = payload.get("sub")
    user_id: int | None = payload.get("id")

    if not username or not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )

    return User(username=username, id=user_id)


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=User,
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated"}},
)
async def my_user_details(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    return user
