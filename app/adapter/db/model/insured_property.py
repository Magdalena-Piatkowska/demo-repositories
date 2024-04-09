from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from app.adapter.db.model.base import BaseSQLModel
from app.adapter.db.repository import SQLRepository
from app.domain.insured_property import InsuredPropertyDTO


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


class SQLInsuredPropertyRepository(SQLRepository):
    model = InsuredProperty
    model_dto = InsuredPropertyDTO
