from fastapi import APIRouter
from passlib.context import CryptContext

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# TODO: bcrypt ...

IN_MEMORY_USERS_DB = [
    {
        "id": 1,
        "username": "foo",
        "password": bcrypt_context.hash("bar"),
    }
]


@router.get("/users")
async def get_users():
    # TODO: remove this endpoint
    return IN_MEMORY_USERS_DB
