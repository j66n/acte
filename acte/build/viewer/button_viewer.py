from typing import Callable, Awaitable, cast

from acte.build.type import Prop, to_ref
from acte.build.viewer.common.base import Base

from acte.node import Button
from acte.schema.schema import NullSchema
from acte.state import Compute, Ref, Signal, Effect


class ButtonViewer(Base):
    @classmethod
    def button(
            cls,
            content: Callable[[], str] | Prop[str] = '',
            on_press: Prop[Callable[[], Awaitable[None] | None]] | None = None,
            title: Callable[[], str] | Prop[str] | None = None,
    ) -> None:
        cls._check_skip()

        if callable(content):
            content = Compute(content)

        if callable(title):
            title = Compute(title)

        cls._append_awaitable(
            cls._button_constructor(
                content,
                title,
                on_press,
            )
        )

    @classmethod
    async def _button_constructor(
            cls,
            content: Prop[str],
            title: Prop[str] | None,
            on_press: Prop[Callable[[], Awaitable[None] | None]] | None,
    ) -> None:
        content = to_ref(content)
        if title is not None:
            title = to_ref(title)
        if on_press is not None:
            on_press = to_ref(on_press)

        node = Button()
        node.set_interactive_id(cls._generate_interactive_id())
        node.set_schema(NullSchema())

        await node.bind_content(content)

        if title is not None:
            async def _() -> None:
                schema = cast(NullSchema, node.schema)
                schema.set_title(title.value)

            e = await Effect.create(_)
            node.add_effect(e)

        if on_press is not None:
            await node.bind_on_press(on_press)

        cls._attach_to_container(node)
