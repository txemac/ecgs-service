from typing import Dict
from uuid import uuid4

from starlette import status
from starlette.testclient import TestClient

from api import messages
from api.ecg.domain.ecg import ECG
from tests.utils import assert_dicts


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


def test_ecg_get_one_ok(
        client: TestClient,
        ecg_1: ECG,
) -> None:
    response = client.get(
        url=f"/ecgs/{ecg_1.id}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert_dicts(original=response.json(), expected=ecg_1.dict())


def test_ecg_get_one_not_exists(
        client: TestClient,
) -> None:
    response = client.get(
        url=f"/ecgs/{uuid4()}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail") == messages.ECG_NOT_FOUND
