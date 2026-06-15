from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from database import get_db 
from schemas import UserLogin
import models
import utils
import oauth

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(credential:UserLogin ,db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == credential.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credential")
    
    if not utils.verify(credential.password, user.password): #user.password is comming from database, it will be stored hashed password
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credential")
    
    #create a toke and return token
    access_token = oauth.create_access_token(data={"user_id": user.id}) #we only provided user_id in paylod, we can put anything

    return {"token": access_token, "token_type":"bearer"}