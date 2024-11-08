from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from duroveswall.db import get_session
from duroveswall.schemas import RegistrationForm, RegistrationSuccess
from duroveswall.utils.user import register_user, authenticate_user


api_router = APIRouter(
    prefix="/user",
    tags=["User"],
)

security = HTTPBasic()

@api_router.post(
    "/authentication",
    status_code=status.HTTP_200_OK)
async def authentication(
    _:Request,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    session: AsyncSession = Depends(get_session),
): 
    user = await authenticate_user(session, credentials.username, credentials.password)
    if not user:
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


@api_router.post(
    "/registration",
    status_code=status.HTTP_201_CREATED,
    response_model=RegistrationSuccess,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad parameters for registration",
        },
    },
)
async def registration(
    _: Request,
    registration_form: RegistrationForm = Body(...),
    session: AsyncSession = Depends(get_session),
):
    is_success, message = await register_user(session, registration_form)
    if is_success:
        return {"message": message}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message,
    )

@api_router.get(
    "/me",
    status_code=status.HTTP_200_OK)
async def get_me():
    # FIXME: your code here
    pass


@api_router.delete(
    "/delete",
    status_code=status.HTTP_204_NO_CONTENT)
async def delete():
    # FIXME: your code here
    pass
