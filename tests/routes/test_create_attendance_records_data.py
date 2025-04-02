from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from factory import Faker

from api.models.attendance_record import AttendanceRecord, AttendanceType


class AttendanceRecordFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = AttendanceRecord
        sqlalchemy_session_persistence = "commit"

    id = 1
    type = AttendanceType.CLOCK_IN
