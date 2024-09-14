import contextlib
from typing import Iterator

from acte.node import Div

from acte.build.viewer.common.base import Base


class DivViewer(Base):
    @classmethod
    @contextlib.contextmanager
    def div(cls) -> Iterator[None]:
        cls._check_skip()

        cls._append_awaitable(cls._enter_div_constructor())

        try:
            yield
        finally:

            cls._append_awaitable(cls._leave_div_constructor())

    @classmethod
    async def _enter_div_constructor(cls) -> None:
        node = Div()

        cls._append_container(node)

    @classmethod
    async def _leave_div_constructor(cls) -> None:
        node = cls._pop_container_node()
        cls._attach_to_container(node)
