from typing import List, Union
from uuid import UUID

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.calculations import get_fire_risk
from app.db_connection import get_session
from app.model.fire_risk import FireRiskDTO
from app.model.insured_property import (
    BaseInsuredPropertyDTO,
    InsuredProperty,
    InsuredPropertyDTO,
)
from app.model.occupancy_rate import OccupancyRate, OccupancyRateDTO
from app.model.quote import BaseQuoteDTO, Quote, QuoteDTO

app = FastAPI()


@app.get("/api/occupancy_rates")
def get_occupancy_rates(
    session: Session = Depends(get_session),
) -> List[OccupancyRateDTO]:
    statement = select(OccupancyRate)
    results = session.execute(statement).all()
    results = [OccupancyRateDTO(**result[0].__dict__) for result in results]  # type: ignore
    return results  # type: ignore


@app.get("/api/quote")
def get_quote(id, session: Session = Depends(get_session)) -> QuoteDTO:
    statement = select(Quote).where(Quote.id == id)
    result = session.execute(statement).first()
    result = QuoteDTO(**result[0].__dict__)  # type: ignore
    return result  # type: ignore


@app.post("/api/quote")
def create_quote(
    obj_in: BaseQuoteDTO, session: Session = Depends(get_session)
) -> QuoteDTO:
    db_obj = Quote(**obj_in.model_dump())
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    result = QuoteDTO(**db_obj.__dict__)
    return result


@app.get("/api/property")
def get_properties(
    quote_id: Union[UUID, str], session: Session = Depends(get_session)
) -> List[InsuredPropertyDTO]:
    if quote_id:
        statement = select(InsuredProperty).where(InsuredProperty.quote_id == quote_id)
    else:
        statement = select(InsuredProperty)
    results = session.execute(statement).all()
    results = [InsuredPropertyDTO(**result[0].__dict__) for result in results]  # type: ignore
    return results  # type: ignore


@app.post("/api/fire-risk")
def calculate(
    quote_id: Union[UUID, str], session: Session = Depends(get_session)
) -> FireRiskDTO:
    assert quote_id
    fire_risk = get_fire_risk(quote_id=quote_id, session=session)
    return fire_risk
