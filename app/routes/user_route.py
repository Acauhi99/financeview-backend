from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.verifier_auth import token_verify
from app.controllers.feedback_controller import FeedbackController
from app.controllers.user_controller import UserController
from app.sql.database import get_db
from app.sql.dtos import *


router = APIRouter(prefix='/user', tags=['user'])

@router.post("/register")
def user_register(user: UserCreateDTO, 
                  db: Session = Depends(get_db)):
    return UserController(db).create_user(user)

@router.post("/login")
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), 
               db: Session = Depends(get_db)):
    user = UserLoginDTO(email=form_data.username, password=form_data.password)
    return UserController(db).user_login(user)

@router.get("/image/{user_id}", dependencies=[Depends(token_verify)])
def user_image(user_id: int, 
               db: Session = Depends(get_db)):
    return UserController(db).get_user_image(user_id)

@router.put("/update/{user_id}", dependencies=[Depends(token_verify)])
def user_update(user_id: int, 
                user: UserUpdateDTO, 
                db: Session = Depends(get_db)):
    return UserController(db).update_user(user_id, user)

@router.patch("/desactive/{user_id}", dependencies=[Depends(token_verify)])
def user_desactive(user_id: int, 
                   db: Session = Depends(get_db)):
    return UserController(db).desactive_user(user_id)

@router.patch("/reactive/{user_email}")
def user_reactive(user_email: str, 
                  db: Session = Depends(get_db)):
    return UserController(db).reactive_user(user_email)

@router.get("/favorites/{user_id}", dependencies=[Depends(token_verify)])
def user_favorites_stocks(user_id: int, 
                   db: Session = Depends(get_db)):
    return UserController(db).get_user_favorites_stocks(user_id)

@router.post("/favorites", dependencies=[Depends(token_verify)])
def create_user_favorites_stock(user_favorite: UserFavoriteStocksCreateDTO, 
                   db: Session = Depends(get_db)):
    return UserController(db).create_user_favorite_stock(user_favorite)

@router.delete("/favorites", dependencies=[Depends(token_verify)])
def unfavorite_a_stock(user_favorite: UserFavoriteStocksCreateDTO, 
                   db: Session = Depends(get_db)):
    return UserController(db).delete_user_favorite_stock(user_favorite)

@router.post("/feedback", dependencies=[Depends(token_verify)])
def user_feedback(feedback: FeedbackCreateDTO, 
                  db: Session = Depends(get_db)):   
    return FeedbackController(db).create_feedback(feedback)

@router.get("/feedback")
def get_user_feedback(db: Session = Depends(get_db)):
    return FeedbackController(db).get_feedback()
