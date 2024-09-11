from typing import Any

import jsonschema  # type: ignore

from acte.schema.simple_schema.simple_schema import SimpleSchema


class BoolSchema(SimpleSchema):
    def __init__(self) -> None:
        super().__init__()
        self._enum: list[bool] | None = None

    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "boolean",
        }

        if self._title is not None:
            schema['title'] = self._title

        if self.enum is not None:
            schema['enum'] = self.enum

        return schema

    @property
    def enum(self) -> list[bool] | None:
        return self._enum

    def resolve(self, data: Any) -> bool:
        jsonschema.validate(data, self.json_schema)
        return bool(data)
