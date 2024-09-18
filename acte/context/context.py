from __future__ import annotations

from contextvars import ContextVar, Token
from typing import TYPE_CHECKING, Any, Awaitable

from acte.context.context_obj import ContextObj

if TYPE_CHECKING:
    from acte.node import Cache
    from acte.node.implement import Container
    from acte.state import Effect


class Context:
    _context_obj: ContextVar[ContextObj | None] = ContextVar("context_obj", default=None)

    @classmethod
    def use(cls, c: ContextObj) -> Token:
        token = cls._context_obj.set(c)
        return token

    @classmethod
    def reset(cls, token: Token) -> None:
        cls._context_obj.reset(token)

    @classmethod
    def get_awaitable_list_stack(cls) -> list[list[Awaitable[None]]]:
        context = cls._context_obj.get()

        if isinstance(context, ContextObj):
            return context.awaitable_list_stack
        else:
            raise ValueError("context_obj is None")

    @classmethod
    def get_container_stack(cls) -> list[Container]:
        context = cls._context_obj.get()

        if isinstance(context, ContextObj):
            return context.container_stack
        else:
            raise ValueError("context_obj is None")

    @classmethod
    def get_interactive_count(cls) -> int:
        context = cls._context_obj.get()

        if isinstance(context, ContextObj):
            return context.interactive_count
        else:
            raise ValueError("context_obj is None")

    @classmethod
    def set_interactive_count(cls, count: int) -> None:
        context = cls._context_obj.get()

        if isinstance(context, ContextObj):
            context.set_interactive_count(count)
        else:
            raise ValueError("context_obj is None")

    @classmethod
    def get_effect_stack(cls) -> list[Effect]:
        context = cls._context_obj.get()

        if isinstance(context, ContextObj):
            return context.effect_stack
        else:
            raise ValueError("context_obj is None")

    @classmethod
    def get_is_skip(cls) -> bool:
        context = cls._context_obj.get()

        if isinstance(context, ContextObj):
            return context.is_skip
        else:
            raise ValueError("context_obj is None")

    @classmethod
    def set_is_skip(cls, is_skip: bool) -> None:
        context = cls._context_obj.get()

        if isinstance(context, ContextObj):
            context.set_is_skip(is_skip)
        else:
            raise ValueError("context_obj is None")

    @classmethod
    def get_cache_dict_stack(cls) -> list[dict[Any, Cache]]:
        context = cls._context_obj.get()

        if isinstance(context, ContextObj):
            return context.cache_dict_stack
        else:
            raise ValueError("context_obj is None")
