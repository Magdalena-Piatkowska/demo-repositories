from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, NonNegativeFloat

from app.domain.insured_property import InsuredPropertyDTO
from app.domain.occupancy_rate import OccupancyRateDTO
from app.ports.repositories import Repositories


class FireRiskDTO(BaseModel):
    quote_id: Optional[UUID] = None
    tiv: NonNegativeFloat = 0.0
    loss_cost: NonNegativeFloat = 0.0


def get_property_fire_loss_cost(
    insured_property: InsuredPropertyDTO, occupancy_rates: List[OccupancyRateDTO]
) -> float:
    occupancy_rate = 0.0
    for item in occupancy_rates:
        if item.occupancy == insured_property.occupancy:
            occupancy_rate = item.rate
    return insured_property.tiv * occupancy_rate


def get_fire_risk(quote_id: Union[UUID, str], repos: Repositories) -> FireRiskDTO:
    insured_properties: List[InsuredPropertyDTO] = repos.insured_property.read_multi(
        filters={"quote_id": quote_id}
    )
    occupancy_rates: List[OccupancyRateDTO] = repos.occupancy_rate.read_multi()

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
