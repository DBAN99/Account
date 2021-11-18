from datetime import datetime, timedelta
from fastapi import APIRouter, FastAPI
from pydantic import EmailStr, BaseModel

import db_class as db
import db_conn
import mk_token

router = APIRouter()
engine = db_conn.engineconn()
session = engine.sessionmaker()

class Users(BaseModel):
    user_email: EmailStr
    user_password: str

class Login(BaseModel):
    login_email: EmailStr
    login_password: str

@router.post("/register", tags=["login"])
async def post_register(user: Users):
    # 임시 데이터 넣기
    addMemo = db.Register(user_email=user.user_email, user_password=user.user_password)
    session.add(addMemo)

    try:
        session.commit()
        result = "DB 적용 완료"

    except:
        result = "Email이 중복 되었습니다. 다시 입력해주세요 :)"

    return result


@router.post("/login", tags=["login"])
async def post_login(login: Login):
    result = session.query(db.Register).filter(db.Register.user_email == login.login_email,db.Register.user_password == login.login_password).all()
    session.commit()

    if result == []:
        result = "아이디와 비밀번호를 다시 확인하세요 :)"

    else:

        payload = {
            'email' : login.login_email,
            'password': login.login_password,
            'exp': datetime.utcnow() + timedelta(minutes=60)
        }
        result = mk_token.create_token(payload)

    return result