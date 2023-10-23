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





