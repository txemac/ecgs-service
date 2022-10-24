from starlette import status
from starlette.testclient import TestClient

from api import messages
from api.user.application.create_access_token import create_access_token
from api.user.domain.user import User
from tests.utils import assert_dicts


def test_login_ok(
        client: TestClient,
        user_1: User,
) -> None:
    data = dict(
        username=user_1.email,
        password="12345678",
    )
    response = client.post(
        url="/login",
        data=data,
    )
    assert response.status_code == status.HTTP_200_OK
    expected = dict(
        access_token=create_access_token(email=user_1.email),
        token_type="bearer",
    )
    assert_dicts(original=response.json(), expected=expected)


def test_login_user_not_exists(
        client: TestClient,
) -> None:
    data = dict(
        username="non_exists@gmail.com",
        password="12345678",
    )
    response = client.post(
        url="/login",
        data=data,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == messages.USER_NOT_FOUND


def test_login_password_incorrect(
        client: TestClient,
        user_1: User,
) -> None:
    data = dict(
        username=user_1.email,
        password="wrong_password",
    )
    response = client.post(
        url="/login",
        data=data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == messages.USER_INCORRECT_USERNAME_PASSWORD


def test_logout_ok(
        client: TestClient,
        headers_user_1: str,
) -> None:
    response = client.get(
        url="/logout",
        headers=headers_user_1,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("access_token") == ""


def test_logout_no_login(
        client: TestClient,
) -> None:
    response = client.get(
        url="/logout",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("access_token") == ""
