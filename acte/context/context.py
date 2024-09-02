from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, Awaitable

if TYPE_CHECKING:
    from acte.node import Cache
    from acte.node.implement import Container
    from acte.state.effect import Effect


class Context:
    # Used for view construction, component and dyna's view construction has two phases: sync and async
    _awaitable_list_stack: ContextVar[list[list[Awaitable[None]]]] | None = None

    # collect pending effects in sync phase, then call them in async phase
    _pending_effect_list: ContextVar[list[Effect]] | None = None

    # in async phase, track containers to ensure children are added to the correct container
    _container_stack: ContextVar[list[Container]] | None = None

    # in async phase, interactive count is used to define interactive id
    _interactive_count: ContextVar[int] | None = None

    # in async phase, track calling effects because effects may be nested
    _effect_stack: ContextVar[list[Effect]] | None = None

    # skip when cached
    _is_skip: ContextVar[bool] | None = None

    # save new cache list for each dyna
    _cache_dict_stack: ContextVar[list[dict[Any, Cache]]] | None = None

    def __init__(self) -> None:
        self._awaitable_list_stack: ContextVar[list[list[Awaitable[None]]]] = (
            ContextVar('_awaitable_list_stack', default=[]))
        self._pending_effect_list: ContextVar[list[Effect]] = ContextVar('_pending_init_list', default=[])
        self._container_stack: ContextVar[list[Container]] = ContextVar('_container_stack', default=[])
        self._interactive_count: ContextVar[int] = ContextVar('_interactive_count', default=0)
        self._effect_stack: ContextVar[list[Effect]] = ContextVar('_effect_stack', default=[])
        self._is_skip: ContextVar[bool] = ContextVar('_is_skip', default=False)
        self._cache_dict_stack: ContextVar[list[dict[Any, Cache]]] = ContextVar('_cache_dict_stack', default=[])

    @classmethod
    def use(cls, c: Context) -> None:
        cls._awaitable_list_stack = c._awaitable_list_stack
        cls._pending_effect_list = c._pending_effect_list
        cls._container_stack = c._container_stack
        cls._interactive_count = c._interactive_count
        cls._effect_stack = c._effect_stack
        cls._is_skip = c._is_skip
        cls._cache_dict_stack = c._cache_dict_stack

    @classmethod
    def get_awaitable_list_stack(cls) -> list[list[Awaitable[None]]]:
        if cls._awaitable_list_stack is None:
            raise ValueError("awaitable list stack is None")

        return cls._awaitable_list_stack.get()

    @classmethod
    def get_pending_effect_list(cls) -> list[Effect]:
        if cls._pending_effect_list is None:
            raise ValueError("pending effect list is None")

        return cls._pending_effect_list.get()

    @classmethod
    def get_container_stack(cls) -> list[Container]:
        if cls._container_stack is None:
            raise ValueError("container stack is None")

        return cls._container_stack.get()

    @classmethod
    def get_interactive_count(cls) -> int:
        if cls._interactive_count is None:
            raise ValueError("interactive count is None")

        return cls._interactive_count.get()

    @classmethod
    def set_interactive_count(cls, count: int) -> None:
        if cls._interactive_count is None:
            raise ValueError("interactive count is None")

        cls._interactive_count.set(count)

    @classmethod
    def get_effect_stack(cls) -> list[Effect]:
        if cls._effect_stack is None:
            raise ValueError("effect stack is None")

        return cls._effect_stack.get()

    @classmethod
    def get_is_skip(cls) -> bool:
        if cls._is_skip is None:
            raise ValueError("is skip is None")

        return cls._is_skip.get()

    @classmethod
    def set_is_skip(cls, is_skip: bool) -> None:
        if cls._is_skip is None:
            raise ValueError("is skip is None")

        cls._is_skip.set(is_skip)

    @classmethod
    def get_cache_dict_stack(cls) -> list[dict[Any, Cache]]:
        if cls._cache_dict_stack is None:
            raise ValueError("cache dict stack is None")

        return cls._cache_dict_stack.get()
