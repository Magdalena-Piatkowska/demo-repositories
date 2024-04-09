from abc import ABC
from io import StringIO
from typing import Set


class StorageConnection(ABC):
    def __init__(
        self,
        container_name: str,
        connection_string: str,
    ):
        self.container_name: str = ""

    def load(self, file_path: str) -> StringIO:
        raise NotImplementedError

    def save(self, file_path: str, data: str):
        raise NotImplementedError

    def list_blobs_flat(self, container_name: str) -> Set[str]:
        raise NotImplementedError
