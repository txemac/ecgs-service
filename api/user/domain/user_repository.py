from abc import ABC
from abc import abstractmethod
from typing import Optional

from pydantic import EmailStr
from pydantic import UUID4
from sqlmodel import Session

from api.user.domain.user import User
from api.user.domain.user import UserCreate


class UserRepository(ABC):

    @staticmethod
    @abstractmethod
    def count(
            db_sql: Session,
    ) -> int:
        """
        Count the number of element in the user table.

        :param db_sql: session of the SQL database
        :return: number of users
        """
        pass

    @staticmethod
    @abstractmethod
    def create(
            db_sql: Session,
            new_user: UserCreate,
    ) -> Optional[User]:
        """
        Persist a new User.

        :param db_sql: session of the SQL database
        :param new_user: new User to persist
        :return: user if the record was created, None otherwise
        """
        pass

    @staticmethod
    @abstractmethod
    def get_by_id(
            db_sql: Session,
            user_id: UUID4,
    ) -> Optional[User]:
        """
        Searches for a persisted user by ID and returns it if it exists.

        :param db_sql: session of the SQL database
        :param user_id: user's ID
        :return: user if found, None otherwise
        """
        pass

    @staticmethod
    @abstractmethod
    def get_by_email(
            db_sql: Session,
            email: EmailStr,
    ) -> Optional[User]:
        """
        Searches for a persisted user by email "unique" and returns it if it exists.

        :param db_sql: session of the SQL database
        :param email: user's email
        :return: user if found, None otherwise
        """
        pass
