from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db 
from ..schemas import UserLogin
from .. import models, utils, oauth, schemas

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(credential:OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credential")
    
    if not utils.verify(credential.password, user.password): #user.password is comming from database, it will be stored hashed password
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credential")
    
    #create a toke and return token
    access_token = oauth.create_access_token(data={"user_id": user.id}) #we only provided user_id in paylod, we can put anything

    return {"access_token": access_token, "token_type":"bearer"}