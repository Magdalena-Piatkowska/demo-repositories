from typing import Optional
from uuid import UUID

from pydantic import BaseModel, NonNegativeFloat
from sqlalchemy import Column, Float, String

from .base import BaseSQLModel


class BaseOccupancyRateDTO(BaseModel):
    occupancy: str
    rate: NonNegativeFloat


class OccupancyRateDTO(BaseOccupancyRateDTO):
    id: Optional[UUID] = None


class OccupancyRate(BaseSQLModel):
    __tablename__ = "occupancy_rate"
    __table_args__ = {"extend_existing": True}

    occupancy = Column(String(255), nullable=False, index=True)
    rate = Column(Float, nullable=False)
