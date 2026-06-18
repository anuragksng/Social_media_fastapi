import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from . import models
from .database import get_db

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

load_dotenv()

# openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt 

# It checks whether the token is valid, extracts the user ID from it, and returns that ID in a structured form.
def verify_access_token(token:str, credential_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        id: int = payload.get("user_id")

        if id is None:
            raise credential_exception
        
        token_data = schemas.TokenData(id = id)

    except PyJWTError:
        raise credential_exception
    
    return token_data
    

def get_current_user(
    token: str = Depends(oauth2_schema),
    db: Session = Depends(get_db),
):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could't validate credential", headers={"WWW-Authenticate":"Bearer"})
    token_data = verify_access_token(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if user is None:
        raise credential_exception

    return user