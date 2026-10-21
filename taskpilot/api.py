from typing import Literal, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from taskpilot import auth, cli, storage

app = FastAPI(title="TaskPilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

bearer = HTTPBearer(auto_error=False)


def current_user_id(creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer)):
    if creds is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = auth.decode_token(creds.credentials)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_id


class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=6, max_length=100)


class TaskIn(BaseModel):
    title: str = Field(min_length=1)
    priority: Literal["low", "medium", "high"] = "medium"
    due: Optional[str] = None


class DoneUpdate(BaseModel):
    done: bool


@app.post("/register", status_code=201)
def register(c: Credentials):
    username = c.username.strip().lower()
    user_id = storage.create_user(username, auth.hash_password(c.password))
    if user_id is None:
        raise HTTPException(status_code=409, detail="Username already taken")
    return {"token": auth.create_token(user_id), "username": username}


@app.post("/login")
def login(c: Credentials):
    username = c.username.strip().lower()
    user = storage.get_user(username)
    if not user or not auth.verify_password(c.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"token": auth.create_token(user["id"]), "username": username}


@app.get("/tasks")
def get_tasks(
    status: Optional[Literal["done", "pending"]] = None,
    search: Optional[str] = None,
    user_id: int = Depends(current_user_id),
):
    return cli.list_tasks(status, search, user_id)


@app.post("/tasks", status_code=201)
def create_task(task: TaskIn, user_id: int = Depends(current_user_id)):
    return cli.add_task(task.title, task.priority, task.due, user_id)


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, body: DoneUpdate, user_id: int = Depends(current_user_id)):
    if not storage.set_done(task_id, body.done, user_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task_id, "done": body.done}


@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: int, user_id: int = Depends(current_user_id)):
    if not cli.delete_task(task_id, user_id):
        raise HTTPException(status_code=404, detail="Task not found")