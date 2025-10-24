from fastapi import APIRouter

from src.routers.public import auth

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
