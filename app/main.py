from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, post, user, vote
from . import models, schemas
from .database import engine

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message":"Home Page"}




