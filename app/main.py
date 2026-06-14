from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from database import get_db

try:
    from . import models
    from .database import engine
except ImportError:
    import models
    from database import engine

models.Base.metadata.create_all(bind=engine) #This will create the tables in the database if they do not exist

app = FastAPI()

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port="5433",
        database="fastapi_tutorial",
        user="postgres",
        password="1234@1234",
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor() #cursor is used to execute the sql command
    print("Databse Connection Established...")
except Exception as e:
    print("Database connection failed")
    print(e)



class Post(BaseModel):
    title: str
    content: str
    published: bool = True

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p[id] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message":"Home Page"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"Status": "Success"}

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"Data":posts}

@app.post("/posts", status_code = status.HTTP_200_OK)
def create_posts(post:Post):
    # %s, %s, %s are for data sanetization 
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ", (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()
    conn.commit()

    return {"Data": new_post}

@app.post("/posts/{id}")
def get_post_by_id(id:int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    fetched_post = cursor.fetchone()
    
    if not fetched_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id : {id} not found")
    return {"Data": fetched_post}

@app.delete("/posts/{id}")
def delete_post(id:int):
    cursor.execute("DELETE FROM posts WHERE id = %s returning * ", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id : {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id : {id} not found")

    return {"Data" : updated_post}