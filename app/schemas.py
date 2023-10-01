from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

# Schema from Pydantic
class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr

# Return Schema
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0)

class PostOut(BaseModel):
    Post: Post
    total_likes: int
