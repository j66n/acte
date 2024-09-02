from typing import Callable

from acte.build.viewer.common.base import Base
from acte.node import Dyna


class DynaViewer(Base):
    @classmethod
    def dyna(cls, func: Callable[[], None]) -> None:
        cls._check_skip()

        def decorator(view: Callable[[], None]) -> None:
            cls._append_awaitable(cls._dyna_constructor(view))

        return decorator(func)

    @classmethod
    async def _dyna_constructor(cls, view: Callable[[], None]) -> None:
        node = Dyna()

        async def _on_view_update() -> None:
            cls._append_container(node)

            cls._append_new_awaitable_list()

            cls._append_new_cache_dict()

            view()

            # start: remove children and unmount non-cache children, exclude permanent
            new_cache_dict = cls._pop_new_cache_dict()

            # start: add permanent cache to new_cache_dict
            for identifier, cache in node.cached_dict:
                if cache.permanent and (identifier not in new_cache_dict):
                    new_cache_dict[identifier] = cache
            # end: add permanent cache to new_cache_dict

            node.set_cached_dict(new_cache_dict)

            cached_list = list(new_cache_dict.values())

            while len(node.children) != 0:
                child = node.children.pop(0)

                if child not in cached_list:
                    child.unmount(cached_list)
            # end: remove children and unmount non-cache children

            await cls._async_init(node)
            await cls._call_awaitable_list()

            cls._pop_awaitable_list()

            cls._pop_container_node()

        await node.bind_view(view, _on_view_update)

        cls._attach_to_container(node)
