from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.controllers.feedback_controller import FeedbackAuth
from app.sql.database import get_db
from app.auth.user_auth import UserAuth
from app.auth.verifier_auth import token_verify
from app.sql.dtos import *
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/user', tags=['user'])

@router.post("/register")
def user_register(user: UserCreateDTO, db: Session = Depends(get_db)):
    UserAuth(db).create_user(user)
    return {
        "message": "User created successfully",
        "status_code": status.HTTP_201_CREATED
    }

@router.post("/login")
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserLoginDTO(email=form_data.username, password=form_data.password)
    token_data = UserAuth(db).user_login(user)
    return {
        "message": "User logged in successfully",
        "status_code": status.HTTP_200_OK,
        "data": token_data
    }

@router.post("/feedback", dependencies=[Depends(token_verify)])
def user_feedback(feedback: FeedbackCreateDTO, db: Session = Depends(get_db)):   
    return FeedbackAuth(db).create_feedback(feedback)

@router.get("/feedback")
def get_user_feedback(db: Session = Depends(get_db)):
    feedback_list = FeedbackAuth(db).get_feedback()
    return {
        "message": "Feedback retrieved successfully",
        "status_code": status.HTTP_200_OK,
        "data": feedback_list
    }
    