from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.task as task_crud
import api.schemas.task as task_schema
from api.db import get_db
from api.ddd.application_service import (TaskCreateApplicationService,
                                         TaskListGetApplicationService,
                                         TaskUpdateApplicationService)
from api.ddd.repository.task_repository import TaskRepository

router = APIRouter()


@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    tasks = await TaskListGetApplicationService(TaskRepository(db)).get()
    return [
        task_schema.Task(id=task.id.value(), title=task.title.value(), done=task.done)
        for task in tasks
    ]


@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)):
    repository = TaskRepository(db)
    task = await TaskCreateApplicationService(
        repository,
    ).register(task_body.title)
    return task_schema.TaskCreateResponse(id=task.id.value(), title=task.title.value())


@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(task_id: int, task_body: task_schema.TaskCreate,  db: AsyncSession = Depends(get_db)):
    repository = TaskRepository(db)
    task = await TaskUpdateApplicationService(repository).update(task_id, task_body.title)
    return task_schema.TaskCreateResponse(id=task.id.value(), title=task.title.value())


@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return await task_crud.delete_task(db, task)
