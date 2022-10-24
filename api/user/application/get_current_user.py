import logging

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import jwt
from pydantic import ValidationError
from sqlmodel import Session
from starlette import status

from api import messages
from api.database import db_sql_session
from api.depends import get_user_repository
from api.settings import API_SECRET_KEY
from api.settings import AUTH_ACCESS_TOKEN_ALGORITHM
from api.user.domain.auth import AuthTokenPayload
from api.user.domain.user import User
from api.user.domain.user_repository import UserRepository

logger = logging.getLogger(__name__)

oauth2_scheme_pwd_bearer = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
        db_sql: Session = Depends(db_sql_session),
        user_repository: UserRepository = Depends(get_user_repository),
        token: str = Depends(oauth2_scheme_pwd_bearer),
) -> User:
    """
    Get current user.

    :param db_sql: database SQL session
    :param user_repository: user service
    :param token: access token
    :raise: HTTPException user nor found or without credentials
    :raise: HTTPException user without credentials
    :return: user
    """
    try:
        payload = jwt.decode(token, API_SECRET_KEY, algorithms=[AUTH_ACCESS_TOKEN_ALGORITHM])
        token_data = AuthTokenPayload(**payload)
    except (JWTError, ValidationError) as e:
        logger.exception(str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.USER_NOT_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_db = user_repository.get_by_email(db_sql, email=token_data.sub)
    if not user_db:
        logger.exception(messages.USER_NOT_FOUND)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND)
    return user_db
