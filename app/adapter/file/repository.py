import json
from typing import List, Optional, Type, TypeVar, Union, cast
from uuid import UUID

from pydantic import BaseModel

from app.ports.db_connection import DBConnection
from app.ports.repository import Repository
from app.ports.storage_connection import StorageConnection

ModelDTO = TypeVar("ModelDTO", bound=BaseModel)


class JSONRepository(Repository):
    model_dto: Type[BaseModel]
    file_name: str
    file_name_tmp: str

    def __init__(
        self,
        db: Optional[DBConnection] = None,
        storage: Optional[StorageConnection] = None,
    ):
        super().__init__(db, storage)
        assert self.storage
        self.storage: StorageConnection = cast(StorageConnection, storage)

    def create(
        self,
        obj_in: BaseModel,
        **kwargs,
    ) -> BaseModel:
        quote_id: UUID = kwargs.get("quote_id", None)
        quote_id = quote_id if quote_id else getattr(obj_in, "quote_id")
        assert quote_id

        file_path = self._get_file_path(quote_id=quote_id, file_name=self.file_name)

        json_data: str = obj_in.model_dump_json()
        self.storage.save(file_path, json_data)
        return obj_in

    def read(self, id: Union[UUID, None], **kwargs) -> BaseModel:
        quote_id: UUID = kwargs.get("quote_id", None)
        quote_id = id if id else quote_id
        file_path: str = self._get_file_path(
            quote_id=quote_id, file_name=self.file_name
        )

        assert quote_id
        with self.storage.load(file_path) as json_file:
            parsed_json = json.load(json_file)
            parsed_json = parsed_json[0] if type(parsed_json) == list else parsed_json
            obj = self.model_dto(**parsed_json)

        return obj

    def read_multi(self, filters: Optional[dict] = None, **kwargs) -> List[BaseModel]:
        quote_id = None
        if filters:
            quote_id = filters.get("quote_id", None)
        quote_id = quote_id if quote_id else kwargs.get("quote_id", None)

        assert quote_id
        file_path: str = self._get_file_path(
            quote_id=quote_id, file_name=self.file_name
        )

        results: List[BaseModel] = []
        with self.storage.load(file_path) as json_file:
            parsed_json = json.load(json_file)
            for content in parsed_json:
                results.append(self.model_dto(**content))

        return results

    def _get_file_path(self, quote_id: UUID, file_name: str) -> str:
        return f"{quote_id}/{file_name}"

    def _serialize_objects_to_json(
        self, list_models: List[BaseModel], exclude_unset: bool = False
    ) -> str:
        dict_list = []
        for obj in list_models:
            # pydantic->json->dict to ensure JSON serializable:
            json_obj = obj.model_dump_json(exclude_unset=exclude_unset)
            dict_obj: dict = json.loads(json_obj)
            dict_list.append(dict_obj)
        json_data: str = json.dumps(dict_list, indent=4)

        return json_data
