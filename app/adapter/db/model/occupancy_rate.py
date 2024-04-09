from sqlalchemy import Column, Float, String

from app.domain.occupancy_rate import OccupancyRateDTO

from ..repository import SQLRepository
from .base import BaseSQLModel


class OccupancyRate(BaseSQLModel):
    __tablename__ = "occupancy_rate"
    __table_args__ = {"extend_existing": True}

    occupancy = Column(String(255), nullable=False, index=True)
    rate = Column(Float, nullable=False)


class SQLOccupancyRateRepository(SQLRepository):
    model = OccupancyRate
    model_dto = OccupancyRateDTO
