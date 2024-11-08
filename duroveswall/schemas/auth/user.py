from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    dt_created: datetime
    dt_updated: datetime

    class Config:
        from_attributes = True
