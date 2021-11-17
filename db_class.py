from sqlalchemy import  Column, Integer, VARCHAR,TEXT,Boolean,ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Register(Base):

    __tablename__ = 'register_form'
    user_id = Column(Integer,nullable=False,primary_key=True,autoincrement=True)
    user_email = Column(VARCHAR(255), unique=True, nullable=True)
    user_password = Column(TEXT,nullable=False)
    user_del = Column(Boolean(),nullable=False,default=False)
    user_active = Column(Boolean(),nullable=False,default=False)

    def __repr__(self):
        return "<User(user_id='%s', user_email='%s', user_password='%s',user_del='%s',user_active='%s')>" % \
               (self.user_id,self.user_email, self.user_password, self.user_del, self.user_active)

class Account(Base):

    __tablename__ = 'account_memo'
    owner_id = Column(Integer,nullable=False,primary_key=True,autoincrement=True)
    user_amount = Column(TEXT,nullable=True)
    user_memo = Column(TEXT,nullable=True)
    memo_del = Column(Boolean(),default=False, nullable=False)
    memo_id = Column(Integer, autoincrement=True,nullable=False,primary_key=True)

    def __repr__(self):
        return "<User(owner_id='%s', user_amount='%s', user_memo='%s',memo_del='%s',memo_id='%s')>" % \
               (self.owner_id,self.user_email, self.user_password, self.memo_del, self.memo_id)