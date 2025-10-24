from fastapi import APIRouter

from src.routers.private import auth, user

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(user.router, prefix="/user", tags=["User"])
