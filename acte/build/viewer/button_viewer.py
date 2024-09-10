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
            schema: Prop[NullSchema] | None = None,
    ) -> None:
        cls._check_skip()

        if callable(content):
            content = Compute(content)

        if schema is None:
            schema = NullSchema()

        cls._append_awaitable(
            cls._button_constructor(
                content,
                schema,
                on_press,
            )
        )

    @classmethod
    async def _button_constructor(
            cls,
            content: Prop[str],
            schema: Prop[NullSchema],
            on_press: Prop[Callable[[], Awaitable[None] | None]] | None,
    ) -> None:
        content = to_ref(content)
        schema = to_ref(schema)
        on_press = to_ref(on_press)

        node = Button()
        node.set_interactive_id(cls._generate_interactive_id())

        await node.bind_content(content)
        await node.bind_schema(schema)

        if on_press is not None:
            await node.bind_on_press(on_press)

        cls._attach_to_container(node)
