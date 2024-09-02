from __future__ import annotations

from typing import TYPE_CHECKING

from acte.node.virtual.virtual import Virtual
from acte.node.implement.container import Container

if TYPE_CHECKING:
    from acte.build.component import Component


class ComponentNode(Virtual, Container):
    def __init__(self) -> None:
        Virtual.__init__(self)
        Container.__init__(self)

        self._component: Component | None = None

    @property
    def component(self) -> Component | None:
        return self._component

    def set_component(self, component: Component) -> None:
        self._component = component
