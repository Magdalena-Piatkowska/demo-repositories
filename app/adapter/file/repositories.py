from typing import Optional

from app.adapter.file.model.insured_property import JSONInsuredPropertyRepository
from app.adapter.file.model.occupancy_rate import JSONOccupancyRateRepository
from app.adapter.file.model.quote import JSONQuoteRepository
from app.ports.db_connection import DBConnection
from app.ports.repositories import Repositories
from app.ports.storage_connection import StorageConnection


class JSONRepositories(Repositories):
    def __init__(
        self,
        db: Optional[DBConnection] = None,
        storage: Optional[StorageConnection] = None,
    ):
        super().__init__(db, storage)
        assert self.storage

    @property
    def quote(self) -> JSONQuoteRepository:
        return JSONQuoteRepository(storage=self.storage)

    @property
    def insured_property(self) -> JSONInsuredPropertyRepository:
        return JSONInsuredPropertyRepository(storage=self.storage)

    @property
    def occupancy_rate(self) -> JSONOccupancyRateRepository:
        return JSONOccupancyRateRepository(storage=self.storage)
