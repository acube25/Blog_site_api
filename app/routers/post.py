from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.database import get_db
from app.models.post import Post
from app.schemas.post import PostCreate, PostResponse, PostUpdate, PaginatedPost
from app.core.security import verify_token
from app.routers.auth import get_current_user
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.post("/", response_model=PostResponse)
def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    new_post = Post(author_id=current_user, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/all", response_model=List[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.get("/", response_model=PaginatedPost)
def get_posts(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=50)
):
    skip = (page - 1) * page_size
    total_posts = db.query(func.count(Post.id)).scalar()
    
    posts = db.query(Post).offset(skip).limit(page_size).all()

    return {"total": total_posts, "posts": posts}


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int, 
    post_data: PostUpdate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post: 
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.author_id != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
    post.title = post_data.title
    post.content = post_data.content
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}")
def delete_post(
    post_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    post_query = db.query(Post).filter(Post.id == post_id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.author_id != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    post_query.delete(synchronize_session = False)
    db.commit()
    return {"message": "post delete successfully"}