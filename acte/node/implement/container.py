from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from acte.node.node import Node


class Container:
    def __init__(self) -> None:
        super().__init__()

        self._children: list[Node] = []

    @property
    def children(self) -> list[Node]:
        return self._children

    def set_children(self, children: list[Node]) -> None:
        self._children = children
