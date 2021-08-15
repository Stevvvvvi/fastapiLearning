from ..models import User
from ..dependency import get_db
from sqlalchemy.orm.session import Session
from package.schemas.user import UserRequest, UserResponse
from fastapi import APIRouter, status, Depends, HTTPException
from ..hash import pwd_context

asdf="asf"

router=APIRouter(
    prefix="/user",
    tags=['user']
)

@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def createUser(request:UserRequest,db:Session=Depends(get_db)):
    checkUserExist=db.query(User).filter(User.email==request.email).first()
    if checkUserExist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"the email {checkUserExist.email} has already registered")
    hashPassword=pwd_context.hash(request.password)
    newUser:User=User(email=request.email, password=hashPassword)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

@router.post('/login', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def login(request:UserRequest,db:Session=Depends(get_db)):
    checkUserExist=db.query(User).filter(User.email==request.email).first()
    if not checkUserExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cannot find the email, please register")
    verifyResult=pwd_context.verify(request.password,checkUserExist.password)
    if not verifyResult:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="password is not correct")

    return checkUserExist



@router.get('/', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def getUser(id:int,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cannot find the user or JWT expired")
    return user