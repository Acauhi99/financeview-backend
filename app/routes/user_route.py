from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.sql.database import get_db
from app.auth.user_auth import UserAuth
from app.sql.schemas import UserCreateDTO

router = APIRouter(prefix='/user', tags=['user'])

@router.post("/register")
def user_register(user: UserCreateDTO, db: Session = Depends(get_db)):
    UserAuth(db).create(user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User created"}
    )