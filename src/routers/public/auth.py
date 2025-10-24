from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.dependencies.auth import authenticate_user
from src.dependencies.basic import get_db
from src.schemas.basic import Token
from src.utils.credentials import create_access_token

router = APIRouter()


@router.post("/login")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    token = create_access_token({"sub": user.account[0].username})

    return Token(access_token=token, token_type="bearer")
