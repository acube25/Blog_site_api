from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass 

class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PaginatedPost(BaseModel):
    total: int
    posts: List[PostResponse]

    