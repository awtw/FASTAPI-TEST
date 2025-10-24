from datetime import datetime, timedelta, timezone

from jose import jwt
# from passlib.context import CryptContext
from pwdlib import PasswordHash

from src.utils.handler import handle_jwt_error

pwd_context = PasswordHash.recommended() #CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "c1b3e4b3-4b3c-4b3e-8b3c-4b3e4b3c4b3e"
ALGORITHM = "HS256"
EXPIRE_IN_MIN = 30


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, period=timedelta(minutes=EXPIRE_IN_MIN)) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + period
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


@handle_jwt_error
def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
