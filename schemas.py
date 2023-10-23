from pydantic import BaseModel
from typing import Optional, List


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    name: str
    todos: List[Todo] = []

    class Config:
        orm_mode = True