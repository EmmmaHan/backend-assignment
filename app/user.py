import sqlalchemy as db
from sqlalchemy import MetaData, Column, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from config import get_db_uri
import datetime

engine = db.create_engine(get_db_uri())
connection = engine.connect()
metadata = MetaData()
Base = declarative_base

class ExtendedBase(Base):
    id = Column(Integer, primary_key = True)
    updated_at = Column(DateTime, default=func.utc_timestamp(), onupdate=func.utc_timestamp())
    created_at = Column(DateTime, default=func.utc_timestamp())

class User(ExtendedBase):
    __tablename__ = 'users'
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

# User.__table__.create(bind=engine, checkfirst=True)

Base.metadata.create_all(engine)
    