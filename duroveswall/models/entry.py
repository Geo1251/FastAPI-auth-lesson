from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import TEXT, CHAR

from .base import BaseTable


class Entry(BaseTable):
    __tablename__ = "entry"

    content = Column(
        "content",
        TEXT,
        nullable=False,
        doc="Text content of the entry.",
    )
    author_id = Column(
        "author_id",
        CHAR(32),
        nullable=False,
        doc="Id of the user created the entry.",
    )
    user_wall_id = Column(
        "user_wall_id",
        CHAR(32),
        nullable=False,
        doc="Id of the user's entry which contains the entry.",
    )
