from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Column, Date, String
from sqlalchemy.orm import relationship

from app.model.base import BaseSQLModel


class BaseQuoteDTO(BaseModel):
    insured_name: Optional[str] = None
    inception_date: Optional[date] = date.today()


class QuoteDTO(BaseQuoteDTO):
    id: Optional[UUID] = None


class Quote(BaseSQLModel):
    __tablename__ = "quote"
    __table_args__ = {"extend_existing": True}

    insured_name = Column(String(255), nullable=True)
    inception_date = Column(Date, nullable=True)

    insured_properties = relationship("InsuredProperty", back_populates="quote")  # type: ignore
