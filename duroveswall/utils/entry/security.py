from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status 

from duroveswall.utils.entry import get_entry

async def authorize_user_edit(
    session: AsyncSession,
    user_id: UUID4,
    entry_id: UUID4,
) -> bool:
    entry = await get_entry(session, entry_id)
    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry with this id not found"
        )
    return user_id in (entry.user_wall_id, entry.author_id)