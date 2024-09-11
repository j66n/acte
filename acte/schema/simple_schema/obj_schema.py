from typing import Any

import jsonschema  # type: ignore

from acte.schema.simple_schema.simple_schema import SimpleSchema
from acte.schema.schema import Schema


class ObjSchema(SimpleSchema):
    def __init__(self) -> None:
        super().__init__()
        self._enum: list[dict[str, Any]] | None = None
        self._properties: dict[str, Schema] | None = None
        self._required: list[str] | None = None

    @property
    def enum(self) -> list[dict[str, Any]] | None:
        return self._enum

    @property
    def properties(self) -> dict[str, Schema] | None:
        return self._properties

    @property
    def required(self) -> list[str] | None:
        return self._required

    def set_enum(self, enum: list[dict[str, Any]] | None) -> None:
        self._enum = enum

    def set_properties(self, properties: dict[str, Schema] | None) -> None:
        self._properties = properties

    def set_required(self, required: list[str] | None) -> None:
        self._required = required

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

    def resolve(self, data: Any) -> dict[str, Any]:
        jsonschema.validate(data, self.json_schema)
        return data
