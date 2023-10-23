from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import UserInDB, TodoInDB
from schemas import User, UserCreate, Todo, TodoCreate
import crud


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.post("/users/{username}/todos/", response_model=Todo)
def create_todos(user_name: str, todo: TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo, user_name=user_name)


@app.get("/users/{username}/todos/", response_model=List[Todo])
def read_user_todos(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, user_name=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    todos = crud.get_todos_by_user(db=db, username=username)
    return todos