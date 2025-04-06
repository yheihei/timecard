from pydantic import BaseModel, Field

from api.domain.models.attendance_record.i_attendance_record import \
    AttendanceType


class CreateUserAttendanceRecord(BaseModel):
    type: AttendanceType = Field(None, example="CLOCK_IN")
