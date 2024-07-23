from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False ,unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    url_image = Column(String, nullable=True)

    feedbacks = relationship("Feedback", back_populates="user")

class ActiveStocks(Base):
    __tablename__ = "active_stocks"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", lazy=True)