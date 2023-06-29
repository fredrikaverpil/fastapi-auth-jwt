from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


# WARNING: don't store the secret key like this!
# Generated with: openssl rand -hex 32
SECRET_KEY = "fc5fe393d93d0f1c980eb88aafb56f90d1ae4cdfaaf4060455ef8e635157fd36"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")
