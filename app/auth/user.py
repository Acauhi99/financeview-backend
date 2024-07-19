from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from app.sql.models import User
from app.sql.schemas import UserCreate
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from fastapi import status
from passlib.context import CryptContext
from jose import JWTError, jwt


crypt_context = CryptContext(schemes=['sha256_crypt'])

class UserUseCase:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user: UserCreate):
        user_model = User(
            name=user.name,
            email=user.email,
            hashed_password=crypt_context.hash(user.password)
        )
        try:
            self.db.add(user_model)
            self.db.commit()
        except OperationalError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Database table not found'
            )
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User already exists'
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        
    def user_login(user: UserCreate, expiration: int):
        pass