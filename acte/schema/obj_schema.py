from typing import Any

import jsonschema  # type: ignore

from acte.schema import StrSchema
from acte.schema.schema import Schema


class ObjSchema(Schema):
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
            pattern_properties: dict[str, Schema] | None = None,
            additional_properties: Schema | bool | None = None,
            unevaluated_properties: Schema | bool | None = None,
            required: list[str] | None = None,
            property_names: StrSchema | None = None,
            min_properties: int | None = None,
            max_properties: int | None = None,
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
        self._pattern_properties = pattern_properties
        self._additional_properties = additional_properties
        self._unevaluated_properties = unevaluated_properties
        self._required = required
        self._property_names = property_names
        self._min_properties = min_properties
        self._max_properties = max_properties

    def __getitem__(self, key) -> Schema | None:
        return self._properties.get(key) if self._properties is not None else None

    @property
    def properties(self) -> dict[str, Schema] | None:
        return self._properties

    @property
    def pattern_properties(self) -> dict[str, Schema] | None:
        return self._pattern_properties

    @property
    def additional_properties(self) -> Schema | bool | None:
        return self._additional_properties

    @property
    def unevaluated_properties(self) -> Schema | bool | None:
        return self._unevaluated_properties

    @property
    def required(self) -> list[str] | None:
        return self._required

    @property
    def property_names(self) -> StrSchema | None:
        return self._property_names

    @property
    def min_properties(self) -> int | None:
        return self._min_properties

    @property
    def max_properties(self) -> int | None:
        return self._max_properties

    @property
    def json_schema(self) -> dict[str, Any]:
        schema = super().json_schema

        if self._properties is not None:
            schema['properties'] = {
                key: value.json_schema
                for key, value in self._properties.items()
            }

        if self._pattern_properties is not None:
            schema['patternProperties'] = {
                key: value.json_schema
                for key, value in self._pattern_properties.items()
            }

        if self._additional_properties is not None:
            if isinstance(self._additional_properties, bool):
                schema['additionalProperties'] = self._additional_properties
            else:
                schema['additionalProperties'] = self._additional_properties.json_schema

        if self._unevaluated_properties is not None:
            if isinstance(self._unevaluated_properties, bool):
                schema['unevaluatedProperties'] = self._unevaluated_properties
            else:
                schema['unevaluatedProperties'] = self._unevaluated_properties.json_schema

        if self._required is not None:
            schema['required'] = self._required

        if self._property_names is not None:
            schema['propertyNames'] = self._property_names.json_schema

        if self._min_properties is not None:
            schema['minProperties'] = self._min_properties

        if self._max_properties is not None:
            schema['maxProperties'] = self._max_properties

        return schema

    def resolve(self, data: Any) -> dict[str, Any]:
        jsonschema.validate(data, self.json_schema)
        return data
