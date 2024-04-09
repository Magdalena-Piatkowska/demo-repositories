import json
from typing import List, Optional

from pydantic import BaseModel

from app.adapter.file.repository import JSONRepository
from app.domain.occupancy_rate import OccupancyRateDTO


class JSONOccupancyRateRepository(JSONRepository):
    """
    Deliberately violating Liskov's Substitution Principle
    by removing the 'quote_id' parameter.

    This is just to remind that at the end of the day,
    design patterns exist to enable us, and sometimes
    it's okay to break them.
    """

    model_dto = OccupancyRateDTO
    file_name = f"occupancy_rate_list.json"

    def read_multi(self, filters: Optional[dict] = None, **kwargs) -> List[model_dto]:  # type: ignore
        file_path: str = self._get_file_path(file_name=self.file_name)

        results: List[BaseModel] = []
        with self.storage.load(file_path) as json_file:
            parsed_json = json.load(json_file)
            for content in parsed_json:
                results.append(self.model_dto(**content))
        return results

    def _get_file_path(self, file_name: str) -> str:  # type: ignore
        return f"{file_name}"
