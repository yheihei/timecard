from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr

from api.utils.custom_datetime import now


class TimestampMixin(object):
    """
    created_at, updated_atの共通化Mixin
    """

    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), default=now, nullable=True)

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime(timezone=True),
            default=now,
            onupdate=now,
            nullable=True,
        )
