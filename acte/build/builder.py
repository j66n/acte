from typing import Type

from acte.build.viewer.viewer import Viewer
from acte.build.component import Component
from acte.node import Root


class Builder(Viewer):
    @classmethod
    async def build(cls, entry_class: Type[Component]) -> Root:
        entry = entry_class()

        root = Root()

        cls._append_container(root)

        await cls._component_constructor(entry)

        cls._pop_container()

        return root
