import logging
from typing import Optional

from pydantic import EmailStr
from pydantic import UUID4
from sqlmodel import Session

from api.user.domain.user import User
from api.user.domain.user import UserCreate
from api.user.domain.user_repository import UserRepository

logger = logging.getLogger(__name__)


class SQLModelUserRepository(UserRepository):

    @staticmethod
    def count(
            db_sql: Session,
    ) -> int:
        result = db_sql.query(User).count()
        logger.info(f"SQL query count to User with result {result}")
        return result

    @staticmethod
    def create(
            db_sql: Session,
            new_user: UserCreate,
    ) -> User:
        user = User.from_orm(new_user)
        db_sql.add(user)
        db_sql.commit()
        db_sql.refresh(user)
        logger.info(f"SQL query add new user with ID {user.id}")
        return user

    @staticmethod
    def get_by_id(
            db_sql: Session,
            user_id: UUID4,
    ) -> Optional[User]:
        logger.info(f"SQL query get user with ID {user_id}")
        return db_sql.get(User, user_id)

    @staticmethod
    def get_by_email(
            db_sql: Session,
            email: EmailStr,
    ) -> Optional[User]:
        logger.info(f"SQL query get user with email {email}")
        return db_sql.query(User).where(User.email == email).first()
