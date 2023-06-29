from datetime import datetime, timedelta, timezone

from jose import jwt

# WARNING: don't store the secret key like this in production!
# Generated with: openssl rand -hex 32
SECRET_KEY = "fc5fe393d93d0f1c980eb88aafb56f90d1ae4cdfaaf4060455ef8e635157fd36"
ALGORITHM = "HS256"


async def create_access_token(
    username: str,
    user_id: int,
    expires_delta: timedelta,
) -> str:
    expires_at = datetime.now(tz=timezone.utc) + expires_delta
    to_encode = {"sub": username, "id": user_id, "exp": expires_at}
    return jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
