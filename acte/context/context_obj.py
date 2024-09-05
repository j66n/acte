from __future__ import annotations

from typing import Awaitable, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from acte.node.implement.container import Container
    from acte.node.virtual.cache import Cache
    from acte.state.effect import Effect


class ContextObj:
    def __init__(self) -> None:
        # Used for view construction, component and dyna's view construction has two phases: sync and async
        self._awaitable_list_stack: list[list[Awaitable[None]]] = []

        # collect pending effects in sync phase, then call them in async phase
        self._pending_effect_list: list[Effect] = []

        # in async phase, track containers to ensure children are added to the correct container
        self._container_stack: list[Container] = []

        # in async phase, interactive count is used to define interactive id
        self._interactive_count: int = 0

        # in async phase, track calling effects because effects may be nested
        self._effect_stack: list[Effect] = []

        # skip when cached
        self._is_skip: bool = False

        # save new cache list for each dyna
        self._cache_dict_stack: list[dict[Any, Cache]] = []

    @property
    def awaitable_list_stack(self) -> list[list[Awaitable[None]]]:
        return self._awaitable_list_stack

    def set_awaitable_list_stack(self, awaitable_list_stack: list[list[Awaitable[None]]]) -> None:
        self._awaitable_list_stack = awaitable_list_stack

    @property
    def pending_effect_list(self) -> list[Effect]:
        return self._pending_effect_list

    def set_pending_effect_list(self, pending_effect_list: list[Effect]) -> None:
        self._pending_effect_list = pending_effect_list

    @property
    def container_stack(self) -> list[Container]:
        return self._container_stack

    def set_container_stack(self, container_stack: list[Container]) -> None:
        self._container_stack = container_stack

    @property
    def interactive_count(self) -> int:
        return self._interactive_count

    def set_interactive_count(self, interactive_count: int) -> None:
        self._interactive_count = interactive_count

    @property
    def effect_stack(self) -> list[Effect]:
        return self._effect_stack

    def set_effect_stack(self, effect_stack: list[Effect]) -> None:
        self._effect_stack = effect_stack

    @property
    def is_skip(self) -> bool:
        return self._is_skip

    def set_is_skip(self, is_skip: bool) -> None:
        self._is_skip = is_skip

    @property
    def cache_dict_stack(self) -> list[dict[Any, Cache]]:
        return self._cache_dict_stack

    def set_cache_dict_stack(self, cache_dict_stack: list[dict[Any, Cache]]) -> None:
        self._cache_dict_stack = cache_dict_stack
