from __future__ import annotations

from acte.build.component import Component, call_on_mount
from acte.build.viewer.common.base import Base

from acte.node import ComponentNode


class ComponentViewer(Base):
    @classmethod
    def component(cls, c: Component) -> None:
        cls._check_skip()

        cls._append_awaitable(cls._component_constructor(c))

    @classmethod
    async def _component_constructor(cls, c: Component) -> None:
        component_node = ComponentNode()
        component_node.set_component(c)

        cls._append_container(component_node)

        cls._append_new_awaitable_list()

        c.view()
        await call_on_mount(c)
        await cls._call_awaitable_list()

        cls._pop_awaitable_list()

        node = cls._pop_container_node()

        cls._attach_to_container(node)
