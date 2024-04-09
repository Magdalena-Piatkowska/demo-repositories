from sqlalchemy import Column, Date, String
from sqlalchemy.orm import relationship

from app.adapter.db.model.base import BaseSQLModel
from app.adapter.db.repository import SQLRepository
from app.domain.quote import QuoteDTO


class Quote(BaseSQLModel):
    __tablename__ = "quote"
    __table_args__ = {"extend_existing": True}

    insured_name = Column(String(255), nullable=True)
    inception_date = Column(Date, nullable=True)

    insured_properties = relationship("InsuredProperty", back_populates="quote")  # type: ignore


class SQLQuoteRepository(SQLRepository):
    model = Quote
    model_dto = QuoteDTO
