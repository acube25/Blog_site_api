from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass 

class CommentUpdate(CommentBase):
    content: Optional[str]

class CommentResponse(CommentBase):
    id: int
    author_id: int
    post_id: int
    created_at: datetime


    class Config:
        from_attributes = True 

class PaginatedComments(BaseModel):
    total: int
    comments: List[CommentResponse]