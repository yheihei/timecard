from pydantic import BaseModel, Field


class CreateUserAttendanceRecord(BaseModel):
    type: str = Field(None, example="clock_in")
