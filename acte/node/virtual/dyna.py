from __future__ import annotations

from typing import Callable, Awaitable, Any, TYPE_CHECKING

from acte.node.virtual.virtual import Virtual
from acte.node.implement.container import Container
from acte.state import Effect

if TYPE_CHECKING:
    from acte.node import Cache


class Dyna(Virtual, Container):
    def __init__(self) -> None:
        Virtual.__init__(self)
        Container.__init__(self)

        self._view: Callable[[], None] = lambda: None

        self._cached_dict: dict[Any, Cache] = {}

    @property
    def view(self) -> Callable[[], None]:
        return self._view

    @property
    def cached_dict(self) -> dict[Any, Cache]:
        return self._cached_dict

    def set_cached_dict(self, value: dict[Any, Cache]) -> None:
        self._cached_dict = value

    async def bind_view(self, view: Callable[[], None], on_view_update: Callable[[], Awaitable[None]]) -> None:
        self._view = view

        async def _func() -> None:
            await on_view_update()

        e = await Effect.create(_func)
        self.add_effect(e)
