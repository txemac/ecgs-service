from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import jwt
from pydantic.networks import EmailStr

from api.settings import API_SECRET_KEY
from api.settings import AUTH_ACCESS_TOKEN_ALGORITHM
from api.settings import AUTH_TOKEN_EXPIRE_MINUTES


def create_access_token(
        email: EmailStr,
        expires_delta: timedelta = timedelta(minutes=AUTH_TOKEN_EXPIRE_MINUTES),
) -> str:
    """
    Create a new access token.

    :param email: email
    :param expires_delta: duration of the token valid
    :return: access token
    """
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = dict(exp=expire, sub=str(email))
    return jwt.encode(to_encode, API_SECRET_KEY, algorithm=AUTH_ACCESS_TOKEN_ALGORITHM)
