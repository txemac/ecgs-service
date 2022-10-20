from starlette import status
from starlette.testclient import TestClient

from api.main import api
from tests.utils import assert_dicts


def test_health(
        client: TestClient,
) -> None:
    response = client.get(
        url="/health",
    )
    assert response.status_code == status.HTTP_200_OK
    expected = dict(
        message="OK",
        version=api.version,
        time="*",
    )
    assert_dicts(original=response.json(), expected=expected)
