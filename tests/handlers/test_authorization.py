# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
import pytest
from starlette import status

from tests.handlers.test_entry import TestEntryHandlersBase


class TestAuthorization(TestEntryHandlersBase):
    @pytest.mark.parametrize(
        "headers, expected_status",
        (
            ('authed_headers', status.HTTP_200_OK),
            ('another_authed_headers', status.HTTP_200_OK),
            ('unused_authed_headers', status.HTTP_401_UNAUTHORIZED),
            ('unauthed_headers', status.HTTP_401_UNAUTHORIZED),
        ),
    )
    async def test_update_scenario(self, client, authed_headers, another_authed_headers, unused_authed_headers, user2_wall_entry, unauthed_headers, headers, expected_status, request):
        data = {
            "content": "Опять стену убрали"
        }
        response = await client.post(url=self.update_url(user2_wall_entry), json=data, headers=request.getfixturevalue(headers))
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "headers, expected_status",
        (
            ('authed_headers', status.HTTP_204_NO_CONTENT),
            ('another_authed_headers', status.HTTP_204_NO_CONTENT),
            ('unused_authed_headers', status.HTTP_401_UNAUTHORIZED),
            ('unauthed_headers', status.HTTP_401_UNAUTHORIZED),
        ),
    )
    async def test_delete_scenario(self, client, authed_headers, another_authed_headers, unused_authed_headers, user2_wall_entry, unauthed_headers, headers, expected_status, request):
        response = await client.delete(url=self.delete_url(user2_wall_entry), headers=request.getfixturevalue(headers))
        assert response.status_code == expected_status
