from api import api_login_register, api_account
from fastapi import FastAPI


def include_router(app):
    app.include_router(api_login_register.router, prefix="/login")
    app.include_router(api_account.router, prefix="/crud")


def start_application():
    app = FastAPI()
    include_router(app)
    return app

app = start_application()
