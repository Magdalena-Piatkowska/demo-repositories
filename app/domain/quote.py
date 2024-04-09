from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BaseQuoteDTO(BaseModel):
    insured_name: Optional[str] = None
    inception_date: Optional[date] = date.today()


class QuoteDTO(BaseQuoteDTO):
    id: Optional[UUID] = None
