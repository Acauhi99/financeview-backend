from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.token_auth import TokenAuth
from app.db.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def token_verify(db: Session = Depends(get_db), 
                 token: str = Depends(oauth2_scheme)):
    return TokenAuth(db).verify_token(token)
