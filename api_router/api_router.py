from api import api_login_register
from api import api_account
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(api_login_register.router, tags=["login"])
api_router.include_router(api_account.router, tags=["crud"])
