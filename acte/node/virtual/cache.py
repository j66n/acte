from typing import Any

from acte.node.virtual.virtual import Virtual
from acte.node.implement.container import Container


class Cache(Virtual, Container):
    def __init__(self, identifier: Any, persistent: bool) -> None:
        Virtual.__init__(self)
        Container.__init__(self)

        self._identifier = identifier
        self._persistent = persistent

    @property
    def identifier(self) -> Any:
        return self._identifier

    @property
    def persistent(self) -> bool:
        return self._persistent
