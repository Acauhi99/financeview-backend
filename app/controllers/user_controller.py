from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

from app.auth.token_auth import TokenAuth
from app.sql.models import User
from app.sql.dtos import UserCreateDTO, UserLoginDTO, UserUpdateDTO


class UserController:
    def __init__(self, db: Session):
        self.token_create = TokenAuth(db).token_create
        self.crypt_context = TokenAuth(db).crypt_context
        self.db = db
    
    def create_user(self, user: UserCreateDTO) -> dict:
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
        
        return {
            "message": "User created successfully",
            "status_code": status.HTTP_201_CREATED
        }
        
    def user_login(self, user: UserLoginDTO) -> dict:
        user_exists = self.db.query(User).filter_by(email=user.email).first()

        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email or password is incorrect'
            )

        if user_exists and not user_exists.is_active:
            raise HTTPException(
                status_code=status.HTTP_300_MULTIPLE_CHOICES,
                detail='User is inactive'
            )
        
        if not self.crypt_context.verify(user.password, user_exists.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email or password is incorrect'
            )
        
        return self.token_create(user_exists)

    def update_user(self, user_id: int, user: UserUpdateDTO) -> dict:
        user_exists = self.db.query(User).filter_by(id=user_id).first()

        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        try:
            user_exists.name = user.name
            user_exists.email = user.email
            user_exists.url_image = user.url_image
            self.db.commit()
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
        
        return {
            'message': 'User updated',
            'status_code': status.HTTP_200_OK
        }
    
    def desactive_user(self, user_id: int) -> dict:
        user_exists = self.db.query(User).filter_by(id=user_id).first()
        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        
        user_exists.is_active = False
        self.db.commit()
        return {
            'message': 'User desactive successfully',
            'status_code': status.HTTP_204_NO_CONTENT
        }
    
    def reactive_user(self, user_email: str) -> dict:
        user_exists = self.db.query(User).filter_by(email=user_email).first()
        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        
        user_exists.is_active = True
        self.db.commit()
        return self.token_create(user_exists)