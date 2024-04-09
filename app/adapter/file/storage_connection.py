from io import StringIO
from typing import Set

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobClient, BlobServiceClient

from app.ports.storage_connection import StorageConnection


class FileNotFoundException(Exception):
    pass


class AzureStorageConnection(StorageConnection):
    def __init__(
        self,
        container_name: str,
        connection_string: str,
    ):
        self.container_name = container_name
        self.client: BlobServiceClient = BlobServiceClient.from_connection_string(
            connection_string
        )

    def load(self, file_path: str) -> StringIO:
        try:
            blob_client: BlobClient = self.client.get_blob_client(
                container=self.container_name, blob=file_path
            )
            return StringIO(blob_client.download_blob().readall().decode("utf-8"))
        except ResourceNotFoundError as err:
            raise FileNotFoundException(
                f"File not found, container: {self.container_name}. path: {file_path}"
            )

    def save(self, file_path: str, data: str, overwrite: bool = True):
        blob_client = self.client.get_blob_client(
            container=self.container_name, blob=file_path
        )
        blob_client.upload_blob(data, overwrite=overwrite)

    def list_blobs_flat(self, container_name: str) -> Set[str]:
        return set(
            self.client.get_container_client(container=container_name).list_blob_names()
        )
