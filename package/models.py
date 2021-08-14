from sqlalchemy import Column, String, Integer, Boolean
from .db import Base

class Blog(Base):
    __tablename__= "blog"
    id= Column(Integer, primary_key=True, index=True, unique=True)
    title= Column(String, index=True)
    content= Column(String)
    description= Column(String)
    is_deleted= Column(Boolean, default=False)

