from __future__ import annotations

from typing import Awaitable, cast, Any

from acte.build.viewer.common.exception import SkipException
from acte.node import Node, Cache, Dyna
from acte.node.implement import Container
from acte.context.context import Context


class Base:
    @classmethod
    def _append_container(cls, container: Container) -> None:
        container_stack = Context.get_container_stack()
        container_stack.append(container)

    @classmethod
    def _pop_container(cls) -> Container:
        container_stack = Context.get_container_stack()
        return container_stack.pop()

    @classmethod
    def _pop_container_node(cls) -> Node:
        container_stack = Context.get_container_stack()
        container = container_stack.pop()
        return cast(Node, container)

    @classmethod
    def _attach_to_container(cls, node: Node) -> None:
        container_stack = Context.get_container_stack()
        container_stack[-1].children.append(node)

    @classmethod
    def _get_dyna(cls) -> Dyna | None:
        nearest_dyna_node = None
        for container in reversed(Context.get_container_stack()):
            if isinstance(container, Dyna):
                nearest_dyna_node = container
                break

        return nearest_dyna_node

    @classmethod
    def _get_cached(cls, identifier: Any) -> Cache | None:
        dyna_node = cls._get_dyna()
        if dyna_node is not None:
            cache_dict = dyna_node.cached_dict
            return cache_dict.get(identifier)

        return None

    @classmethod
    def _add_cached(cls, cache: Cache) -> None:
        dyna_node = cls._get_dyna()
        if dyna_node is not None:
            cache_dict = dyna_node.cached_dict
            if cache.identifier in cache_dict:
                raise ValueError(f"Duplicated cache identifier: {cache.identifier}")
            cache_dict[cache.identifier] = cache

    @classmethod
    def _add_new_cache(cls, cache: Cache) -> None:
        cache_dict = cls._get_cache_dict()
        cache_dict[cache.identifier] = cache

    @classmethod
    def _append_new_cache_dict(cls) -> None:
        cache_list_stack = Context.get_cache_dict_stack()
        cache_list_stack.append({})

    @classmethod
    def _pop_new_cache_dict(cls) -> dict[Any, Cache]:
        return Context.get_cache_dict_stack().pop()

    @classmethod
    def _get_cache_dict(cls) -> dict[Any, Cache]:
        return Context.get_cache_dict_stack()[-1]

    @classmethod
    def _append_new_awaitable_list(cls) -> None:
        awaitable_list_stack = Context.get_awaitable_list_stack()
        awaitable_list_stack.append([])

    @classmethod
    def _pop_awaitable_list(cls) -> list[Awaitable[None]]:
        awaitable_list_stack = Context.get_awaitable_list_stack()
        return awaitable_list_stack.pop()

    @classmethod
    async def _call_awaitable_list(cls) -> None:
        awaitable_list = Context.get_awaitable_list_stack()[-1]
        for sub in awaitable_list:
            await sub

    @classmethod
    def _append_awaitable(cls, awaitable: Awaitable[None]) -> None:
        awaitable_list = Context.get_awaitable_list_stack()[-1]
        awaitable_list.append(awaitable)

    @classmethod
    def _generate_interactive_id(cls) -> str:
        interactive_id = Context.get_interactive_count()
        Context.set_interactive_count(interactive_id + 1)
        return str(interactive_id)

    @classmethod
    async def _async_init(cls, node: Node) -> None:
        pending_effect_list = Context.get_pending_effect_list()

        for e in pending_effect_list:  # just add top level effect, not children
            node.add_effect(e)

        for e in pending_effect_list:
            await e.async_init()

    @classmethod
    def _set_skip(cls) -> None:
        Context.set_is_skip(True)

    @classmethod
    def _check_skip(cls) -> None:
        if Context.get_is_skip() is True:
            Context.set_is_skip(False)
            raise SkipException()
