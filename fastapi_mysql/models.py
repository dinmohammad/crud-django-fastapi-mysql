from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Boolean
from database import Base





class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username= Column(String(50), unique=True)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer)
    

class student(Base):
    __tablename__ = "student_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    stdCls = Column(String(100))
    details = Column(String(100))
    imageUrl = Column(String(500))
    user_id = Column(Integer)
