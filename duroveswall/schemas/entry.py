from datetime import datetime

from pydantic import UUID4, BaseModel, constr

MAX_ENTRY_CONTENT_LENGTH = 200


class Entry(BaseModel):
    id: UUID4
    content: str
    author_id: UUID4
    user_wall_id: UUID4
    dt_created: datetime
    dt_updated: datetime

    class Config:
        from_attributes = True


class EntryCreateRequest(BaseModel):
    content: constr(max_length=MAX_ENTRY_CONTENT_LENGTH)
    user_wall_username: str

    class Config:
        extra = 'forbid'

class EntryUpdateRequest(BaseModel):
    content: constr(max_length=MAX_ENTRY_CONTENT_LENGTH)

    class Config:
        extra = 'forbid'
