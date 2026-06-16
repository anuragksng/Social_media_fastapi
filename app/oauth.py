import jwt
from jose import JWTError
from datetime import datetime, timedelta, timezone
import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import models
from database import get_db

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

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

    except JWTError:
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