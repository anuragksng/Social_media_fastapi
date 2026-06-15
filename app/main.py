from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from database import get_db 
from routers import post,user,auth


try:
    from .import models, schemas
    from .database import engine
except ImportError:
    import models, schemas
    from database import engine

from schemas import PostBase, UserCreate, UserOut

models.Base.metadata.create_all(bind=engine) #This will create the tables in the database if they do not exist

app = FastAPI()

#this method is used when we use pgsql with SQL query not the ORM
try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port="5432",
        database="postgres",
        user="postgres",
        password="admin123",
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor() #cursor is used to execute the sql command
    print("Databse Connection Established...")
except Exception as e:
    print("Database connection failed")
    print(e)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message":"Home Page"}




