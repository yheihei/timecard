from pydantic import BaseModel, Field

from api.models.attendance_record import AttendanceType


class CreateUserAttendanceRecord(BaseModel):
    type: AttendanceType = Field(None, example="CLOCK_IN")
