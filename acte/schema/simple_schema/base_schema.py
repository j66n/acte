from typing import Any

import jsonschema  # type: ignore

from acte.schema.schema import Schema


class BaseSchema(Schema):
    def __init__(
            self,
            type_: str | None = None,
            title: str | None = None,
            description: str | None = None,
            enum: list[Any] | None = None,
            const: Any | None = None,
            all_of: list[Schema] | None = None,
            one_of: list[Schema] | None = None,
            any_of: list[Schema] | None = None,
            not_: Schema | None = None,
            if_: Schema | None = None,
            then: Schema | None = None,
            else_: Schema | None = None,
    ) -> None:
        self._type: str | None = type_
        self._title: str | None = title
        self._description: str | None = description
        self._enum: list[Any] | None = enum
        self._const: Any | None = const
        self._all_of: list[Schema] | None = all_of
        self._one_of: list[Schema] | None = one_of
        self._any_of: list[Schema] | None = any_of
        self._not: Schema | None = not_
        self._if: Schema | None = if_
        self._then: Schema | None = then
        self._else: Schema | None = else_

    @property
    def type(self) -> str | None:
        return self._type

    @property
    def title(self) -> str | None:
        return self._title

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def enum(self) -> list[Any] | None:
        return self._enum

    @property
    def const(self) -> Any | None:
        return self._const

    @property
    def all_of(self) -> list[Schema] | None:
        return self._all_of

    @property
    def one_of(self) -> list[Schema] | None:
        return self._one_of

    @property
    def any_of(self) -> list[Schema] | None:
        return self._any_of

    @property
    def not_(self) -> Schema | None:
        return self._not

    @property
    def if_(self) -> Schema | None:
        return self._if

    @property
    def then(self) -> Schema | None:
        return self._then

    @property
    def else_(self) -> Schema | None:
        return self._else

    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": self.type
        }

        if self._title is not None:
            schema['title'] = self._title

        if self._description is not None:
            schema['description'] = self._description

        if self._enum is not None:
            schema['enum'] = self._enum

        if self._const is not None:
            schema['const'] = self._const

        if self._all_of is not None:
            schema['allOf'] = [value.json_schema for value in self._all_of]

        if self._one_of is not None:
            schema['oneOf'] = [value.json_schema for value in self._one_of]

        if self._any_of is not None:
            schema['anyOf'] = [value.json_schema for value in self._any_of]

        if self._not is not None:
            schema['not'] = self._not.json_schema

        if self._if is not None:
            schema['if'] = self._if.json_schema

        if self._then is not None:
            schema['then'] = self._then.json_schema

        if self._else is not None:
            schema['else'] = self._else.json_schema

        return schema

    def resolve(self, data: Any) -> Any:
        jsonschema.validate(data, self.json_schema)
        return data
