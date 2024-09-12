from typing import Any

import jsonschema  # type: ignore

from acte.schema.simple_schema.base_schema import BaseSchema
from acte.schema.schema import Schema


class ArrSchema(BaseSchema):
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

            items: Schema | None = None,
            unique_items: bool | None = None,
            min_items: int | None = None,
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

        self._items: Schema | None = items
        self._unique_items: bool | None = unique_items
        self._min_items: int | None = min_items

    @property
    def items(self) -> Schema | None:
        return self._items

    @property
    def unique_items(self) -> bool | None:
        return self._unique_items

    @property
    def min_items(self) -> int | None:
        return self._min_items

    @property
    def json_schema(self) -> dict[str, Any]:
        schema = super().json_schema

        if self.items is not None:
            schema["items"] = self.items.json_schema

        if self.unique_items is not None:
            schema["uniqueItems"] = self.unique_items

        if self.min_items is not None:
            schema["minItems"] = self.min_items

        return schema

    def resolve(self, data: Any) -> list[Any]:
        jsonschema.validate(data, self.json_schema)
        return data
