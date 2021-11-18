import jwt
import db_conn
import db_class as db

engine = db_conn.engineconn()
session = engine.sessionmaker()

SECRET_KEY = 'bac1a159a966fd9292eaf4cb1e7f8c64217986a183100ad6eec571aecbbd48f9'

def create_token(token: dict):
    token = jwt.encode(token, SECRET_KEY, algorithm='HS256')
    return {'result': 'SUCCESS', 'token': token}

def decode_token(Authorization: str):

    try:
        de_token = jwt.decode(Authorization,SECRET_KEY, algorithms='HS256')

    except:
        result = 0

    else:
        result = session.query(db.Register).filter(db.Register.user_email == de_token['email'],db.Register.user_password == de_token['password']).all()

    return result