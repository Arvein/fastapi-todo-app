from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4

app = FastAPI()
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

# Если хотите, чтобы корневой URL отдавал index.html
@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Task(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

db: dict[UUID, Task] = {}

def find_task_by_id(task_id: UUID):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Task not found")
    return db[task_id]

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return list(db.values())

@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: Task):
    task.id = uuid4()
    db[task.id] = task
    return task

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: UUID):
    return find_task_by_id(task_id)

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: UUID, updated_task: Task):
    task = find_task_by_id(task_id)
    updated_task.id = task_id
    db[task_id] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: UUID):
    find_task_by_id(task_id)
    del db[task_id]
    return None
