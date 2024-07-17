from pydantic import BaseModel


# class Stock(BaseModel):
#     id: int
#     ticker: str
#     name: str
#     owner_id: int

#     class Config:
#         from_attributes = True

# class User(BaseModel):
#     id: int
#     name: str
#     is_active: bool
#     stocks: list[Stock] = []

#     class Config:
#         from_attributes = True

# class UserCreate(BaseModel):
#     email: str
#     password: str