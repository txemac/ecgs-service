import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlmodel import Session
from starlette import status

from api import messages
from api.database import db_sql_session
from api.depends import get_user_repository
from api.user.application.get_current_user import get_current_user
from api.user.application.password_hash import get_password_hash
from api.user.domain.user import User
from api.user.domain.user import UserCreate
from api.user.domain.user import UserID
from api.user.domain.user_repository import UserRepository

logger = logging.getLogger(__name__)

users_router = APIRouter()


@users_router.post(
    path="",
    name="Create",
    description="Create a new user. Only for admins.",
    status_code=status.HTTP_201_CREATED,
    response_model=UserID,
    responses={
        400: {"description": messages.EMAIL_INVALID},
        401: {"description": messages.USER_NOT_CREDENTIALS},
        403: {"description": messages.USER_NOT_PERMISSION},
    },
)
def create(
        payload: UserCreate,
        db_sql: Session = Depends(db_sql_session),
        user_repository: UserRepository = Depends(get_user_repository),
) -> UserID:
    logger.info(f"POST User. Payload: {payload.dict()}")

    if user_repository.get_by_email(db_sql, email=payload.email):
        logger.exception(messages.EMAIL_INVALID)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.EMAIL_INVALID)

    payload.password = get_password_hash(password=payload.password)

    new_user = user_repository.create(db_sql, new_user=payload)
    if not new_user:
        logger.exception(messages.USER_CREATE_ERROR)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.USER_CREATE_ERROR)

    return UserID(id=new_user.id)


@users_router.get(
    path="/me",
    name="Get me",
    description="Get info about the current authenticated user.",
    status_code=status.HTTP_200_OK,
    response_model=User,
    responses={
        401: {"description": messages.USER_NOT_CREDENTIALS},
        403: {"description": messages.USER_NOT_PERMISSION},
    },
)
def get_me(
        db_sql: Session = Depends(db_sql_session),
        current_user: User = Depends(get_current_user),
) -> User:
    logger.info(f"GET User me. Current user: {current_user.id}")
    return current_user
