from package import routers
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .userRouter import asdf
from ..schemas.blog import BlogRequest, BlogResponse
from ..models import Blog
from ..dependency import get_db

router=APIRouter(
    prefix="/blog",
    tags=["blog"]
)

@router.get('/', response_model=List[BlogResponse], status_code=status.HTTP_200_OK)
async def getBlogs(query:Optional[str]=None,db:Session=Depends(get_db)):
    if query:
        blogs:List[Blog]=db.query(Blog).filter(Blog.title.like(f'%{query}%')).all()
    else:
        blogs:List[Blog]=db.query(Blog).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="does not have any blog")
    return blogs

@router.post('/', response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
async def createBlog(request:BlogRequest,db:Session=Depends(get_db)):
    newblog=Blog(**request.dict())
    db.add(newblog)
    db.commit()
    db.refresh(newblog)
    if not newblog:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail="create blog failed")
    return newblog

@router.get('/{id}', response_model=BlogResponse, status_code=status.HTTP_200_OK)
async def getBlog(id:int,db:Session=Depends(get_db)):
    blog:Blog=db.query(Blog).filter(Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="does not have this blog")
    return blog

@router.put('/{id}', response_model=BlogResponse, status_code=status.HTTP_200_OK)
async def updateBlog(id:int,request:BlogRequest,db:Session=Depends(get_db)):
    blogQ=db.query(Blog).filter(Blog.id==id)

    if not blogQ.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="does not have this blog")
    blogQ.update(request.dict())
    db.commit()
    return blogQ.first()

@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def deleteBlog(id:int,db:Session=Depends(get_db)):
    blogQ=db.query(Blog).filter(Blog.id==id)
    if not blogQ.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="does not have this blog")
    blogQ.delete()
    db.commit()
    return {"message":f"succesfully deleted blog {id}"}