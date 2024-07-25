from sqlalchemy.orm import Session
from app.sql.models import User
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from fastapi import status
from jose import JWTError, jwt
from datetime import datetime, timedelta

class TokenAuth:
    def __init__(self, db: Session):
        self.crypt_context = CryptContext(schemes=['sha256_crypt'], deprecated='auto')
        self.SECRET_KEY = '4f1209a00f0d497b84ef1c5259e894cf4bf61c4065082f741815c9d4a72f9322'
        self.ALGORITHM = 'HS256'
        self.db = db
    
    def token_create(self, user: User, expiration = 30) -> dict:
        expiration_time = datetime.now() + timedelta(minutes=expiration)

        payload = {
            'name': user.name,
            'email': user.email,
            'user_id': user.id,
            'user_url_image': user.url_image
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