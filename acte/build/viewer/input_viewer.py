from typing import Callable, Awaitable, cast, Any, TypeVar, Type

from acte.build.type import Prop, to_ref
from acte.build.viewer.common.base import Base

from acte.node import Input, InputKind
from acte.state import Signal, Compute, Ref

T = TypeVar('T')


class InputViewer(Base):
    @classmethod
    def input_str(
            cls,
            name: Callable[[], str] | Prop[str] = '',
            value: Prop[str] | None = None,
            on_fill: Prop[Callable[[str], Awaitable[None] | None]] | None = None,
            hint: Callable[[], str] | Prop[str] = '',
            enum: Prop[list[str]] | None = None,
    ) -> None:
        cls._input(
            str,
            name,
            value,
            on_fill,
            hint,
            enum,
        )

    @classmethod
    def input_int(
            cls,
            name: Callable[[], str] | Prop[str] = '',
            value: Prop[int] | None = None,
            on_fill: Prop[Callable[[str], Awaitable[None] | None]] | None = None,
            hint: Callable[[], str] | Prop[str] = '',
            enum: Prop[list[int]] | None = None,
    ) -> None:
        cls._input(
            int,
            name,
            value,
            on_fill,
            hint,
            enum,
        )

    @classmethod
    def input_float(
            cls,
            name: Callable[[], str] | Prop[str] = '',
            value: Signal[float] | None = None,
            on_fill: Prop[Callable[[str], Awaitable[None] | None]] | None = None,
            hint: Callable[[], str] | Prop[str] = '',
            enum: Prop[list[float]] | None = None,
    ) -> None:
        cls._input(
            float,
            name,
            value,
            on_fill,
            hint,
            enum,
        )

    @classmethod
    def input_bool(
            cls,
            name: Callable[[], str] | Prop[str] = '',
            value: Signal[bool] | None = None,
            on_fill: Prop[Callable[[str], Awaitable[None] | None]] | None = None,
            hint: Callable[[], str] | Prop[str] = '',
            enum: Prop[list[bool]] | None = None,
    ) -> None:
        cls._input(
            bool,
            name,
            value,
            on_fill,
            hint,
            enum,
        )

    @classmethod
    def _input(
            cls,
            input_kind: InputKind,
            name: Callable[[], str] | Prop[str],
            value: Prop[T] | None,
            on_fill: Prop[Callable[[str], Awaitable[None] | None]] | None,
            hint: Callable[[], str] | Prop[str],
            enum: Prop[list[T]] | None,
    ) -> None:
        cls._check_skip()

        if callable(name):
            name = Compute(name)

        if value is None:
            value = Signal(None)

        if (on_fill is None) and (not isinstance(value, Signal)):
            value = cast(Signal, value)

            async def on_fill(v: str) -> None:
                if v == '':
                    await value.set(None)
                else:
                    await value.set(input_kind(v))

        if on_fill is None:
            on_fill = Ref(None)

        if callable(hint):
            hint = Compute(hint)

        if enum is None:
            enum = Ref(None)

        cls._append_awaitable(
            cls._input_constructor(
                input_kind,
                name,
                value,
                on_fill,
                hint,
                enum,
            )
        )

    @classmethod
    async def _input_constructor(
            cls,
            kind: InputKind,
            name: Prop[str],
            value: Prop[Any],
            on_fill: Prop[Callable[[str], Awaitable[None] | None]],
            hint: Prop[str],
            enum: Prop[list[Any]],
    ) -> None:
        name = to_ref(name)
        value = to_ref(value)
        on_fill = to_ref(on_fill)
        hint = to_ref(hint)
        enum = to_ref(enum)

        node = Input(kind)
        node.set_interactive_id(cls._generate_interactive_id())

        await node.bind_name(name)
        await node.bind_value(value)
        await node.bind_on_fill(on_fill)
        await node.bind_hint(hint)
        await node.bind_enum(enum)

        cls._attach_to_container(node)
