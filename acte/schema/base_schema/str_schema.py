from typing import Any

import jsonschema

from acte.schema.base_schema.base_schema import BasicSchema


class StrSchema(BasicSchema):
    def __init__(self) -> None:
        super().__init__()
        self._enum: list[str] | None = None

    @property
    def enum(self) -> list[str] | None:
        return self._enum

    def set_enum(self, enum: list[str] | None) -> None:
        self._enum = enum

    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "string",
        }

        if self._title is not None:
            schema['title'] = self._title

        if self._enum is not None:
            schema['enum'] = self._enum

        return schema

    def resolve(self, data: Any) -> str:
        jsonschema.validate(data, self.json_schema)
        return str(data)
