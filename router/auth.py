from fastapi import FastAPI,APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from models import users
from datetime import timedelta,datetime,timezone
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Annotated,Optional
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import JWTError,jwt



router= APIRouter()

bcrypt_context= CryptContext(schemes=['bcrypt'],deprecated='auto')
OAuth2a_Bearer=OAuth2PasswordBearer(tokenUrl='/login')

import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")



class createusers(BaseModel):
    

    email : str
    username : str
    firstname : str
    lastname:str
    password:str
    role:str
    #phone_number:str

class updateuser(BaseModel):
    
    email : Optional[str]= Field(default=None)
    username :Optional[ str] = Field(default=None)
    firstname : Optional[str] =Field(default=None)
    lastname : Optional[str]= Field(default=None)
 #   phone_number : Optional[str]= Field(default=None)

class updatepassword(BaseModel):
    current_password:str
    new_password:str



def authenticate_user(username, password, db):
    user = db.query(users).filter(users.username == username).first()

    if user is None:
        return False

    if bcrypt_context.verify(password, user.hash_password):
        return user

    return False



def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):

    encode = {
        "sub": username,
        "user_id": user_id,
        "role": role
    }

    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)



def get_current_user(token: Annotated[str, Depends(OAuth2a_Bearer)]):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")
        user_id = payload.get("user_id")
        role = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Authentication failed"
            )

        return {
            "username": username,
            "id": user_id,
            "role": role
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed"
        )
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency= Annotated[dict,Depends(get_current_user)]



@router.post('/createuser')

def create_users(db :db_dependency, new_user:createusers):
    users_model=users(
        email =new_user.email,
        username=new_user.username,
        firstname= new_user.firstname,
        lastname=new_user.lastname,
        hash_password=bcrypt_context.hash(new_user.password),
        is_active=True,
        role=new_user.role,
       # phone_number=new_user.phone_number

    )
    db.add(users_model)
    db.commit()
    return JSONResponse(status_code=201, content={'massage' : 'user created siccussfully'})


@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
          db: db_dependency):

    user = authenticate_user(
        form_data.username,
        form_data.password,
        db
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    token = create_access_token(
        user.username,
        user.id,
        user.role,
        timedelta(minutes=30)
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
    

@router.put("/edituser")
def update_user(
    user: user_dependency,
    db: db_dependency,
   
    update_user: updateuser
):
    if user is None:
        raise HTTPException(status_code=401, detail="Failed authentication")

    user = db.query(users).filter(
        users.id == user.get("id")).first()

   

    update_data = update_user.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    

    return {"message": "user updated successfully"}



@router.put("/passwordchange")
def update_password(
    user: user_dependency,
    db: db_dependency,
   
    update_password: updatepassword
):
    if user is None:
        raise HTTPException(status_code=401, detail="Failed authentication")

    user = db.query(users).filter(
        users.id == user.get("id")).first()

   

    if not bcrypt_context.verify(update_password.current_password,user.hash_password):
        raise HTTPException(status_code=401,detail='wrong password')

    user.hash_password =bcrypt_context.hash(update_password.new_password)

    db.add(user)
    db.commit()
    

    return {"message": "password updated successfully"}
