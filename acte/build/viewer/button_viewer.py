from typing import Callable, Awaitable

from acte.build.type import Prop, to_ref
from acte.build.viewer.common.base import Base

from acte.node import Button
from acte.state import Compute, Ref


class ButtonViewer(Base):
    @classmethod
    def button(
            cls,
            content: Callable[[], str] | Prop[str] = '',
            on_press: Prop[Callable[[], Awaitable[None] | None]] | None = None
    ) -> None:
        cls._check_skip()

        if callable(content):
            content = Compute(content)

        if on_press is None:
            def on_press() -> None:
                pass

        cls._append_awaitable(cls._button_constructor(content, on_press))

    @classmethod
    async def _button_constructor(
            cls,
            content: Prop[str],
            on_press: Prop[Callable[[], Awaitable[None] | None]]
    ) -> None:
        content = to_ref(content)
        on_press = to_ref(on_press)

        node = Button()
        node.set_interactive_id(cls._generate_interactive_id())

        await node.bind_content(content)
        await node.bind_on_press(on_press)

        cls._attach_to_container(node)
