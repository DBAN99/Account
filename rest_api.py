from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy import MetaData

from jose import JWTError, jwt

import db_class

import db_conn
import uvicorn


app = FastAPI()
metadata = MetaData()
engine = db_conn.engineconn()
session = engine.sessionmaker()
connect = engine.connection()

# ----------------------- Class  -----------------------
class Item(BaseModel):
    user_amount : str
    user_memo: str
    memo_del : int

class Users(BaseModel):
    user_email: EmailStr
    user_password : str
    user_del : int

class Login(BaseModel):
    login_email : EmailStr
    login_password: str

class Id(BaseModel):
    num_id : int


# ----------------------- API Method  -----------------------


# ----------------------- Register/Login -----------------------
@app.post("/register")
async def post_account(user : Users):
    # 임시 데이터 넣기
    addMemo = db_class.Register(user_email=user.user_email, user_password =user.user_password,user_del= user.user_del)
    session.add(addMemo)

    try:
        session.commit()
        result = "DB 적용 완료"

    except:
        result = "Email이 중복 되었습니다. 다시 입력해주세요 :)"

    return result


@app.post("/login")
async def post_account(login : Login):
    result = session.query(db_class.Register.user_active).filter(db_class.Register.user_email == login.login_email,db_class.Register.user_password == login.login_password ).all()
    session.commit()

    if result == []:
        result = "아이디와 비밀번호를 다시 확인하세요 :)"
    else:
        user = session.query(db_class.Register.user_active).update({'user_active': db_class.Register.user_active + 1})
        print(user)
        session.commit()

    return result
# ----------------------- Register/Login -----------------------


# ----------------------- Request -----------------------

@app.get("/accountmemo")
async def get_account():
    result = session.query(db_class.Account.user_amount,db_class.Account.user_memo).filter(db_class.Account.memo_del == 0).all()
    return result

@app.post("/accountmemo")
async def post_account(item : Item):
    # 임시 데이터 넣기
    result = session.query().filter().all()
    addMemo = db_class.Account(owner_id= 454,user_amount = item.user_amount,user_memo = item.user_memo, memo_del = item.memo_del)
    session.add(addMemo)
    session.commit()
    return


# ----------------------- Request -----------------------


if __name__ == '__main__':
    uvicorn.run(app)