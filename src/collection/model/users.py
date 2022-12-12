import hashlib
from sqlalchemy import BOOLEAN, DATETIME, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import database
from datetime import date

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    alias = Column(String)
    created_at = Column(DATETIME)
    updated_at = Column(DATETIME)
    is_active = Column(BOOLEAN, default=1)


class UserRepository:
    def __init__(self):
        self.engine = database.load_sqlite()
        session_fn = sessionmaker(bind=self.engine)
        self.session = session_fn()
    
    def create_user(self, username, password, email, is_active):
        print(hashlib.md5(password.encode('utf-8')).hexdigest())
        new_user = User(username = username, email=email, password = hashlib.md5(password.encode('utf-8')).hexdigest(), alias=username,
         is_active=is_active, created_at=date.today(), updated_at=date.today())
        self.session.add(new_user)
        self.session.commit()

    def get_by_username_and_password(self, username, password):
        query = self.session.query(User).filter(User.username == username,
                                                User.password == hashlib.md5(password.encode('utf-8')).hexdigest()).all()
        return query

    def get_by_username(self, username):
        query = self.session.query(User).filter(User.username == username).all()
        return query
