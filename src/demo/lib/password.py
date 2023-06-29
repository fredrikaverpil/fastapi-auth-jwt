from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(
    plain_password: str,
    hashed_password: str,
):
    return bcrypt_context.verify(plain_password, hashed_password)
