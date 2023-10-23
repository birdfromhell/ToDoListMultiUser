from sqlalchemy.orm import Session
from models import UserInDB, TodoInDB
from schemas import UserCreate, TodoCreate
from sqlalchemy.exc import IntegrityError

def get_user_by_name(db: Session, name: str):
    try:
        query = db.query(UserInDB).filter(UserInDB.name == name)
        result = query.first()
        if result is None:
            return "User not found."
        return result
    except Exception as e:
        return str(e)


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)  # Implement this function
    db_user = UserInDB(name=user.name, password=hashed_password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        return "User already exists."
    except Exception as e:
        return str(e)


def create_todo(db: Session, todo: TodoCreate, user_name: str):
    db_todo = TodoInDB(**todo.dict(), owner=user_name)
    try:
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except IntegrityError:
        db.rollback()
        return "Todo already exists."
    except Exception as e:
        return str(e)


def get_todos_by_user(db: Session, username: str):
    try:
        query = db.query(TodoInDB).filter(TodoInDB.owner == username).all()
        return query
    except Exception as e:
        return str(e)