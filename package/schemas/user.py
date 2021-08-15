from pydantic import BaseModel

class UserRequest(BaseModel):
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    email:str
    class Config:
        orm_mode=True