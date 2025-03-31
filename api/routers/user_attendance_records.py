from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.done as done_crud
import api.schemas.done as done_schema
from api.auth.auth_api import get_current_user, oauth2_scheme
from api.db import get_db
from api.ddd.application_service import DoneCreateApplicationService
from api.ddd.repository import DoneRepository
from api.models import User
from api.models.attendance_record import AttendanceRecord
from api.schemas.user_attendance_records import CreateUserAttendanceRecord
from api.utils.custom_datetime import now

router = APIRouter()

@router.post("/users/{user_id}/attendance-records", response_model=None)
async def create_user_attendance_records(body: CreateUserAttendanceRecord, user_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    record = AttendanceRecord(
        user_id=user_id,
        type=body.type,
        timestamp=now(),
    )
    db.add(record)
    await db.commit()
    return None
