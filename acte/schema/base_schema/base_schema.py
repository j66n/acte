from abc import ABC
from typing import Any

import jsonschema

from acte.schema.schema import Schema


class BasicSchema(Schema, ABC):
    def __init__(self) -> None:
        self._title: str | None = None

    @property
    def title(self) -> str | None:
        return self._title

    def set_title(self, title: str | None) -> None:
        self._title = title

    def resolve(self, data: Any) -> int:
        jsonschema.validate(data, self.json_schema)
        return int(data)
