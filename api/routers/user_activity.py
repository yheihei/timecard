from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.done as done_crud
import api.schemas.done as done_schema
from api.auth.auth_api import get_current_user, oauth2_scheme
from api.db import get_db
from api.ddd.application_service import DoneCreateApplicationService
from api.ddd.repository import DoneRepository
from api.models import User

router = APIRouter()

@router.post("/users/{user_id}/activities", response_model=None)
async def create_user_activity(user_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return {"hello": "world"}
