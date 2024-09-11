from abc import ABC, abstractmethod
from typing import Any

import jsonschema  # type: ignore

from acte.schema.schema import Schema


class SimpleSchema(Schema, ABC):
    def __init__(self) -> None:
        self._title: str | None = None

    @property
    def title(self) -> str | None:
        return self._title

    def set_title(self, title: str | None) -> None:
        self._title = title

    @abstractmethod
    def resolve(self, data: Any) -> Any:
        pass
