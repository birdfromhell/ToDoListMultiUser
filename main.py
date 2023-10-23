from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

users = {}
todos = {}


class User(BaseModel):
    name: str
    password: str


class Todo(BaseModel):
    title: str
    description: str


@app.post("/users/", response_model=User)
def create_user(user: User):
    users[user.name] = user.password
    return user


@app.post("/users/{username}/todos/", response_model=Todo)
def create_todo_for_user(username: str, todo: Todo):
    if username not in todos:
        todos[username] = []
    todos[username].append(todo)
    return todo


@app.get("/users/{username}/todos/", response_model=List[Todo])
def read_todos_for_user(username: str):
    return todos.get(username, [])
