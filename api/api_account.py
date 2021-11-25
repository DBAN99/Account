from fastapi import Header, APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import MetaData
from dbconn import db_conn, db_class as db
from mk_package import mk_token


router = APIRouter()
metadata = MetaData()
engine = db_conn.engineconn()
session = engine.sessionmaker()
connect = engine.connection()


# ----------------------- Class  -----------------------
class Item(BaseModel):
    user_amount: str
    user_memo: str

class Edit(BaseModel):
    user_amount: str
    user_memo: str

class Delete(BaseModel):
    memo_del : bool

class Id(BaseModel):
    num_id: int


# ----------------------- Request -----------------------
# 전체 리스트 조회(삭제되지 않은 것)
@router.get("/accountmemo" ,tags=["crud"])
async def get_account(Authorization : str = Header(None)):

    if mk_token.decode_token(Authorization) == 0:
        raise HTTPException(status_code=404, detail="Token not found")

    else:
        result = session.query(db.Account.user_amount, db.Account.user_memo).filter(db.Account.memo_del == 0).all()

    return result

# 특정 가계부 조회 (삭제되지 않은 것)
@router.get("/accountmemo/{id}",tags=["crud"])
async def get_account_id(id : int ,Authorization : str = Header(None)):

    if mk_token.decode_token(Authorization) == 0:
        raise HTTPException(status_code=404, detail="Token not found")

    else:
        result = session.query(db.Account).filter(db.Account.memo_id == id, db.Account.memo_del == 0 ).all()

        if result == []:
            raise HTTPException(status_code=404, detail="Token not found")

    return result

# 데이터 입력
@router.post("/accountmemo",tags=["crud"])
async def post_account(item: Item,Authorization : str = Header(None)):

    check_token = mk_token.decode_token(Authorization)
    if check_token == 0:
        raise HTTPException(status_code=404, detail="Token not found")

    else:
        user_id = check_token[0].user_id
        addMemo = db.Account(owner_id=user_id, user_amount=item.user_amount, user_memo=item.user_memo)
        session.add(addMemo)
        session.commit()
        result = HTTPException(status_code=200, detail="Create Complete")

    return result

# 데이터 수정
@router.patch("/accountmemo/{id}",tags=["crud"])
async def patch_account_id(id : int,edit : Edit,Authorization : str = Header(None)):

    if mk_token.decode_token(Authorization) == 0:
        raise HTTPException(status_code=404, detail="Token not found")

    else:
        session.query(db.Account).filter(db.Account.memo_id == id).update(dict(user_memo =edit.user_memo,user_amount=edit.user_amount))
        session.commit()
        result = HTTPException(status_code=200, detail="Edit Complete")

    return result

# 해당 memo_id를 가진 데이터 삭제
@router.delete("/accountmemo/{id}",tags=["crud"])
async def del_account_id(id : int,delete : Delete,Authorization : str = Header(None)):

    if mk_token.decode_token(Authorization) == 0:
        raise HTTPException(status_code=404, detail="Token not found")

    else:
        session.query(db.Account).filter(db.Account.memo_id == id).update(dict(memo_del=delete.memo_del))
        session.commit()
        result = HTTPException(status_code=200, detail="Delete Complete")

    return result

# 해당 memo_id를 가진 데이터 복구
@router.post("/accountmemo/{id}",tags=["crud"])
async def post_account_id(id : int,delete : Delete,Authorization : str = Header(None)):

    if mk_token.decode_token(Authorization) == 0:
        raise HTTPException(status_code=404, detail="Token not found")

    else:
        session.query(db.Account).filter(db.Account.memo_id == id).update(dict(memo_del=delete.memo_del))
        session.commit()
        result = HTTPException(status_code=200, detail="Recover Complete")

    return result


# ----------------------- Request -----------------------
