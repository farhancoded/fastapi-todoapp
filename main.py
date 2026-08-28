from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import session
from pydantic import BaseModel,Field
import models
from models import Todos,users
from typing import Annotated
from database import engine,SessionLocal
from fastapi.responses import JSONResponse
from typing import Optional
from router import auth,admin
from router.auth import get_current_user


app=FastAPI()


class Todo(BaseModel):
    id : int
    title : str
    description : str = Field(max_length=100)
    priority : int =Field(gt=0,lt=6)
    completed : bool


class Todoupdate(BaseModel):
    
    title : Optional[str]= Field(default=None)
    description :Optional[ str] = Field(default=None,max_length=100)
    priority : Optional[int] =Field(default=None, gt=0,lt=6)
    completed : Optional[bool]= Field(default=None)



models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(admin.router)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency= Annotated[session,Depends(get_db)]
user_dependency= Annotated[dict,Depends(get_current_user)]


@app.get('/')
def read_todos(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='failed authentication')

    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@app.get('/todo/{todo_id}')
def read_specific_todos(user: user_dependency, db: db_dependency, todo_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail='failed authentication')

    specific_todo = db.query(Todos).filter(
        Todos.owner_id == user.get("id"),
        Todos.id == todo_id
    ).first()

    if specific_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return specific_todo


@app.post("/create/")
def create_todos(
    user: user_dependency,
    db: db_dependency,
    new_todo: Todo
):
    if user is None:
        raise HTTPException(status_code=401, detail="Failed authentication")

    todo = Todos(
        **new_todo.model_dump(),
        owner_id=user.get("id")
    )

    db.add(todo)
    db.commit()

    return {"message": "Todo created successfully"}


@app.put("/todo/{todo_id}")
def update_user(
    todo_id: int,
    user: user_dependency,
    db: db_dependency,
    update_todo: Todoupdate
):
    if user is None:
        raise HTTPException(status_code=401, detail="Failed authentication")

    todo = db.query(Todos).filter(
        Todos.id == todo_id,
        Todos.owner_id == user.get("id")
    ).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = update_todo.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)

    return {"message": "Todo updated successfully"}


@app.get("/user")
def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Failed authentication")

    db_user = db.query(users).filter(
        users.id == user.get("id")
    ).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


