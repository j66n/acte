from typing import Any

import jsonschema  # type: ignore

from acte.schema import Schema


class StrSchema(Schema):
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
            pattern: str | None = None,
            format_: str | None = None,
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

        self._min_length = min_length
        self._max_length = max_length
        self._pattern = pattern
        self._format = format_

    @property
    def min_length(self) -> int | None:
        return self._min_length

    @property
    def max_length(self) -> int | None:
        return self._max_length

    @property
    def pattern(self) -> str | None:
        return self._pattern

    @property
    def format_(self) -> str | None:
        return self._format

    @property
    def json_schema(self) -> dict[str, Any]:
        schema = super().json_schema

        if self._min_length is not None:
            schema["minLength"] = self._min_length

        if self._max_length is not None:
            schema["maxLength"] = self._max_length

        if self._pattern is not None:
            schema["pattern"] = self._pattern

        if self._format is not None:
            schema["format"] = self._format

        return schema

    def resolve(self, data: Any) -> str:
        jsonschema.validate(data, self.json_schema)
        return str(data)
