from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

class engineconn:

    def __init__(self,dbname:str):
        self.engine = create_engine(sql['name'] + '://' + sql['user']+ ':'+sql['password']+'@'+sql['host']+':'+sql['port']+'/'+dbname, pool_recycle =500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn