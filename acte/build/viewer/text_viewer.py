from collections.abc import Callable

from acte.build.type import Prop, to_ref
from acte.build.viewer.common.base import Base
from acte.node import Text
from acte.state import Compute, Ref


class TextViewer(Base):
    @classmethod
    def text(cls, content: Callable[[], str] | Prop[str]) -> None:
        cls._check_skip()

        if callable(content):
            content = Compute(content)

        cls._append_awaitable(cls._text_constructor(content))

    @classmethod
    async def _text_constructor(cls, content: Prop[str]) -> None:
        content = to_ref(content)

        node = Text()
        await node.bind_content(content)

        cls._attach_to_container(node)
