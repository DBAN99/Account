import api_login_register
from fastapi import FastAPI

import rest_api


def include_router(app):
    app.include_router(api_login_register.router, prefix="/login")
    app.include_router(rest_api.router, prefix="/crud")


def start_application():
    app = FastAPI()
    include_router(app)
    return app

app = start_application()