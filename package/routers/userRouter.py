from package.jwt import create_access_token, get_current_user
from ..models import User
from ..dependency import get_db
from sqlalchemy.orm.session import Session
from package.schemas.base import UserRequest
from ..schemas.user import UserResponse, UserTokenResponse
from fastapi import APIRouter, status, Depends, HTTPException
from ..hash import pwd_context
from fastapi.security import OAuth2PasswordRequestForm


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

@router.post('/login', response_model=UserTokenResponse, status_code=status.HTTP_200_OK)
async def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    checkUserExist=db.query(User).filter(User.email==request.username).first()
    if not checkUserExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cannot find the email, please register")
    verifyResult=pwd_context.verify(request.password,checkUserExist.password)
    print(f'result of verify user login detail{verifyResult}')
    if not verifyResult:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="password is not correct")
    token = create_access_token(data={"sub":checkUserExist.email})
    return {**checkUserExist.__dict__,"access_token":token}



@router.get('/', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def getUser(user: User = Depends(get_current_user)):
    return user