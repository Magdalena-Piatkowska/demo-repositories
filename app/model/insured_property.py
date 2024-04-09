from typing import Optional
from uuid import UUID

from pydantic import BaseModel, NonNegativeFloat
from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from .base import BaseSQLModel


class BaseInsuredPropertyDTO(BaseModel):
    quote_id: Optional[UUID] = None
    street_name: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    occupancy: str
    tiv: NonNegativeFloat = 0.0


class InsuredPropertyDTO(BaseInsuredPropertyDTO):
    id: Optional[UUID] = None


class InsuredProperty(BaseSQLModel):
    __tablename__ = "insured_property"
    __table_args__ = {"extend_existing": True}

    quote_id: Column = Column(
        UUIDType, ForeignKey("quote.id", ondelete="CASCADE"), index=True
    )
    street_name = Column(String(255), nullable=True)
    postal_code = Column(String(20), nullable=True)
    city = Column(String(80), nullable=True)
    country = Column(String(20), nullable=True)
    occupancy = Column(String(255), nullable=True)
    tiv = Column(Float, nullable=True)

    quote = relationship("Quote", back_populates="insured_properties")  # type: ignore
