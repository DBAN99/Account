from fastapi import *
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.responses import RedirectResponse

import uvicorn

app = FastAPI()
SECRET = '2c01b7facd47e87237b6160b40c255a2b51cdafd0aa98814'
manager = LoginManager(SECRET, token_url='/auth/token')

fake_db = {'johndoe@e.mail': {'password': 'hunter2'}}


class NotAuthenticatedException(Exception):
    pass

@app.get("/")
async def main():
    main = "Account API"
    return main


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

# This will be deprecated in the future
# set your exception when initiating the instance
# manager = LoginManager(..., custom_exception=NotAuthenticatedException)


@manager.user_loader()
def load_user(email: str):  # could also be an asynchronous function
    user = fake_db.get(email)
    return user
manager.not_authenticated_exception = NotAuthenticatedException
# You also have to add an exception handler to your app instance
app.add_exception_handler(NotAuthenticatedException, exc_handler)


if __name__ == '__main__':
    uvicorn.run(app)