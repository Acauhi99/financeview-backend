from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.auth.user_auth import UserAuth
from sqlalchemy.orm import Session
from app.sql.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/login')

def token_verify(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_auth = UserAuth(db)
    user_auth.verify_token(token)