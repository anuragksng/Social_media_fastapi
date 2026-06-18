from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware


import models, schemas
from database import engine

from schemas import PostBase, UserCreate, UserOut

models.Base.metadata.create_all(bind=engine) #This will create the tables in the database if they do not exist

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message":"Home Page"}




