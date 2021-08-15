from typing import List
from .base import BlogBaseResponse, UserBaseResponse


class UserResponse(UserBaseResponse):
    blogs: List[BlogBaseResponse]

class UserTokenResponse(UserBaseResponse):
    access_token: str
    token_type:str = "bearer"

