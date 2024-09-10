from typing import Any

from acte.schema.base_schema.base_schema import BasicSchema


class IntSchema(BasicSchema):
    def __init__(self) -> None:
        super().__init__()
        self._enum: list[int] | None = None

    @property
    def enum(self) -> list[int] | None:
        return self._enum

    def set_enum(self, enum: list[int] | None) -> None:
        self._enum = enum

    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "integer",
        }

        if self._title is not None:
            schema['title'] = self._title

        if self._enum is not None:
            schema['enum'] = self._enum

        return schema