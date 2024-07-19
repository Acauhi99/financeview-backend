from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.sql.database import get_db
from app.auth.user_auth import UserAuth
from app.sql.dtos import *
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/user', tags=['user'])

@router.post("/register")
def user_register(user: UserCreateDTO, db: Session = Depends(get_db)) -> JSONResponse:
    UserAuth(db).create_user(user)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User created"}
    )

@router.post("/login")
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> JSONResponse:
    user = UserLoginDTO(email=form_data.username, password=form_data.password)
    token_data = UserAuth(db).user_login(user)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=token_data
    )

