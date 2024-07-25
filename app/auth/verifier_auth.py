from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.auth.token_auth import TokenAuth
from sqlalchemy.orm import Session
from app.sql.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def token_verify(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not token or token == "undefined":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing or undefined"
        )
    return TokenAuth(db).verify_token(token)
