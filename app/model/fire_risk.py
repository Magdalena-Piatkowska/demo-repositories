from typing import Optional
from uuid import UUID

from pydantic import BaseModel, NonNegativeFloat


class FireRiskDTO(BaseModel):
    quote_id: Optional[UUID] = None
    tiv: NonNegativeFloat = 0.0
    loss_cost: NonNegativeFloat = 0.0
