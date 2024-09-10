from typing import Any

import jsonschema

from acte.schema.base_schema.base_schema import BasicSchema
from acte.schema.schema import Schema


class ArraySchema(BasicSchema):
    def __init__(self) -> None:
        super().__init__()
        self._enum: list[Any] | None = None
        self._items: Schema | None = None

    @property
    def enum(self) -> list[list[Any]] | None:
        return self._enum

    @property
    def items(self) -> Schema:
        return self._items

    def set_enum(self, enum: list[list[Any]] | None) -> None:
        self._enum = enum

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
        return
