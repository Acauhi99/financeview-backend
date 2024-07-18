from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.sql.database import get_db
from app.auth.user import UserUseCase
from app.sql.schemas import UserCreate

router = APIRouter(prefix='/user', tags=['user'])

@router.post("/register")
def user_register(user: UserCreate ,db: Session = Depends(get_db)):
    UserUseCase(db).create(user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content='User created'
    )