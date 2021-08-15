from pydantic import BaseModel

class UserRequest(BaseModel):
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    email:str
    is_admin:bool
    class Config:
        orm_mode=True
class UserTokenResponse(UserResponse):
    access_token: str
    token_type:str = "bearer"