from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response
from duroveswall.models import User
from duroveswall.schemas import User as UserSchema
from duroveswall.utils.user import register_user, authenticate_user, create_access_token, get_current_user, delete_user

from duroveswall.db import get_session
from duroveswall.schemas import RegistrationForm, RegistrationSuccess, Token
from duroveswall.utils.user import register_user, authenticate_user, create_access_token


api_router = APIRouter(
    prefix="/user",
    tags=["User"],
)

@api_router.post(
    "/authentication",
    status_code=status.HTTP_200_OK,
    response_model=Token,    
)
async def authentication(
    _:Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
): 
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub":user.username})
    return {"access_token": access_token, "token_type": "bearer"}


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
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def get_me(
    _:Request,
    current_user: User = Depends(get_current_user),
):
    return UserSchema.model_validate(current_user)


@api_router.delete(
    "/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def delete(
    _:Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    await delete_user(session, current_user)
   
