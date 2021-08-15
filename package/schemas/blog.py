from .base import BlogBaseResponse, UserBaseResponse

    
class BlogResponse(BlogBaseResponse):
    creator: UserBaseResponse
    owner_id: int

