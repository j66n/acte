from typing import Any

import jsonschema  # type: ignore

from acte.schema.simple_schema.base_schema import BaseSchema
from acte.schema.schema import Schema


class ObjSchema(BaseSchema):
    def __init__(
            self,
            type_: str | None = 'object',
            title: str | None = None,
            description: str | None = None,
            enum: list[dict[str, Any]] | None = None,
            const: Any | None = None,
            all_of: list[Schema] | None = None,
            one_of: list[Schema] | None = None,
            any_of: list[Schema] | None = None,
            not_: Schema | None = None,
            if_: Schema | None = None,
            then: Schema | None = None,
            else_: Schema | None = None,

            properties: dict[str, Schema] | None = None,
            required: list[str] | None = None,
            additional_properties: bool | None = None
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

        self._properties = properties
        self._required = required
        self._additional_properties = additional_properties

    def __getitem__(self, key) -> Schema | None:
        return self._properties.get(key) if self._properties is not None else None

    @property
    def properties(self) -> dict[str, Schema] | None:
        return self._properties

    @property
    def required(self) -> list[str] | None:
        return self._required

    @property
    def additional_properties(self) -> bool | None:
        return self._additional_properties

    @property
    def json_schema(self) -> dict[str, Any]:
        schema = super().json_schema

        if self._properties is not None:
            schema['properties'] = {
                key: value.json_schema
                for key, value in self._properties.items()
            }

        if self._required is not None:
            schema['required'] = self._required

        if self._additional_properties is not None:
            schema['additionalProperties'] = self._additional_properties

        return schema

    def resolve(self, data: Any) -> dict[str, Any]:
        print(self.json_schema)
        jsonschema.validate(data, self.json_schema)
        return data
