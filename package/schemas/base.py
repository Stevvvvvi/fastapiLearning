from typing import Optional
from pydantic import BaseModel

class UserRequest(BaseModel):
    email:str
    password:str

class UserBaseResponse(BaseModel):
    id:int
    email:str
    is_admin:bool
    class Config:
        orm_mode=True

    

class BlogRequest(BaseModel):
    title: str
    content: str
    description: Optional[str] = None

class BlogBaseResponse(BlogRequest):
    id: int
    class Config:
        orm_mode = True