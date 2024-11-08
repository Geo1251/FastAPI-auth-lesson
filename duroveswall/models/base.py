# pylint: disable=not-callable
import uuid
from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import TIMESTAMP, CHAR
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase

class BaseTable(DeclarativeBase):
    __abstract__ = True

    id = Column(
        CHAR(32),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        doc="Unique index of element (type UUID)",
    )
    dt_created = Column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
        doc="Date and time of create",
    )
    dt_updated = Column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
        doc="Date and time of last update",
    )
