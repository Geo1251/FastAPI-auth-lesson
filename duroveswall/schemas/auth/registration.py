from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from duroveswall.config import get_settings


class RegistrationForm(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None

    @field_validator("password")
    def validate_password(cls, password):
        settings = get_settings()
        password = settings.PWD_CONTEXT.hash(password)
        return password


class RegistrationSuccess(BaseModel):
    message: str
