from typing import Callable, Awaitable, cast, Any

from acte.build.type import Prop, to_ref
from acte.build.viewer.common.base import Base

from acte.node import Input
from acte.schema.schema import StrSchema, Schema, IntSchema, NumSchema, BoolSchema
from acte.state import Signal, Compute, Effect


class InputViewer(Base):
    @classmethod
    def input_str(
            cls,
            name: Callable[[], str] | Prop[str] = '',
            value: Prop[str] | None = None,
            on_set: Prop[Callable[[str], Awaitable[None] | None]] | None = None,
            schema: StrSchema | None = None,
    ) -> None:
        if schema is None:
            schema = StrSchema()

        cls._input(
            name,
            value,
            on_set,
            schema,
        )

    @classmethod
    def input_int(
            cls,
            name: Callable[[], str] | Prop[str] = '',
            value: Prop[int] | None = None,
            on_set: Prop[Callable[[str], Awaitable[None] | None]] | None = None,
            schema: IntSchema | None = None,
    ) -> None:
        if schema is None:
            schema = IntSchema()

        cls._input(
            name,
            value,
            on_set,
            schema,
        )

    @classmethod
    def input_float(
            cls,
            name: Callable[[], str] | Prop[str] = '',
            value: Signal[float] | None = None,
            on_set: Prop[Callable[[str], Awaitable[None] | None]] | None = None,
            schema: NumSchema | None = None,
    ) -> None:
        if schema is None:
            schema = NumSchema()

        cls._input(
            name,
            value,
            on_set,
            schema,
        )

    @classmethod
    def input_bool(
            cls,
            name: Callable[[], str] | Prop[str] = '',
            value: Signal[bool] | None = None,
            on_set: Prop[Callable[[str], Awaitable[None] | None]] | None = None,
            schema: BoolSchema | None = None,
    ) -> None:
        if schema is None:
            schema = BoolSchema()

        cls._input(
            name,
            value,
            on_set,
            schema,
        )

    @classmethod
    def _input(
            cls,
            name: Callable[[], str] | Prop[str],
            value: Prop[Any] | None,
            on_set: Prop[Callable[[str], Awaitable[None] | None]] | None,
            schema: Schema,
    ) -> None:
        cls._check_skip()

        if callable(name):
            name = Compute(name)

        if value is None:
            value = Signal(None)

        if (on_set is None) and isinstance(value, Signal):
            value = cast(Signal, value)

            async def on_set(v: Any) -> None:
                await value.set(v)

        cls._append_awaitable(
            cls._input_constructor(
                name,
                value,
                on_set,
                schema,
            )
        )

    @classmethod
    async def _input_constructor(
            cls,
            name: Prop[str],
            value: Prop[Any],
            on_set: Prop[Callable[[str], Awaitable[None] | None]] | None,
            schema: Schema,
    ) -> None:
        name = to_ref(name)
        value = to_ref(value)
        if on_set is not None:
            on_set = to_ref(on_set)

        node = Input()
        node.set_interactive_id(cls._generate_interactive_id())
        node.set_schema(schema)

        await node.bind_name(name)
        await node.bind_value(value)
        if on_set is not None:
            await node.bind_on_set(on_set)

        cls._attach_to_container(node)
