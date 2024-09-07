from __future__ import annotations

import contextlib
from typing import Any, Iterator, cast, Container

from acte.build.viewer.common.exception import SkipException
from acte.build.viewer.common.base import Base

from acte.node import Cache


class CacheViewer(Base):
    @classmethod
    @contextlib.contextmanager
    def cache(cls, identifier: Any, permanent: bool = False) -> Iterator[None]:
        cls._check_skip()

        cached = cls._get_cached(identifier)

        if cached is None:
            cls._append_awaitable(cls._enter_new_cache_constructor(identifier, permanent))
        else:
            cls._append_awaitable(cls._enter_cached_constructor(cached))

            cls._set_skip()
            cls._add_new_cache(cached)

        try:
            yield
        except SkipException:
            pass

        finally:
            cls._append_awaitable(cls._leave_cache_constructor())

    @classmethod
    async def _enter_new_cache_constructor(cls, identifier: Any, permanent: bool) -> None:
        cache = Cache(identifier, permanent)
        cls._add_cached(cache)  # execute during await cls._call_awaitable_list(), so add to cached

        cls._append_container(cache)

    @classmethod
    async def _enter_cached_constructor(cls, cached: Cache) -> None:
        cls._append_container(cached)

    @classmethod
    async def _leave_cache_constructor(cls) -> None:
        node = cls._pop_container_node()
        cls._attach_to_container(node)
