from .. import models, schemas
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db 
from ..schemas import PostBase, UserCreate, UserOut
import hashlib

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user:UserCreate, db: Session = Depends(get_db)):
    user_data = user.model_dump()

    #if user email is already exist, raise exception
    existing_user = db.query(models.User).filter(models.User.email == user_data["email"]).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    raw_password = user_data.pop("password")
    hashed_password = hashlib.sha256(raw_password.encode()).hexdigest()
    new_user = models.User(**user_data, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"user not found with id : {id}")
    
    return user