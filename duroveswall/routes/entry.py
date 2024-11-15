from typing import List, Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Request, Response
from fastapi.security import HTTPBasicCredentials
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import current_user
from starlette import status

from duroveswall.db import get_session
from duroveswall.schemas import Entry as EntrySchema
from duroveswall.schemas import EntryCreateRequest, EntryUpdateRequest
from duroveswall.utils import entry as utils
from duroveswall.utils import user as user_utils
from duroveswall.utils.user import authenticate_user, get_current_user
from duroveswall.models import User

api_router = APIRouter(
    prefix="/entry",
    tags=["Entry"],
)

@api_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=EntrySchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Could not find user's wall",
        },
    },
)
async def create(
    _: Request,
    entry_instance: EntryCreateRequest = Body(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    user_wall = await user_utils.get_user(session, entry_instance.user_wall_username)
    if user_wall:
        return await utils.create_entry(session, current_user, user_wall.id, entry_instance)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User with this username not found",
    )


@api_router.get(
    "/{entry_id}",
    status_code=status.HTTP_200_OK,
    response_model=EntrySchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Entry with this id not found",
        },
    },
)
async def get(
    _: Request,
    entry_id: UUID4 = Path(...),
    session: AsyncSession = Depends(get_session),
):
    entry = await utils.get_entry(session, entry_id)
    if entry:
        return EntrySchema.model_validate(entry)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Entry with this id not found",
    )


@api_router.post(
    "/{entry_id}",
    status_code=status.HTTP_200_OK,
    response_model=EntrySchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Entry with this id not found",
        },
    },
)
async def update(
    _: Request,
    entry_id: UUID4 = Path(...),
    entry_content: EntryUpdateRequest = Body(...),
    session: AsyncSession = Depends(get_session),
):
    # FIXME: your code here
    entry = await utils.update_entry(session, entry_id, entry_content)
    if entry:
        return EntrySchema.model_validate(entry)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Entry with this id not found",
    )


@api_router.delete(
    "/{entry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Entry with this id not found",
        },
    },
)
async def delete(
    _: Request,
    entry_id: UUID4 = Path(...),
    session: AsyncSession = Depends(get_session),
):
    # FIXME: your code here
    success = await utils.delete_entry(session, entry_id)
    if success:
        return None
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Entry with this id not found",
    )


@api_router.get(
    "/list/{user_wall_username}",
    status_code=status.HTTP_200_OK,
    response_model=List[EntrySchema],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Could not find user's wall",
        },
    },
)
async def list_wall(
    _: Request,
    user_wall_username: str = Path(...),
    session: AsyncSession = Depends(get_session),
):
    user = await user_utils.get_user(session, user_wall_username)
    if user:
        return await utils.list_entries(session, user.id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User with this username not found",
    )
