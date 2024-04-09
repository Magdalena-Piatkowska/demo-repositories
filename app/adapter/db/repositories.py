from typing import Optional, cast

from app.adapter.db.db_connection import SQLALchemyDBConnection
from app.adapter.db.model.insured_property import SQLInsuredPropertyRepository
from app.adapter.db.model.occupancy_rate import SQLOccupancyRateRepository
from app.adapter.db.model.quote import SQLQuoteRepository
from app.ports.db_connection import DBConnection
from app.ports.repositories import Repositories
from app.ports.storage_connection import StorageConnection


class SQLRepositories(Repositories):
    def __init__(
        self,
        db: Optional[DBConnection] = None,
        storage: Optional[StorageConnection] = None,
    ):
        super().__init__(db, storage)
        assert self.db
        self.db: SQLALchemyDBConnection = cast(SQLALchemyDBConnection, db)

    def commit(self):
        self.db.session.commit()

    def rollback(self):
        self.db.session.rollback()

    @property
    def quote(self) -> SQLQuoteRepository:
        return SQLQuoteRepository(self.db)

    @property
    def insured_property(self) -> SQLInsuredPropertyRepository:
        return SQLInsuredPropertyRepository(self.db)

    @property
    def occupancy_rate(self) -> SQLOccupancyRateRepository:
        return SQLOccupancyRateRepository(self.db)
