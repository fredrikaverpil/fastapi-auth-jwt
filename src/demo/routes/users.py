from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt

from demo.lib.jwt import ALGORITHM, SECRET_KEY, oauth2_bearer
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
    }
]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return {"username": username, "id": user_id}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )


user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/me")
async def my_user_details(
    user: user_dependency,
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated failed",
        )
    return user
