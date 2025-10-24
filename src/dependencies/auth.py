import os
from typing import Annotated

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from sqlalchemy.orm import Session

from src.database import models
from src.dependencies.basic import get_db
from src.utils.credentials import verify_password, decode_token
from src.utils.handler import handle_error, handle_none_value

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/public/auth/login", auto_error=True)

API_KEY = os.getenv("ADMIN_API_KEY", "admin")
SUPER_ADMIN_API_KEY = os.getenv("SUPER_ADMIN_API_KEY", "admin.root")

api_key_header = APIKeyHeader(name="X-ADMIN-TOKEN", auto_error=True, scheme_name="X-ADMIN-TOKEN")
super_admin_api_key_header = APIKeyHeader(name="X-SUPER-ADMIN-TOKEN", auto_error=True,
                                          scheme_name="X-SUPER-ADMIN-TOKEN")


@handle_none_value("User")
@handle_error
def get_user_by_username(db: Session, username: str) -> models.User | None:
    user = db.query(models.User).join(models.UserAccount).filter_by(username=username).first()
    return user


def authenticate_user(db: Session, username: str, password: str) -> models.User:
    user = get_user_by_username(db, username)
    truth_password = user.account[0].password
    if not verify_password(password, truth_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return user


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)
) -> models.User:
    payload = decode_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not validate credentials (username) not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_username(db, username)

    return user


async def get_admin_user(api_key: Annotated[str, Depends(api_key_header)] = None):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid api key"
        )


async def get_super_admin_user(api_key: Annotated[str, Depends(super_admin_api_key_header)] = None):
    if api_key != SUPER_ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid api key"
        )
