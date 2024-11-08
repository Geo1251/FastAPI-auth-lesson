# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=too-many-arguments
import os
from os import environ
from uuid import uuid4

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from duroveswall.__main__ import get_app
from duroveswall.config import get_settings
from duroveswall.db import SessionManager, init_models


@pytest.fixture(name="sqlite")
async def sqlite() -> str:
    """
    Создает временную БД для запуска теста.
    """
    settings = get_settings()

    tmp_name = ".".join([uuid4().hex, "pytest"])
    settings.DB_NAME = tmp_name
    environ["DB_NAME"] = tmp_name

    await init_models()
    try:
        yield settings.database_uri
    finally:
        os.remove(tmp_name)


@pytest.fixture(name="database")
async def database(sqlite, manager: SessionManager = SessionManager()) -> AsyncSession:
    """
    Returns a class object with which you can create a new session to connect to the database.
    """
    manager.refresh()  # без вызова метода изменения конфига внутри фикстуры sqlite не подтягиваются в класс
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        yield session


@pytest.fixture(name="client")
async def client(database, manager: SessionManager = SessionManager()) -> AsyncClient:
    """
    Returns a client that can be used to interact with the application.
    """
    app = get_app()
    manager.refresh()  # без вызова метода изменения конфига внутри фикстуры postgres не подтягиваются в класс
    # utils_module.check_website_exist = AsyncMock(return_value=(True, "Status code < 400"))
    yield AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


async def make_user(client, username, password, email=None):
    reg_data = {"username": username, "password": password, "email": email}
    reg_res = await client.post(url="/user/registration", json=reg_data)
    if reg_res.status_code != status.HTTP_201_CREATED:
        raise Exception(reg_res.status_code, reg_res.content)
    return username, password


@pytest.fixture(name="authed_headers")
async def authed_headers(client):
    # FIXME: your code here
    pass


@pytest.fixture(name="another_authed_headers")
async def another_authed_headers(client):
    # FIXME: your code here
    pass

@pytest.fixture(name="unused_authed_headers")
async def unused_authed_headers(client):
    # FIXME: your code here
    pass

@pytest.fixture(name="unauthed_headers")
async def unauthed_headers(client):
    yield {}

@pytest.fixture(name="user2_wall_entry")
async def user2_wall_entry(client, authed_headers):
    data = {
        "content": "Наконец-то вернули стену.",
        "user_wall_username": "user2",
    }

    create_response = await client.post(url="/entry", json=data, headers=authed_headers)
    yield create_response.json().get("id", "")
