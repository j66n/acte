from typing import Any

import jsonschema  # type: ignore

from acte.schema import Schema


class NumSchema(Schema):
    def __init__(
            self,
            type_: str | None = 'number',
            title: str | None = None,
            description: str | None = None,
            enum: list[None] | None = None,
            const: Any | None = None,
            all_of: list[Schema] | None = None,
            one_of: list[Schema] | None = None,
            any_of: list[Schema] | None = None,
            not_: Schema | None = None,
            if_: Schema | None = None,
            then: Schema | None = None,
            else_: Schema | None = None,

            multiple_of: float | None = None,
            minimum: float | None = None,
            maximum: float | None = None,
            exclusive_minimum: bool | None = None,
            exclusive_maximum: bool | None = None,
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

        self._multiple_of = multiple_of
        self._minimum = minimum
        self._maximum = maximum
        self._exclusive_minimum = exclusive_minimum
        self._exclusive_maximum = exclusive_maximum

    @property
    def multiple_of(self) -> float | None:
        return self._multiple_of

    @property
    def minimum(self) -> float | None:
        return self._minimum

    @property
    def maximum(self) -> float | None:
        return self._maximum

    @property
    def exclusive_minimum(self) -> bool | None:
        return self._exclusive_minimum

    @property
    def exclusive_maximum(self) -> bool | None:
        return self._exclusive_maximum

    @property
    def json_schema(self) -> dict[str, Any]:
        schema = super().json_schema

        if self._multiple_of is not None:
            schema['multipleOf'] = self._multiple_of

        if self._minimum is not None:
            schema['minimum'] = self._minimum

        if self._maximum is not None:
            schema['maximum'] = self._maximum

        if self._exclusive_minimum is not None:
            schema['exclusiveMinimum'] = self._exclusive_minimum

        if self._exclusive_maximum is not None:
            schema['exclusiveMaximum'] = self._exclusive_maximum

        return schema

    def resolve(self, data: Any) -> float:
        jsonschema.validate(data, self.json_schema)
        return float(data)
