from abc import ABC, abstractmethod
from typing import Any

import jsonschema  # type: ignore


class Schema(ABC):
    @abstractmethod
    def resolve(self, data: Any) -> Any:
        pass

    @property
    @abstractmethod
    def json_schema(self) -> dict[str, Any]:
        pass
