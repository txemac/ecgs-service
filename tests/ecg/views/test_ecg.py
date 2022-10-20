from typing import Dict

from starlette import status
from starlette.testclient import TestClient


def test_ecg_create_ok(
        client: TestClient,
        new_ecg_data: Dict,
) -> None:
    response = client.post(
        url="/ecgs",
        json=new_ecg_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("id") is not None
