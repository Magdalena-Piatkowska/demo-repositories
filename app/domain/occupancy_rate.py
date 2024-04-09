from typing import Optional
from uuid import UUID

from pydantic import BaseModel, NonNegativeFloat


class BaseOccupancyRateDTO(BaseModel):
    occupancy: str
    rate: NonNegativeFloat


class OccupancyRateDTO(BaseOccupancyRateDTO):
    id: Optional[UUID] = None
