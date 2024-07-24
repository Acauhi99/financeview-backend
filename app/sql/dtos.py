import re
from typing import Optional
from pydantic import BaseModel, field_validator

class UserCreateDTO(BaseModel):
    name: str
    email: str
    password: str

    @field_validator('name')
    def validate_name(cls, value) -> str:
        if not re.match('^(?!^[0-9@]+$)(?=.*[a-zA-Z])[a-zA-Z0-9@]+$', value):
            raise ValueError('Invalid name')
        return value
    
    @field_validator('email')
    def validate_email(cls, value) -> str:
        if not '@' in value:
            raise ValueError('Invalid email')
        return value

class UserLoginDTO(BaseModel):
    email: str
    password: str

    @field_validator('email')
    def validate_email(cls, value) -> str:
        if not '@' in value:
            raise ValueError('Invalid email')
        return value


class FeedbackCreateDTO(BaseModel):
    user_id: int
    rating: float
    description: str

    @field_validator('rating')
    def validate_rating(cls, value) -> float:
        if value < 1 or value > 5:
            raise ValueError('Invalid rating')
        return value

    @field_validator('description')
    def validate_description(cls, value) -> str:
        if len(value) < 3:
            raise ValueError('Description too short')
        return value
    
    @field_validator('user_id')
    def validate_user_id(cls, value) -> int:
        if value < 1:
            raise ValueError('Invalid user id')
        return value
    
class FeedbackReadDTO(BaseModel):
    user_name: str
    url_img_user: Optional[str]  
    rating: float
    description: str
