from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False ,unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


class ActiveStocks(Base):
    __tablename__ = "active_stocks"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
