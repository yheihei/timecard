from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.done as done_crud
import api.schemas.done as done_schema
from api.db import get_db
from api.ddd.application_service import DoneCreateApplicationService
from api.ddd.repository import DoneRepository

router = APIRouter()


@router.put("/tasks/{task_id}/done", response_model=done_schema.DoneResponse)
async def mark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):
    # done = await done_crud.get_done(db, task_id=task_id)
    # if done is not None:
    #     raise HTTPException(status_code=400, detail="Done already exists")

    # return await done_crud.create_done(db, task_id)
    repository = DoneRepository(db)
    await DoneCreateApplicationService(repository).register(task_id)
    return done_schema.DoneResponse(id=task_id)


@router.delete("/tasks/{task_id}/done", response_model=None)
async def unmark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):
    done = await done_crud.get_done(db, task_id=task_id)
    if done is None:
        raise HTTPException(status_code=404, detail="Done not found")

    return await done_crud.delete_done(db, done)
