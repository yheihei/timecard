from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.auth_api import get_current_user
from api.db import get_db
from api.models import User
from api.models.attendance_record import AttendanceRecord
from api.schemas.user_attendance_records import CreateUserAttendanceRecord
from api.utils.custom_datetime import now

router = APIRouter()

@router.post("/attendance-records", response_model=None)
async def create_user_attendance_records(body: CreateUserAttendanceRecord, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    current = now()
    # AttendanceRecordのうち、その日の開始時点から現在までの間に打刻されたものの最新を取得
    query = await db.execute(
        select(AttendanceRecord).where(
            AttendanceRecord.user_id == user.id,
            AttendanceRecord.timestamp >= current.replace(hour=0, minute=0, second=0, microsecond=0),
            AttendanceRecord.timestamp <= current,
        ).order_by(AttendanceRecord.timestamp.desc())
    )

    # 2連続で出勤打刻または退勤打刻を行うことはできない
    existance_last_record = query.scalars().first()
    if existance_last_record and existance_last_record.type == body.type:
        raise HTTPException(
            status_code=400,
            detail=f"2連続で{body.type.value}はできません",
        )

    record = AttendanceRecord(
        user_id=user.id,
        type=body.type,
        timestamp=now(),
    )
    db.add(record)
    await db.commit()
    return None
