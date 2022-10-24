import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlmodel import Session
from starlette import status

from api import messages
from api.database import db_sql_session
from api.depends import get_user_repository
from api.user.application.create_access_token import create_access_token
from api.user.application.password_hash import verify_password
from api.user.domain.auth import AuthToken
from api.user.domain.user_repository import UserRepository

logger = logging.getLogger(__name__)

auth_router = APIRouter()


@auth_router.post(
    path="/login",
    description="Generate a new access token.",
    status_code=status.HTTP_200_OK,
    response_model=AuthToken,
    responses={
        400: {"description": messages.USER_INCORRECT_USERNAME_PASSWORD},
        404: {"description": messages.USER_NOT_FOUND},
    },
)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db_sql: Session = Depends(db_sql_session),
        user_repository: UserRepository = Depends(get_user_repository),
) -> AuthToken:
    logger.info(f"POST login. Email: {form_data.username}")

    user_db = user_repository.get_by_email(db_sql, email=EmailStr(form_data.username))
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND)

    if not verify_password(plain_password=form_data.password, hashed_password=user_db.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.USER_INCORRECT_USERNAME_PASSWORD)

    access_token = create_access_token(email=user_db.email)
    return AuthToken(access_token=access_token, token_type="bearer")


@auth_router.get(
    path="/logout",
    description="Logout.",
    status_code=status.HTTP_200_OK,
    response_model=AuthToken,
)
def logout() -> AuthToken:
    logger.info("GET logout.")
    return AuthToken(access_token="", token_type="bearer")
