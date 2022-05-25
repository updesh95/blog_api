from email.policy import default
from typing import Collection

from psycopg2 import Timestamp
from database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey,Integer, String,Boolean, false
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key = True, nullable= False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean,server_default = 'True', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

class User(Base):
    __tablename__ = "users"
    email = Column(String,nullable=False,unique=True)
    password = Column(String, nullable=False)
    id= Column(Integer,primary_key=True,nullable= false)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
