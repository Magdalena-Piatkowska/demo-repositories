from typing import List, Union
from uuid import UUID

from fastapi import Depends, FastAPI

from app.adapter.fastapi.dependencies import get_repos, get_sql_db
from app.domain.fire_risk import FireRiskDTO, get_fire_risk
from app.domain.insured_property import (BaseInsuredPropertyDTO,
                                         InsuredPropertyDTO)
from app.domain.occupancy_rate import OccupancyRateDTO
from app.domain.quote import BaseQuoteDTO, QuoteDTO
from app.ports.db_connection import DBConnection
from app.ports.repositories import Repositories

app = FastAPI()


@app.get("/api/initialise-db")
def initialise_db(db: DBConnection = Depends(get_sql_db)):
    try:
        db.init_db()
        return
    except Exception as e:
        return {"An error occured": str(e)}


@app.get("/api/occupancy_rates")
def get_occupancy_rates(
    repos: Repositories = Depends(get_repos),
) -> List[OccupancyRateDTO]:
    result = repos.occupancy_rate.read_multi()
    return result


@app.get("/api/quote")
def get_quote(id, repos: Repositories = Depends(get_repos)) -> QuoteDTO:
    result = repos.quote.read(id=id)
    return result


@app.post("/api/quote")
def create_quote(
    obj_in: BaseQuoteDTO,
    repos: Repositories = Depends(get_repos),
) -> QuoteDTO:
    result = repos.quote.create(
        obj_in=obj_in,
    )
    return result


@app.get("/api/property")
def get_properties(
    quote_id: Union[UUID, str], repos: Repositories = Depends(get_repos)
) -> List[InsuredPropertyDTO]:
    if quote_id:
        result = repos.insured_property.read_multi(filters={"quote_id": quote_id})
    else:
        result = repos.insured_property.read_multi()
    return result


@app.post("/api/fire-risk")
def calculate(
    quote_id: Union[UUID, str], repos: Repositories = Depends(get_repos)
) -> FireRiskDTO:
    return get_fire_risk(quote_id=quote_id, repos=repos)
