from typing import Any

import jsonschema  # type: ignore

from acte.schema.schema import Schema


class ArrSchema(Schema):
    def __init__(
            self,
            type_: str | None = "array",
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

            items: Schema | bool | None = None,
            prefix_items: list[Schema] | None = None,
            unevaluated_items: Schema | bool | None = None,
            contains: Schema | None = None,
            min_contains: int | None = None,
            max_contains: int | None = None,
            min_items: int | None = None,
            max_items: int | None = None,
            unique_items: bool | None = None,
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

        self._items: Schema | bool | None = items
        self._prefix_items: list[Schema] | None = prefix_items
        self._unevaluated_items: Schema | bool | None = unevaluated_items
        self._contains: Schema | None = contains
        self._min_contains: int | None = min_contains
        self._max_contains: int | None = max_contains
        self._min_items: int | None = min_items
        self._max_items: int | None = max_items
        self._unique_items: bool | None = unique_items

    @property
    def items(self) -> Schema | bool | None:
        return self._items

    @property
    def prefix_items(self) -> list[Schema] | None:
        return self._prefix_items

    @property
    def unevaluated_items(self) -> Schema | bool | None:
        return self._unevaluated_items

    @property
    def contains(self) -> Schema | None:
        return self._contains

    @property
    def min_contains(self) -> int | None:
        return self._min_contains

    @property
    def max_contains(self) -> int | None:
        return self._max_contains

    @property
    def min_items(self) -> int | None:
        return self._min_items

    @property
    def max_items(self) -> int | None:
        return self._max_items

    @property
    def unique_items(self) -> bool | None:
        return self._unique_items

    @property
    def json_schema(self) -> dict[str, Any]:
        schema = super().json_schema

        if self.items is not None:
            if isinstance(self.items, bool):
                schema["items"] = self.items
            else:
                schema["items"] = self.items.json_schema

        if self.prefix_items is not None:
            schema["prefixItems"] = [item.json_schema for item in self.prefix_items]

        if self.unevaluated_items is not None:
            if isinstance(self.unevaluated_items, bool):
                schema["unevaluatedItems"] = self.unevaluated_items
            else:
                schema["unevaluatedItems"] = self.unevaluated_items.json_schema

        if self.contains is not None:
            schema["contains"] = self.contains.json_schema

        if self.min_contains is not None:
            schema["minContains"] = self.min_contains

        if self.max_contains is not None:
            schema["maxContains"] = self.max_contains

        if self.min_items is not None:
            schema["minItems"] = self.min_items

        if self.max_items is not None:
            schema["maxItems"] = self.max_items

        if self.unique_items is not None:
            schema["uniqueItems"] = self.unique_items

        return schema

    def resolve(self, data: Any) -> list[Any]:
        jsonschema.validate(data, self.json_schema)
        return data
