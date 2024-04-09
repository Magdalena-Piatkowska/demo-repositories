from uuid import UUID

from app.adapter.file.repository import JSONRepository
from app.domain.insured_property import InsuredPropertyDTO


class JSONInsuredPropertyRepository(JSONRepository):
    model_dto = InsuredPropertyDTO
    file_name = f"insured_property_list.json"
