from typing import List, Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.model.fire_risk import FireRiskDTO
from app.model.insured_property import InsuredProperty, InsuredPropertyDTO
from app.model.occupancy_rate import OccupancyRate, OccupancyRateDTO


def get_property_fire_loss_cost(
    insured_property: InsuredPropertyDTO, occupancy_rates: List[OccupancyRateDTO]
) -> float:
    occupancy_rate = 0.0
    for item in occupancy_rates:
        if item.occupancy == insured_property.occupancy:
            occupancy_rate = item.rate
    return insured_property.tiv * occupancy_rate


def get_fire_risk(quote_id: Union[UUID, str], session: Session) -> FireRiskDTO:
    statement = select(InsuredProperty).where(InsuredProperty.quote_id == quote_id)
    results = session.execute(statement).all()
    insured_properties = [
        InsuredPropertyDTO(**result[0].__dict__) for result in results
    ]

    statement = select(OccupancyRate)
    results = session.execute(statement).all()
    occupancy_rates = [OccupancyRateDTO(**result[0].__dict__) for result in results]

    assert len(insured_properties) > 0
    quote_id = insured_properties[0].quote_id  # type: ignore
    tiv_sum = 0.0
    loss_cost_sum = 0.0

    for property_ in insured_properties:
        tiv_sum += property_.tiv
        loss_cost_sum += get_property_fire_loss_cost(
            insured_property=property_, occupancy_rates=occupancy_rates
        )

    return FireRiskDTO(quote_id=quote_id, tiv=tiv_sum, loss_cost=loss_cost_sum)  # type: ignore
