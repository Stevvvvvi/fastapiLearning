from package.models import User
from package.dependency import get_db
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from fastapi import status, HTTPException, Depends
from dotenv import load_dotenv
from sqlalchemy.orm.session import Session
load_dotenv()

expires_time = timedelta(minutes=int(os.environ['ACCESS_TOKEN_EXPIRE_MINUTES']))
SECRET_KEY = os.environ['HASH_SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/login')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = expires_time):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(JWTtoken: str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        print(JWTtoken)
        print(JWTtoken)
        print('in try block')
        payload =jwt.decode(JWTtoken, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = db.query(User).filter(User.email==username).first()
        if user is None:
            raise credentials_exception
    except JWTError:
        print(JWTError)
        raise credentials_exception
    
    return user