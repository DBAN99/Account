from datetime import datetime, timedelta
from fastapi import APIRouter
from pydantic import EmailStr, BaseModel

from dbconn import db_conn, db_class as conn
from mk_package import mk_token

router = APIRouter()
engine = db_conn.engineconn()
session = engine.sessionmaker()


# ----------------------------- Class -----------------------------
class Users(BaseModel):
    user_email: EmailStr
    user_password: str

class Login(BaseModel):
    login_email: EmailStr
    login_password: str


# ----------------------------- API -----------------------------
# 이메일,비밀번호 입력 시 db에 저장 [해시 이용하기]
@router.post("/register", tags=["login"])
async def post_register(user: Users):
    addMemo = conn.Register(user_email=user.user_email, user_password=user.user_password)
    session.add(addMemo)

    try:
        session.commit()
        result = "DB 적용 완료"

    except:
        result = "Email이 중복 되었습니다. 다시 입력해주세요 :)"

    return result

# 이메일, 비밀번호가 db속 데이터와 일치하면 jwt 토큰을 발행
@router.post("/login", tags=["login"])
async def post_login(login: Login):
    result = session.query(conn.Register).filter(conn.Register.user_email == login.login_email,conn.Register.user_password == login.login_password).all()
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