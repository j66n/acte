from typing import Callable, Awaitable, cast, Any, Type

from acte.build.type import Prop, to_ref
from acte.build.viewer.common.base import Base

from acte.node import Input, InputType
from acte.state import Signal, Compute


class InputViewer(Base):
    @classmethod
    def input_str(
            cls,
            name: Callable[[], str] | Prop[str] = '',
            value: Signal[str] | None = None,
            on_fill: Prop[Callable[[str], Awaitable[None] | None]] | None = None,
    ) -> None:
        cls._check_skip()

        if callable(name):
            name = Compute(name)

        if value is None:
            value = Signal[str](None)

        if on_fill is None:
            async def on_fill(v: str) -> None:
                await value.set(v)

        cls._append_awaitable(
            cls._input_constructor(
                str,
                name,
                value,
                on_fill,
            )
        )

    @classmethod
    def input_int(
            cls,
            name: Callable[[], str] | Prop[str] = '',
            value: Signal[int] | None = None,
            on_fill: Prop[Callable[[str], Awaitable[None] | None]] | None = None,
    ) -> None:
        cls._check_skip()

        if callable(name):
            name = Compute(name)

        if value is None:
            value = Signal[int](None)

        if on_fill is None:
            async def on_fill(v: str) -> None:
                if v == '':
                    await value.set(None)
                else:
                    await value.set(int(v))

        cls._append_awaitable(
            cls._input_constructor(
                int,
                name,
                value,
                on_fill,
            )
        )

    @classmethod
    def input_float(
            cls,
            name: Callable[[], str] | Prop[str] = '',
            value: Signal[float] | None = None,
            on_fill: Prop[Callable[[str], Awaitable[None] | None]] | None = None,
    ) -> None:
        cls._check_skip()

        if callable(name):
            name = Compute(name)

        if value is None:
            value = Signal[float](None)

        if on_fill is None:
            async def on_fill(v: str) -> None:
                if v == '':
                    await value.set(None)
                else:
                    await value.set(float(v))

        cls._append_awaitable(
            cls._input_constructor(
                float,
                name,
                value,
                on_fill,
            )
        )

    @classmethod
    async def _input_constructor(
            cls,
            input_type: InputType,
            name: Prop[str],
            value: Signal[Any],
            on_fill: Prop[Callable[[str], Awaitable[None] | None]],
    ) -> None:
        name = to_ref(name)
        on_fill = to_ref(on_fill)

        node = Input[input_type](input_type)
        node.set_interactive_id(cls._generate_interactive_id())

        await node.bind_name(name)
        await node.bind_value(value)
        await node.bind_on_fill(on_fill)

        cls._attach_to_container(node)
