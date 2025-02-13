from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse, CommentUpdate, PaginatedComments
from app.routers.auth import get_current_user
from typing import List

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

@router.post("/", response_model=CommentResponse)
def create_comment(
    comment: CommentCreate, 
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    new_comment = Comment(author_id=current_user, post_id=post_id, **comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/{post_id}/all", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments

@router.get("/{post_id}", response_model=PaginatedComments)
def get_comments_paginated(
    post_id: int,
    db: Session = Depends(get_db),
    page: int = Query(1, alias="page", ge=1),
    page_size: int = Query(10, alias="page_size", le = 50)
):
    skip = (page - 1) * page_size
    total_comments = db.query(func.count(Comment.id)).filter(Comment.post_id == post_id).scalar()

    comments = db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(page_size).all()

    return {"total": total_comments, "comments": comments}


@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    update_comment: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.author_id != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
    
    db_comment.content = update_comment.content or db_comment.content
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.author_id != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    db.delete(db_comment)
    db.commit()
    return {"message": "Comment deleted successfully"}
