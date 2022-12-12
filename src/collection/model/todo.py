import hashlib
from sqlalchemy import DATETIME, Column, INTEGER, String, MetaData, Table, Identity
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import database
from datetime import date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ToDo(Base):
    __tablename__ = 'todo'
    ID = Column(INTEGER, primary_key=True, autoincrement=True)
    TODO = Column(String)
    DESCRIPTION = Column(String)
    CREATED_AT = Column(DATETIME)

class ToDoRepository:
    def __init__(self):
        self.engine = database.load_sqlite()
        session_fn = sessionmaker(bind=self.engine)
        self.session = session_fn()
        self.create_table()
    
    def create_table(self):
        if not self.engine.dialect.has_table(self.engine.connect(), table_name=ToDo.__tablename__):
            metadata = MetaData(self.engine)
            Table(ToDo.__tablename__, metadata,
                    Column('ID', INTEGER, Identity(), primary_key=True),
                    Column('TODO', String),
                    Column('DESCRIPTION', String),
                    Column('CREATED_AT', DATETIME)
                )
            metadata.create_all()
    
    def create_todo(self, todo, description):
        new_todo = ToDo(TODO = todo, DESCRIPTION=description, CREATED_AT = date.today())
        self.session.add(new_todo)
        self.session.commit()
    
    def get_all(self):
        query = self.session.query(ToDo)
        return query

    def fetch_one_by_id(self, todo_id):
        query = self.session.query(ToDo).filter(ToDo.ID == todo_id).first()
        return query

    def update_by_id(self,todo_id,query):
        self.session.query(ToDo).filter(ToDo.ID == todo_id).update(query)
        self.session.commit()

    def delete_by_id(self, todo_id):
        query = self.session.query(ToDo).filter(ToDo.ID == todo_id).first()
        self.session.delete(query)
        self.session.commit()
