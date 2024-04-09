from collections.abc import Generator

from fastapi import Depends

from app.adapter.db.db_connection import SQLALchemyDBConnection
from app.adapter.db.repositories import SQLRepositories
from app.adapter.file.repositories import JSONRepositories
from app.adapter.file.storage_connection import AzureStorageConnection
from app.config import AZURE_STORAGE_CONNECTION_STRING, CONTAINER_NAME, DB_URL
from app.ports.db_connection import DBConnection
from app.ports.repositories import Repositories
from app.ports.storage_connection import StorageConnection


def get_sql_db() -> Generator[DBConnection, None, None]:
    adapter = SQLALchemyDBConnection(DB_URL)
    with adapter.transaction():
        yield adapter


def get_storage() -> Generator[StorageConnection, None, None]:
    adapter = AzureStorageConnection(
        container_name=CONTAINER_NAME, connection_string=AZURE_STORAGE_CONNECTION_STRING
    )
    yield adapter


def get_repos() -> Generator[Repositories, None, None]:
    adapter = SQLALchemyDBConnection(DB_URL)
    with adapter.transaction():
        yield SQLRepositories(adapter)


# def get_repos(storage=Depends(get_storage)) -> Generator[Repositories, None, None]:
#     yield JSONRepositories(storage=storage)
