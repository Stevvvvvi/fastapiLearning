from package.jwt import get_current_user
from package import routers
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..schemas.base import BlogRequest
from ..schemas.blog import BlogResponse
from ..models import Blog, User
from ..dependency import get_db

router=APIRouter(
    prefix="/blog",
    tags=["blog"]
)

@router.get('/', response_model=List[BlogResponse], status_code=status.HTTP_200_OK)
async def getBlogs(query:Optional[str]=None,db:Session=Depends(get_db),user: User = Depends(get_current_user)):
    if query:
        blogs:List[Blog]=db.query(Blog).filter(and_(Blog.owner_id==user.id, Blog.title.like(f'%{query}%'))).all()
    else:
        blogs:List[Blog]=db.query(Blog).filter(Blog.owner_id==user.id).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="does not have any blog")
    return blogs

@router.post('/', response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
async def createBlog(request:BlogRequest,db:Session=Depends(get_db),user: User = Depends(get_current_user)):
    newblog=Blog(**request.dict(), owner_id=user.id)
    db.add(newblog)
    db.commit()
    db.refresh(newblog)
    if not newblog:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail="create blog failed")
    return newblog

@router.get('/{id}', response_model=BlogResponse, status_code=status.HTTP_200_OK)
async def getBlog(id:int,db:Session=Depends(get_db),user: User = Depends(get_current_user)):
    blog:Blog=db.query(Blog).filter(and_(Blog.owner_id==user.id, Blog.id==id)).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="does not have this blog")
    return blog

@router.put('/{id}', response_model=BlogResponse, status_code=status.HTTP_200_OK)
async def updateBlog(id:int,request:BlogRequest,db:Session=Depends(get_db),user: User = Depends(get_current_user)):
    blogQ=db.query(Blog).filter(and_(Blog.owner_id==user.id, Blog.id==id))

    if not blogQ.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="does not have this blog")
    blogQ.update(request.dict())
    db.commit()
    return blogQ.first()

@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def deleteBlog(id:int,db:Session=Depends(get_db),user: User = Depends(get_current_user)):
    blogQ=db.query(Blog).filter(and_(Blog.owner_id==user.id, Blog.id==id))
    if not blogQ.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="does not have this blog")
    blogQ.delete()
    db.commit()
    return {"message":f"succesfully deleted blog {id}"}