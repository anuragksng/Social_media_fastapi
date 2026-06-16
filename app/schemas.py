from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(BaseModel):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# this is the response class 
class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email : EmailStr
    password : str


class UserLogin(BaseModel):
    email : EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
