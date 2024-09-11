from typing import Any

import jsonschema  # type: ignore

from acte.schema.simple_schema.simple_schema import SimpleSchema
from acte.schema.schema import Schema


class ArrSchema(SimpleSchema):
    def __init__(self) -> None:
        super().__init__()
        self._enum: list[list[Any]] | None = None
        self._items: Schema | None = None

    @property
    def enum(self) -> list[list[Any]] | None:
        return self._enum

    @property
    def items(self) -> Schema | None:
        return self._items

    def set_enum(self, enum: list[list[Any]] | None) -> None:
        self._enum = enum

    def set_items(self, items: Schema | None) -> None:
        self._items = items

    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "array",
        }

        if self._title is not None:
            schema['title'] = self._title

        if self._enum is not None:
            schema['enum'] = self._enum

        return schema

    def resolve(self, data: Any) -> list[Any]:
        jsonschema.validate(data, self.json_schema)
        return data
