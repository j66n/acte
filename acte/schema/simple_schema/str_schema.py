from typing import Any

import jsonschema  # type: ignore

from acte.schema import Schema
from acte.schema.simple_schema.base_schema import BaseSchema


class StrSchema(BaseSchema):
    def __init__(
            self,
            type_: str | None = 'string',
            title: str | None = None,
            description: str | None = None,
            enum: list[str] | None = None,
            const: Any | None = None,
            all_of: list[Schema] | None = None,
            one_of: list[Schema] | None = None,
            any_of: list[Schema] | None = None,
            not_: Schema | None = None,
            if_: Schema | None = None,
            then: Schema | None = None,
            else_: Schema | None = None,

            min_length: int | None = None,
            max_length: int | None = None,
    ) -> None:
        super().__init__(
            type_=type_,
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

        self.min_length = min_length
        self.max_length = max_length

    @property
    def json_schema(self) -> dict[str, Any]:
        schema = super().json_schema

        if self.min_length is not None:
            schema["minLength"] = self.min_length

        if self.max_length is not None:
            schema["maxLength"] = self.max_length

        return schema

    def resolve(self, data: Any) -> str:
        jsonschema.validate(data, self.json_schema)
        return str(data)
