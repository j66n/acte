import abc
from typing import Any

import jsonschema  # type: ignore


class Schema:
    @abc.abstractmethod
    def resolve(self, data: Any) -> Any:
        pass

    @property
    @abc.abstractmethod
    def json_schema(self) -> dict[str, Any]:
        pass


class BasicSchema(Schema):
    def __init__(self) -> None:
        self._title: str | None = None

    @property
    def title(self) -> str | None:
        return self._title

    def set_title(self, title: str | None) -> None:
        self._title = title


class StrSchema(BasicSchema):
    def __init__(self) -> None:
        super().__init__()
        self._enum: list[str] | None = None

    @property
    def enum(self) -> list[str] | None:
        return self._enum

    def set_enum(self, enum: list[str] | None) -> None:
        self._enum = enum

    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "string",
        }

        if self._title is not None:
            schema['title'] = self._title

        if self._enum is not None:
            schema['enum'] = self._enum

        return schema

    def resolve(self, data: Any) -> str:
        jsonschema.validate(data, self.json_schema)
        return str(data)


class IntSchema(BasicSchema):
    def __init__(self) -> None:
        super().__init__()
        self._enum: list[int] | None = None

    @property
    def enum(self) -> list[int] | None:
        return self._enum

    def set_enum(self, enum: list[int] | None) -> None:
        self._enum = enum

    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "integer",
        }

        if self._title is not None:
            schema['title'] = self._title

        if self._enum is not None:
            schema['enum'] = self._enum

        return schema

    def resolve(self, data: Any) -> int:
        jsonschema.validate(data, self.json_schema)
        return int(data)


class NumSchema(BasicSchema):
    def __init__(self) -> None:
        super().__init__()
        self._enum: list[float] | None = None

    @property
    def enum(self) -> list[float] | None:
        return self._enum

    def set_enum(self, enum: list[float] | None) -> None:
        self._enum = enum

    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "number",
        }

        if self._title is not None:
            schema['title'] = self._title

        if self._enum is not None:
            schema['enum'] = self._enum

        return schema

    def resolve(self, data: Any) -> float:
        jsonschema.validate(data, self.json_schema)
        return float(data)


class BoolSchema(BasicSchema):
    def __init__(self) -> None:
        super().__init__()
        self._enum: list[bool] | None = None

    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "boolean",
        }

        if self._title is not None:
            schema['title'] = self._title

        if self.enum is not None:
            schema['enum'] = self.enum

        return schema

    @property
    def enum(self) -> list[bool] | None:
        return self._enum

    def resolve(self, data: Any) -> bool:
        jsonschema.validate(data, self.json_schema)
        return bool(data)


class NullSchema(BasicSchema):
    @property
    def json_schema(self) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "null",
        }

        if self._title is not None:
            schema['title'] = self._title

        return schema

    def resolve(self, data: Any) -> None:
        return None
