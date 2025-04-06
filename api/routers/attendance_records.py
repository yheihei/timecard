from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.app_services.clock_in.create_clock_in_app_service import \
    CreateClockInAppService
from api.auth.auth_api import get_current_user
from api.db import get_db
from api.domain.models.attendance_record.attendance_time import AttendanceTime
from api.domain.models.user.user import User
from api.domain.services.clock_in.clock_in_service import ClockInService
from api.domain.services.clock_in.exceptions import AlreadyClockedInError
from api.infrastructure.sqlalchemy.clock_in.clock_in_repository import \
    ClockInRepository
from api.models import User as UserModel
from api.schemas.attendance_records import CreateUserAttendanceRecord
from api.utils.custom_datetime import now

router = APIRouter()

@router.post("/clock_in", response_model=None)
async def create_user_attendance_records(body: CreateUserAttendanceRecord, db: AsyncSession = Depends(get_db), user: UserModel = Depends(get_current_user)):
    try:
        await CreateClockInAppService(
            ClockInService(ClockInRepository(db))
        ).execute(
            user=User(
                id=user.id,
                user_name=user.username,
                display_name=user.username,
            ),
            attendance_time=AttendanceTime(now())
        )
    except AlreadyClockedInError:
        raise HTTPException(
            status_code=400,
            detail=f"2連続で{body.type.value}はできません",
        )
    return None