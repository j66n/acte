from typing import Any

from acte.schema.base_schema.base_schema import BasicSchema


class NullSchema(BasicSchema):
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
