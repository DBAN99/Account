from fastapi_login import LoginManager
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import MetaData, Column, BigInteger, Integer, VARCHAR,TEXT
from sqlalchemy.orm import declarative_base
import db_conn
import uvicorn


app = FastAPI()

Base = declarative_base()
metadata = MetaData()
engine = db_conn.engineconn()

session = engine.sessionmaker()
connect = engine.connection()

# ----------------------- Class  -----------------------

#Body 값
class Item(BaseModel):
    user_amount : str
    user_memo: str
    user_del : str
    memo_del : str
    memo_id : int

class Register(Base):

    __tablename__ = 'register_form'
    user_id = Column(Integer,nullable=False,primary_key=True)
    user_email = Column(VARCHAR(60),nullable=True)
    user_password = Column(TEXT,nullable=True)
    user_del = Column(VARCHAR(10),nullable=True,default=False)

    def __repr__(self):
        return "<User(user_id='%s', user_email='%s', user_password='%s',user_del='%s')>" % \
               (self.user_id,self.user_email, self.user_password, self.user_del)

class Account(Base):

    __tablename__ = 'account_memo'
    user_id = Column(Integer,nullable=False,primary_key=True)
    user_amount = Column(TEXT,nullable=True)
    user_memo = Column(TEXT,nullable=True)
    user_del = Column(VARCHAR(2),nullable=True)
    memo_del = Column(VARCHAR(2), nullable=True)
    memo_id = Column(Integer, autoincrement=True,nullable=True)

    def __repr__(self):
        return "<User(user_id='%s', user_amount='%s', user_memo='%s',user_del='%s',memo_del='%s',memo_id='%s')>" % \
               (self.user_id,self.user_email, self.user_password, self.user_del, self.memo_del, self.memo_id)

# ----------------------- API Method  -----------------------


# ----------------------- Register/Login -----------------------
# 회원가입 부분입니다.
# ----------------------- Register/Login -----------------------

# ----------------------- Request -----------------------

@app.get("/")
async def main():
    main = "Account API"
    return main

@app.get("/accountmemo")
async def get_account():

    return

@app.post("/accountmemo")
async def post_account(item : Item):
    # 임시 데이터 넣기
    addMemo = Account(user_id = 1 ,user_amount = item.user_amount,user_memo = item.user_memo, user_del = item.user_del, memo_del = item.memo_del, memo_id =item.memo_id)
    session.add(addMemo)
    session.commit()
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