from __future__ import annotations

from typing import TYPE_CHECKING

from acte.node.implement.container import Container
from acte.state.effect import Effect

if TYPE_CHECKING:
    from acte.node.virtual.cache import Cache


class Node:
    """
    - Node
        - Element
            - Block (HasChildren)
            - Inline
        - Virtual (HasChildren)
    """

    def __init__(self) -> None:
        self._effect_list: list[Effect] = []

    def add_effect(self, e: Effect) -> None:
        self._effect_list.append(e)

    def unmount(self, cached_list: list[Cache] | None = None) -> None:
        if isinstance(self, Container):
            while len(self.children) != 0:
                child = self.children.pop(0)

                if (cached_list is not None) and (child not in cached_list):
                    child.unmount(cached_list)

        for effect in self._effect_list:
            effect.cancel()
