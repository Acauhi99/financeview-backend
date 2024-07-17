from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.sql import models

engine = create_engine(
    "sqlite:///./sql.db", connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
