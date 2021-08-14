from typing import Optional
from pydantic import BaseModel

class BlogRequest(BaseModel):
    title: str
    content: str
    description: Optional[str] = None

class BlogResponse(BlogRequest):
    id: int
    class Config:
        orm_mode = True

