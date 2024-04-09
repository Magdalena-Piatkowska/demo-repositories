from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

from pydantic import UUID4, BaseModel
from sqlalchemy.exc import IntegrityError

from app.adapter.db.db_connection import SQLALchemyDBConnection
from app.ports.repository import Repository

from .model.base import BaseSQLModel

ModelDTOType = Type[BaseModel]
ModelDTO = TypeVar("ModelDTO", bound=BaseModel)
FilterType = Optional[Union[Dict, Callable]]

logger = logging.getLogger(__name__)


class RecordNotFound(Exception):
    pass


class DBIntegrityError(Exception):
    pass


class SQLRepository(Repository):
    model: Any = BaseSQLModel
    model_dto: ModelDTOType = BaseModel

    def __init__(self, db: SQLALchemyDBConnection):
        self.db: SQLALchemyDBConnection = db

    def create(self, obj_in: BaseModel, **kwargs) -> BaseModel:
        db_obj = self.model(**obj_in.model_dump())
        try:
            self.db.session.add(db_obj)
            self.db.session.commit()
        except IntegrityError as err:
            logger.warning(
                f"DB integrity Error creating: {self.__class__.__name__}, er: {err}"
            )
            self.db.rollback()
            raise DBIntegrityError(err.orig)
        self.db.session.refresh(db_obj)
        return self._model_to_dto(db_obj)

    def read(self, id: UUID4, **kwargs) -> BaseModel:
        query = self.db.session.query(self.model).filter(self.model.id == id)
        entity = query.first()
        if not entity:
            raise RecordNotFound(
                f"Model: {self.model.__name__}, Record: {id}, not found"
            )
        return self._model_to_dto(entity)

    def read_multi(self, filters: Optional[dict] = None, **kwargs) -> List[BaseModel]:
        query = self.db.session.query(self.model)
        if filters:
            query = query.filter_by(**filters)
        results = [self._model_to_dto(db_object) for db_object in query]
        return results

    def _model_to_dto(self, db_object):
        return self.model_dto(**db_object.__dict__)
