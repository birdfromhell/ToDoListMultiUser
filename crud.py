from sqlalchemy.orm import Session
from models import UserInDB, TodoInDB
from schemas import UserCreate, TodoCreate


def get_user_by_name(db: Session, name: str):
    return db.query(UserInDB).filter(UserInDB.name == name).first()


def create_user(db: Session, user: UserCreate):
    db_user = UserInDB(name=user.name, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_todo(db: Session, todo: TodoCreate, user_name: str):
    db_todo = TodoInDB(**todo.dict(), owner=user_name)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos_by_user(db: Session, username: str):
    return db.query(TodoInDB).filter(TodoInDB.owner == username).all()