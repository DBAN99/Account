import api_login_register
import rest_api
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(api_login_register.router, tags=["login"])
api_router.include_router(rest_api.router, tags=["crud"])
