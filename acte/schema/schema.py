import abc
from typing import Any

import jsonschema  # type: ignore

from acte.state import Ref


class Schema:

    @abc.abstractmethod
    def resolve(self, data: Any) -> Any:
        pass

    @property
    @abc.abstractmethod
    def json_schema(self) -> dict[str, Any]:
        pass


class BasicSchema(Schema):
    def __init__(self, title: Ref[str] | None) -> None:
        self._title = title

    @property
    def title(self) -> Ref[str] | None:
        return self._title


class StrSchema(BasicSchema):
    def __init__(
            self,
            title: Ref[str] | None = None,
            enum: Ref[list[str]] | None = None
    ) -> None:
        super().__init__(title)
        self._enum = enum

    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "string",
        }

        if self._enum is not None:
            schema['enum'] = self._enum.value

        return schema

    @property
    def enum(self) -> Ref[list[str]] | None:
        return self._enum

    def resolve(self, data: Any) -> str:
        jsonschema.validate(data, self.json_schema)
        return str(data)


class IntSchema(BasicSchema):
    def __init__(
            self,
            title: Ref[str] | None = None,
            enum: Ref[list[int]] | None = None
    ) -> None:
        super().__init__(title)
        self._enum = enum

    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "integer",
        }

        if self._enum is not None:
            schema['enum'] = self._enum.value

        return schema

    @property
    def enum(self) -> Ref[list[int]] | None:
        return self._enum

    def resolve(self, data: Any) -> int:
        jsonschema.validate(data, self.json_schema)
        return int(data)


class NumSchema(BasicSchema):
    def __init__(
            self,
            title: Ref[str] | None = None,
            enum: Ref[list[float]] | None = None
    ) -> None:
        super().__init__(title)
        self._enum = enum

    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "number",
        }

        if self._enum is not None:
            schema['enum'] = self._enum.value

        return schema

    @property
    def enum(self) -> Ref[list[float]] | None:
        return self._enum

    def resolve(self, data: Any) -> float:
        jsonschema.validate(data, self.json_schema)
        return float(data)


class BoolSchema(BasicSchema):
    def __init__(
            self,
            title: Ref[str] | None = None,
            enum: Ref[list[bool]] | None = None
    ) -> None:
        super().__init__(title)
        self._enum = enum

    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "boolean",
        }

        if self.enum is not None:
            schema['enum'] = self.enum.value

        return schema

    @property
    def enum(self) -> Ref[list[bool]] | None:
        return self._enum

    def resolve(self, data: Any) -> bool:
        jsonschema.validate(data, self.json_schema)
        return bool(data)


class NullSchema(BasicSchema):
    def __init__(
            self,
            title: Ref[str] | None = None,
    ) -> None:
        super().__init__(title)

    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "null",
        }

        return schema

    def resolve(self, data: Any) -> None:
        return None
