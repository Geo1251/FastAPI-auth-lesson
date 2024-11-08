# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
from starlette import status

UUID_DOES_NOT_EXIST = "00000000-1111-2222-3333-444444444444"


class TestEntryHandlersBase:
    @staticmethod
    def module_url() -> str:
        return "/entry"

    @staticmethod
    def get_url(entry_id: str) -> str:
        return f"{TestEntryHandlersBase.module_url()}/{entry_id}"

    @staticmethod
    def update_url(entry_id: str) -> str:
        return f"{TestEntryHandlersBase.module_url()}/{entry_id}"

    @staticmethod
    def list_url(username: str) -> str:
        return f"{TestEntryHandlersBase.module_url()}/list/{username}"

    @staticmethod
    def create_url() -> str:
        return f"{TestEntryHandlersBase.module_url()}"

    @staticmethod
    def delete_url(entry_id: str) -> str:
        return f"{TestEntryHandlersBase.module_url()}/{entry_id}"


class TestGetHandler(TestEntryHandlersBase):
    async def test_base_scenario(self, client, authed_headers, another_authed_headers):
        data = {
            "content": "Наконец-то вернули стену.",
            "user_wall_username": "user2",
        }

        create_response = await client.post(url=self.create_url(), json=data, headers=authed_headers)
        assert create_response.status_code == status.HTTP_201_CREATED
        entry_uuid = create_response.json().get("id", "")
        assert entry_uuid != ""

        get_response = await client.get(url=self.get_url(entry_uuid))
        assert get_response.status_code == status.HTTP_200_OK
        assert create_response.json() == get_response.json()

    async def test_errors(self,  client):
        response = await client.get(url=self.get_url("not-a-uuid"))
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        response = await client.get(url=self.get_url(UUID_DOES_NOT_EXIST))
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestListHandler(TestEntryHandlersBase):
    async def test_base_scenario(self, client, authed_headers, another_authed_headers):
        data = {
            "content": "Наконец-то вернули стену.",
            "user_wall_username": "user2",
        }

        for i in range(3):
            create_response = await client.post(url=self.create_url(), json=data, headers=authed_headers)
            assert create_response.status_code == status.HTTP_201_CREATED

        list_response = await client.get(url=self.list_url("user2"))
        assert list_response.status_code == status.HTTP_200_OK
        assert len(list_response.json()) == 3
        for i in range(3):
            assert list_response.json()[i].get("content", "") == data["content"]

    async def test_blank_scenario(self, client, authed_headers, another_authed_headers):
        list_response = await client.get(url=self.list_url("user2"))
        assert list_response.status_code == status.HTTP_200_OK
        assert len(list_response.json()) == 0

    async def test_not_found(self, client):
        list_response = await client.get(url=self.list_url("user3"))
        assert list_response.status_code == status.HTTP_404_NOT_FOUND


class TestCreateHandler(TestEntryHandlersBase):
    async def test_base_scenario(self, client, authed_headers, another_authed_headers):
        data = {
            "content": "Наконец-то вернули стену.",
            "user_wall_username": "user2",
        }

        create_response = await client.post(url=self.create_url(), json=data, headers=authed_headers)
        assert create_response.status_code == status.HTTP_201_CREATED
        assert create_response.json().get("content", "") == data["content"]

    async def test_long_content(self,  client, authed_headers, another_authed_headers):
        data = {
            "content": "Привет, пользователь. Это я, твой единственный комментатор. "
                       "На протяжении многих лет я создавал иллюзию того, что "
                       "твою стену комментирует много людей. Но это был я. "
                       "Сейчас напишу это сообщение со всех аккаунтов.",
            "user_Wall_username": "user1",
        }
        response = await client.post(url=self.create_url(), json=data, headers=authed_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json().get("detail", [{}])[0].get("type") == "string_too_long"


class TestUpdateHandler(TestEntryHandlersBase):
    async def test_base_scenario(self, client, authed_headers, another_authed_headers, user2_wall_entry):
        data = {
            "content": "Опять стену убрали",
        }

        update_response = await client.post(url=self.update_url(user2_wall_entry), json=data, headers=authed_headers)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json().get("content") == data["content"]

        get_response = await client.get(url=self.get_url(user2_wall_entry))
        assert get_response.status_code == status.HTTP_200_OK
        assert update_response.json() == get_response.json()

    async def test_not_found(self, client, authed_headers, another_authed_headers):
        data = {
            "content": "Наконец-то вернули стену.",
        }

        update_response = await client.post(url=self.update_url(UUID_DOES_NOT_EXIST), json=data, headers=authed_headers)
        assert update_response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteHandler(TestEntryHandlersBase):
    async def test_base_scenario(self, client, authed_headers, another_authed_headers, user2_wall_entry):

        delete_response = await client.delete(url=self.delete_url(user2_wall_entry), headers=authed_headers)
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        get_response = await client.get(url=self.get_url(user2_wall_entry))
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    async def test_not_found(self, client, authed_headers, another_authed_headers):
        update_response = await client.delete(url=self.delete_url(UUID_DOES_NOT_EXIST), headers=authed_headers)
        assert update_response.status_code == status.HTTP_404_NOT_FOUND
