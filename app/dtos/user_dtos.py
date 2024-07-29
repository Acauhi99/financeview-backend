import re
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

class UserCreateDTO(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator('name')
    def validate_name(cls, value) -> str:
        if not re.match(r'^(?!.*  )(?!^[0-9@]+$)(?=.*[a-zA-Z])[a-zA-Z0-9@ ]+$', value):
            raise ValueError('Invalid name')
        return value

class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str
    
class UserUpdateDTO(BaseModel):
    name: str
    email: EmailStr
    url_image: Optional[str]

    @field_validator('name')
    def validate_name(cls, value) -> str:
        if not re.match(r'^(?!.*  )(?!^[0-9@]+$)(?=.*[a-zA-Z])[a-zA-Z0-9@ ]+$', value):
            raise ValueError('Invalid name')
        return value
    
class UserFavoriteStocksCreateDTO(BaseModel):
    user_id: int
    stock_ticker: str
    
    @field_validator('user_id')
    def validate_user_id(cls, value) -> int:
        if value < 1:
            raise ValueError('Invalid user id')
        return value