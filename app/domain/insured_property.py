from typing import Optional
from uuid import UUID

from pydantic import BaseModel, NonNegativeFloat


class BaseInsuredPropertyDTO(BaseModel):
    quote_id: Optional[UUID] = None
    street_name: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    occupancy: str
    tiv: NonNegativeFloat = 0.0


class InsuredPropertyDTO(BaseInsuredPropertyDTO):
    id: Optional[UUID] = None
