from fastapi import FastAPI,Depends
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.responses import RedirectResponse
from pydantic import BaseModel

import uvicorn

app = FastAPI()
SECRET = '2c01b7facd47e87237b6160b40c255a2b51cdafd0aa98814'
manager = LoginManager(SECRET, token_url='/auth/token')
fake_db = {'johndoe@e.mail': {'password': 'hunter2'}}


# ----------------------- Class  -----------------------

class NotAuthenticatedException(Exception):
    pass

class Item(BaseModel):
    user_amount : str
    user_memo: str





# ----------------------- API Method  -----------------------


# ----------------------- Register -----------------------
# 회원가입 부분입니다.
# ----------------------- Register -----------------------


# ----------------------- Login -----------------------

@app.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

def exc_handler(request, exc):
    return RedirectResponse(url='/login')

@manager.user_loader()
def load_user(email: str):  # could also be an asynchronous function
    user = fake_db.get(email)
    return user
manager.not_authenticated_exception = NotAuthenticatedException
# You also have to add an exception handler to your app instance
app.add_exception_handler(NotAuthenticatedException, exc_handler)

# ----------------------- Login -----------------------


# ----------------------- Request -----------------------

@app.get("/")
async def main():
    main = "Account API"
    return main

@app.get("/accountmemo")
async def get_account():

    return

@app.post("/accountmemo")
async def post_account():

    return

@app.put("/accountmemo")
async def put_account():

    return

@app.delete("/accountmemo")
async def del_account():

    return

# ----------------------- Request -----------------------


if __name__ == '__main__':
    uvicorn.run(app)