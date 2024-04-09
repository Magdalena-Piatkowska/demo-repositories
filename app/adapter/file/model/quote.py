from uuid import UUID, uuid4

from pydantic import BaseModel

from app.adapter.file.repository import JSONRepository
from app.domain.quote import QuoteDTO


class JSONQuoteRepository(JSONRepository):
    model_dto = QuoteDTO
    file_name = f"quote.json"

    def create(self, obj_in: BaseModel, **kwargs) -> QuoteDTO:
        quote_id: UUID = kwargs.get("quote_id", None)
        quote_id = quote_id if quote_id else uuid4()

        obj_in = self.model_dto(**obj_in.model_dump())
        obj_in.id = quote_id

        file_path = self._get_file_path(quote_id=quote_id, file_name=self.file_name)

        json_data: str = obj_in.model_dump_json()
        self.storage.save(file_path, json_data)
        return obj_in
