import jwt
from dbconn import db_conn, db_class as db
import security

engine = db_conn.engineconn()
session = engine.sessionmaker()

SECRET_KEY = security.auth['secret']

def create_token(token: dict):
    token = jwt.encode(token, SECRET_KEY, algorithm='HS256')
    return {'result': 'SUCCESS', 'token': token}

def decode_token(Authorization: str):

    try:
        de_token = jwt.decode(Authorization,SECRET_KEY, algorithms='HS256')

    except:
        result = 0

    else:
        result = session.query(db.Register).filter(db.Register.user_email == de_token['email']).all()

    return result