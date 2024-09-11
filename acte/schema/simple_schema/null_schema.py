from typing import Any

from acte.schema.simple_schema.simple_schema import SimpleSchema


class NullSchema(SimpleSchema):
    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "null",
        }

        if self._title is not None:
            schema['title'] = self._title

        return schema

    def resolve(self, data: Any) -> None:
        return None
