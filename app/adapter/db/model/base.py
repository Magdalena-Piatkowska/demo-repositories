from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import UUIDType

Base = declarative_base()


class BaseSQLModel(Base):
    __abstract__ = True
    id = Column(UUIDType, primary_key=True, default=uuid4)  # type: ignore
