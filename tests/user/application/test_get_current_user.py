import pytest
from fastapi import HTTPException
from sqlmodel import Session
from starlette import status

from api import messages
from api.user.application.create_access_token import create_access_token
from api.user.application.get_current_user import get_current_user
from api.user.domain.user import User
from api.user.domain.user_repository import UserRepository


def test_get_current_user_ok(
        db_sql: Session,
        user_repository: UserRepository,
        user_1: User,
) -> None:
    token = create_access_token(email=user_1.email)
    assert get_current_user(db_sql=db_sql, user_repository=user_repository, token=token) == user_1


def test_get_current_user_unauthorized(
        db_sql: Session,
        user_repository: UserRepository,
) -> None:
    with pytest.raises(HTTPException) as exception:
        get_current_user(db_sql=db_sql, user_repository=user_repository, token="token")
    assert exception.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exception.value.detail == messages.USER_NOT_CREDENTIALS
