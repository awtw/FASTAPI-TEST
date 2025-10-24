from typing import Annotated

from fastapi import APIRouter, Depends

from src.database import models
from src.dependencies.auth import get_current_user
from src.schemas import base

router = APIRouter()


@router.get('/me', response_model=base.UserInfo)
async def me(
        user: Annotated[models.User, Depends(get_current_user)]
):
    return base.UserInfo.from_model(user)
