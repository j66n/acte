from typing import Any

import jsonschema  # type: ignore

from acte.schema import Schema
from acte.schema.simple_schema.base_schema import BaseSchema


class IntSchema(BaseSchema):
    def __init__(
            self,
            title: str | None = None,
            description: str | None = None,
            enum: list[int] | None = None,
            const: Any | None = None,
            all_of: list[Schema] | None = None,
            one_of: list[Schema] | None = None,
            any_of: list[Schema] | None = None,
            not_: Schema | None = None,
            if_: Schema | None = None,
            then: Schema | None = None,
            else_: Schema | None = None,

            minimum: int | None = None,
            maximum: int | None = None,
    ) -> None:
        super().__init__(
            type_="integer",
            title=title,
            description=description,
            enum=enum,
            const=const,
            all_of=all_of,
            one_of=one_of,
            any_of=any_of,
            not_=not_,
            if_=if_,
            then=then,
            else_=else_,
        )

        self._minimum = minimum
        self._maximum = maximum

    @property
    def minimum(self) -> int | None:
        return self._minimum

    @property
    def maximum(self) -> int | None:
        return self._maximum

    @property
    def json_schema(self) -> dict[str, Any]:
        schema = super().json_schema

        if self.minimum is not None:
            schema["minimum"] = self.minimum

        if self.maximum is not None:
            schema["maximum"] = self.maximum

        return schema

    def resolve(self, data: Any) -> int:
        jsonschema.validate(data, self.json_schema)
        return int(data)
