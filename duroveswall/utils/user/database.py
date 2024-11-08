from sqlalchemy import delete, exc, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from duroveswall.models import User
from duroveswall.schemas import RegistrationForm


async def get_user(session: AsyncSession, username: str) -> User | None:
    query = select(User).where(
        and_(User.username == username)
    )
    return await session.scalar(query)


async def register_user(session: AsyncSession, potential_user: RegistrationForm) -> tuple[bool, str]:
    user = User(**potential_user.model_dump(exclude_unset=True))
    session.add(user)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False, "Username already exists."
    return True, "Successful registration!"


async def delete_user(session: AsyncSession, user: User) -> None:
    query = delete(User).where(
        and_(User.username == user.username)
    )
    await session.execute(query)
    await session.commit()
