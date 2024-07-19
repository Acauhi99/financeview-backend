from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from app.sql.models import User
from app.sql.schemas import UserCreateDTO
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from fastapi import status
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta


crypt_context = CryptContext(schemes=['sha256_crypt'])
SECRET_KEY = '4f1209a00f0d497b84ef1c5259e894cf4bf61c4065082f741815c9d4a72f9322'
ALGORITHM = 'HS256'

class UserAuth:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user: UserCreateDTO):
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
        
    def user_login(self, user: UserCreateDTO, expiration: int = 30):
        user_exists = self.db.query(User).filter_by(email=user.email)

        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email or password is incorrect'
            )
        
        if not crypt_context.verify(user.password, user_exists.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email or password is incorrect'
            )
        
        expiration_time = datetime.now() + timedelta(minutes=expiration)

        payload = {
            'sub': user.email,
            'exp': expiration_time
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token