from fastapi import APIRouter, Depends

from src.dependencies.auth import get_current_user, get_admin_user, get_super_admin_user
from src.routers.db import server as db_server
from src.routers.private import server as private_server
from src.routers.public import server as public_server
from src.routers.root import server as root_server

router = APIRouter()

router.include_router(public_server.router, prefix="/public")
router.include_router(private_server.router, prefix="/private", dependencies=[Depends(get_current_user)])
router.include_router(root_server.router, prefix="/root", dependencies=[Depends(get_admin_user)])
router.include_router(db_server.router, prefix="/db", dependencies=[Depends(get_super_admin_user)],
                      tags=["DB Actions"])
