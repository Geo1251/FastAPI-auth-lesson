from duroveswall.config import get_settings
from .database import get_user
from sqlalchemy.ext.asyncio import AsyncSession
from duroveswall.config import get_settings
from duroveswall.models import User

async def authenticate_user (
    session: AsyncSession,
    username: str,
    password: str,
) -> User | None:
    user = await get_user(session, username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def verify_password(
    plain_password: str,
    hashed_password: str,
):
    pwd_context = get_settings().PWD_CONTEXT
    return pwd_context.verify(plain_password, hashed_password)