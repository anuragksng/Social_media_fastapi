import models, schemas
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from database import get_db 
from schemas import PostBase, UserCreate, UserOut
import hashlib
from typing import List
import oauth
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), limit:int = 40, skip:int=0, search:Optional[str]=""):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results
 
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:PostBase, db: Session = Depends(get_db), get_current_user_id: int = Depends(oauth.get_current_user)):
    # %s, %s, %s are for data sanetization 
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published) -> This similar things can be done as 
    new_post = models.Post(owner_id=get_current_user_id.id, **post.model_dump()) #whoever the user is logged in, takes their user id and make it as owner id, means who ever is login -> post will crated by there id 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post_by_id(id:int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    # fetched_post = cursor.fetchone()

    fetched_post = db.query(models.Post).filter(models.Post.id == id).first()
    votes = (
        db.query(func.count(models.Votes.post_id))
        .filter(models.Votes.post_id == id)
        .scalar()
    )
    
    if not fetched_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id : {id} not found")
    
    print(fetched_post.owner_id)
    if fetched_post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authorized to perform this action")

    return {"Post": fetched_post, "votes": votes}

@router.delete("/{id}")
def delete_post(id:int, db: Session = Depends(get_db), get_current_user_id: int = Depends(oauth.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s returning * ", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_to_be_deleted = db.query(models.Post).filter(models.Post.id == id) #seaching post by id

    if post_to_be_deleted.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id : {id} not found")
    
    if post_to_be_deleted.first().owner_id != get_current_user_id.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authorized to perform this action")
    
    post_to_be_deleted.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.CreatePost, db: Session = Depends(get_db), get_current_user_id: int = Depends(oauth.get_current_user)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id : {id} not found")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()