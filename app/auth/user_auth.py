from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from app.sql.models import User
from app.sql.dtos import UserCreateDTO, UserLoginDTO
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from fastapi import status
from jose import JWTError, jwt
from datetime import datetime, timedelta

class UserAuth:
    def __init__(self, db: Session):
        self.crypt_context = CryptContext(schemes=['sha256_crypt'], deprecated='auto')
        self.SECRET_KEY = '4f1209a00f0d497b84ef1c5259e894cf4bf61c4065082f741815c9d4a72f9322'
        self.ALGORITHM = 'HS256'
        self.db = db
    
    def create_user(self, user: UserCreateDTO) -> None:
        user_model = User(
            name=user.name,
            email=user.email,
            hashed_password=self.crypt_context.hash(user.password)
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
        
    def user_login(self, user: UserLoginDTO, expiration: int = 30) -> dict:
        user_exists = self.db.query(User).filter_by(email=user.email).first()

        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email or password is incorrect'
            )
        
        if not self.crypt_context.verify(user.password, user_exists.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email or password is incorrect'
            )
        
        expiration_time = datetime.now() + timedelta(minutes=expiration)

        payload = {
            'name': user_exists.name,
            'email': user_exists.email,
            'user_id': user_exists.id,
            'user_url_image': user_exists.url_image
        }

        token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return {
            'access_token': token,
            'token_type': 'bearer',
            'exp': expiration_time.isoformat()
        }
    
    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token'
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        
        user_exists = self.db.query(User).filter_by(email=payload.get('email')).first()
        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User not found'
            )
        
        return payload
