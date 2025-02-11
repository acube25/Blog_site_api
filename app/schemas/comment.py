from pydantic import BaseModel
from typing import Optional

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

    class Config:
        from_attributes = True 

