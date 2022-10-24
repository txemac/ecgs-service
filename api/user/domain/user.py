import logging
from datetime import datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import UUID4
from pydantic.types import constr
from sqlmodel import Field
from sqlmodel import SQLModel

logger = logging.getLogger(__name__)


class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=1) = Field(..., exclude=True)
    role: RoleEnum = RoleEnum.USER

    class Config:
        schema_extra = dict(
            example=dict(
                email="txema.bermudez@gmail.com",
                password="thebestpassword",
                role=RoleEnum.ADMIN,
            )
        )


class User(SQLModel, UserCreate, table=True):
    __tablename__ = "user"

    id: UUID4 = Field(default_factory=uuid4, primary_key=True, nullable=False)
    email: EmailStr = Field(unique=True, index=True)
    created_at: datetime = datetime.utcnow()

    def __str__(self):
        return str(self.email)

    class Config:
        orm_mode = True
        read_with_orm_mode = True
        schema_extra = dict(
            example=dict(
                id="eb75b926-8b44-4fae-a744-b3b3f96d98cd",
                email="txema.bermudez@gmail.com",
                role=RoleEnum.USER,
                created_at="2022-20-20 12:34:56",
            )
        )

    def is_admin(self) -> bool:
        """
        Check if a user is admin.

        :return: True if the user is admin
        """
        return self.role == RoleEnum.ADMIN


class UserID(BaseModel):
    id: UUID4

    class Config:
        schema_extra = dict(
            example=dict(
                id="eb75b926-8b44-4fae-a744-b3b3f96d98cd",
            )
        )
