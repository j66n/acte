from typing import TypeVar, Type

from acte.build import Component, Builder
from acte.executor import Executor, ActionType
from acte.node import Root, Node
from acte.render import Renderer
from acte.context import Context, ContextObj

T = TypeVar('T')


class Session:
    def __init__(
            self,
            entry_class: Type[Component],
            builder: Builder,
            executor: Executor,
            renderer: Renderer
    ) -> None:
        self._entry_class = entry_class
        self._builder = builder
        self._executor = executor
        self._renderer = renderer

        self._context = ContextObj()
        self._root: Root | None = None

    async def start(self) -> None:
        Context.use(self._context)

        self._root = await self._builder.build(self._entry_class)

    async def execute(self, target_id: str, action_type: ActionType, value: str | None = None) -> None:
        Context.use(self._context)

        if not isinstance(self._root, Root):
            raise RuntimeError("session hasn't started, and root is None.")

        await self._executor.execute(self._root, target_id, action_type, value)

    async def display(self) -> None:
        if not isinstance(self._root, Node):
            raise RuntimeError("session hasn't started, and root is None.")

        await self._executor.display(self._root)

    def render(self) -> str:
        if not isinstance(self._root, Node):
            raise RuntimeError("session hasn't started, and root is None.")

        output = self._renderer.render(self._root)

        return output
