from typing import List

from pydantic import UUID4
from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from duroveswall.models import Entry, User
from duroveswall.schemas import Entry as EntrySchema, EntryUpdateRequest
from duroveswall.schemas import EntryCreateRequest


async def create_entry(
    session: AsyncSession,
    author: User,
    user_wall_id: UUID4,
    entry_schema: EntryCreateRequest,
) -> EntrySchema:
    new_entry = Entry(
        content=entry_schema.content,
        user_wall_id=user_wall_id,
        author_id=author.id,
    )

    session.add(new_entry)
    await session.commit()
    await session.refresh(new_entry)

    return EntrySchema.model_validate(new_entry)


async def get_entry(
    session: AsyncSession,
    entry_id: UUID4,
) -> EntrySchema | None:
    get_entry_query = select(Entry).where(
        and_(
            Entry.id == str(entry_id),
        )
    )
    entry_from_base = await session.scalar(get_entry_query)
    if entry_from_base is None:
        return None
    return EntrySchema.model_validate(entry_from_base)


async def list_entries(
    session: AsyncSession,
    user_wall_id: UUID4,
) -> List[EntrySchema] | None:
    list_entries_query = select(Entry).where(
        and_(
            Entry.user_wall_id == str(user_wall_id),
        )
    )
    entries_from_base = await session.scalars(list_entries_query)
    if entries_from_base is None:
        return None
    return [EntrySchema.model_validate(entry_from_base) for entry_from_base in entries_from_base]


async def update_entry(
    session: AsyncSession,
    entry_id: UUID4,
    entry_schema: EntryUpdateRequest
) -> EntrySchema | None:
    update_entry_query = update(Entry).where(
        and_(
            Entry.id == str(entry_id),
        )
    ).values(content=entry_schema.content)

    res = await session.execute(update_entry_query)
    if not res.rowcount:
        await session.rollback()
        return None
    await session.commit()

    return await get_entry(session, entry_id)

async def delete_entry(
    session: AsyncSession,
    entry_id: UUID4,
) -> bool:
    delete_entry_query = delete(Entry).where(
        and_(
            Entry.id == str(entry_id),
        )
    )
    res = await session.execute(delete_entry_query)
    if not res.rowcount:
        await session.rollback()
        return False
    await session.commit()
    return True
