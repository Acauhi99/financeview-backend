import re
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
    
