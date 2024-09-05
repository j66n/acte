from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, Awaitable

from acte.context.context_obj import ContextObj

if TYPE_CHECKING:
    from acte.node import Cache
    from acte.node.implement import Container
    from acte.state.effect import Effect


class Context:
    _context_obj: ContextVar[ContextObj] = ContextVar("context_obj", default=None)

    @classmethod
    def use(cls, c: ContextObj) -> None:
        cls._context_obj.set(c)

    @classmethod
    def get_awaitable_list_stack(cls) -> list[list[Awaitable[None]]]:
        if cls._context_obj.get() is None:
            raise ValueError("context_obj is None")

        return cls._context_obj.get().awaitable_list_stack

    @classmethod
    def get_pending_effect_list(cls) -> list[Effect]:
        if cls._context_obj is None:
            raise ValueError("context_obj is None")

        return cls._context_obj.get().pending_effect_list

    @classmethod
    def get_container_stack(cls) -> list[Container]:
        if cls._context_obj is None:
            raise ValueError("context_obj is None")

        return cls._context_obj.get().container_stack

    @classmethod
    def get_interactive_count(cls) -> int:
        if cls._context_obj is None:
            raise ValueError("context_obj is None")

        return cls._context_obj.get().interactive_count

    @classmethod
    def set_interactive_count(cls, count: int) -> None:
        if cls._context_obj is None:
            raise ValueError("context_obj is None")

        cls._context_obj.get().set_interactive_count(count)

    @classmethod
    def get_effect_stack(cls) -> list[Effect]:
        if cls._context_obj is None:
            raise ValueError("context_obj is None")

        return cls._context_obj.get().effect_stack

    @classmethod
    def get_is_skip(cls) -> bool:
        if cls._context_obj is None:
            raise ValueError("context_obj is None")

        return cls._context_obj.get().is_skip

    @classmethod
    def set_is_skip(cls, is_skip: bool) -> None:
        if cls._context_obj is None:
            raise ValueError("context_obj is None")

        cls._context_obj.get().set_is_skip(is_skip)

    @classmethod
    def get_cache_dict_stack(cls) -> list[dict[Any, Cache]]:
        if cls._context_obj is None:
            raise ValueError("context_obj is None")

        return cls._context_obj.get().cache_dict_stack
