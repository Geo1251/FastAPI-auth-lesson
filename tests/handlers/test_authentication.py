# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
import pytest
from starlette import status


class TestRegistrationHandler:
    @staticmethod
    def get_url() -> str:
        return "/user/registration"

    @pytest.mark.parametrize(
        "username, password, email, expected",
        (
            ("user", "hackme", None, {"message": "Successful registration!"}),
            ("user2", "hackme", "test@example.com", {"message": "Successful registration!"}),
        ),
    )
    async def test_success(self, client, username, password, email, expected):
        data = {
            "username": username,
            "password": password,
            "email": email,
        }
        response = await client.post(url=self.get_url(), json=data)
        assert response.json() == expected

    @pytest.mark.parametrize(
        "username, password, email, expected_status",
        (
            ("user", "hackme2", None, status.HTTP_400_BAD_REQUEST),
            (None, "hackme", "test@example.com", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ),
    )
    async def test_error(self, client, username, password, email, expected_status):
        data = {
            "username": username,
            "password": password,
            "email": email,
        }
        response = await client.post(url=self.get_url(), json=data)

        if expected_status == status.HTTP_400_BAD_REQUEST:
            assert response.status_code == status.HTTP_201_CREATED
            response = await client.post(url=self.get_url(), json=data)

        assert response.status_code == expected_status


class TestAuthenticationHandler:
    @staticmethod
    def module_url() -> str:
        return "/user"

    @staticmethod
    def auth_url() -> str:
        return TestAuthenticationHandler.module_url() + "/authentication"

    @staticmethod
    def reg_url() -> str:
        return TestAuthenticationHandler.module_url() + "/registration"

    @staticmethod
    def me_url() -> str:
        return TestAuthenticationHandler.module_url() + "/me"

    @staticmethod
    def delete_url() -> str:
        return TestAuthenticationHandler.module_url() + "/delete"

    @pytest.mark.parametrize(
        "username, password",
        (("user", "hackme"),),
    )
    async def test_base_scenario(self, client, username, password):
        data = {
            "username": username,
            "password": password,
        }
        wrong_pass_data = {"username": username, "password": password + "abc"}
        wrong_user_data = {"username": username + "abc", "password": password}
        broken_data = {"username": username}
        reg_res = await client.post(url=self.reg_url(), json=data)
        assert reg_res.status_code == status.HTTP_201_CREATED
        assert reg_res.json() == {"message": "Successful registration!"}

        me_res = await client.get(url=self.me_url())
        assert me_res.status_code == status.HTTP_401_UNAUTHORIZED

        wrong_pass_auth = await client.post(url=self.auth_url(), data=wrong_pass_data)
        assert wrong_pass_auth.status_code == status.HTTP_401_UNAUTHORIZED

        wrong_user_auth = await client.post(url=self.auth_url(), data=wrong_user_data)
        assert wrong_user_auth.status_code == status.HTTP_401_UNAUTHORIZED

        broken_auth = await client.post(url=self.auth_url(), data=broken_data)
        assert broken_auth.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        me_res = await client.get(url=self.me_url())
        assert me_res.status_code == status.HTTP_401_UNAUTHORIZED

        true_auth = await client.post(url=self.auth_url(), data=data)
        assert true_auth.status_code == status.HTTP_200_OK
        assert "access_token" in true_auth.json() and "token_type" in true_auth.json()

        token = true_auth.json()["access_token"]

        me_res = await client.get(url=self.me_url(), headers={"Authorization": "Bearer " + token})
        assert me_res.status_code == status.HTTP_200_OK
        assert me_res.json().get("username", "") == username

        delete_res = await client.delete(url=self.delete_url(), headers={"Authorization": "Bearer " + token})
        assert delete_res.status_code == status.HTTP_204_NO_CONTENT

        me_res = await client.get(url=self.me_url(), headers={"Authorization": "Bearer " + token})
        assert me_res.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_unauthorized(self, client):
        me_res = await client.get(url=self.me_url())
        assert me_res.status_code == status.HTTP_401_UNAUTHORIZED

        delete_res = await client.delete(url=self.delete_url())
        assert delete_res.status_code == status.HTTP_401_UNAUTHORIZED
