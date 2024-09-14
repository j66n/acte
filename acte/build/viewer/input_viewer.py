from typing import Callable, Awaitable, cast, Any

from acte.node import Input
from acte.schema import Schema, StrSchema
from acte.state import Signal, Compute

from acte.build.type import Prop, to_ref
from acte.build.viewer.common.base import Base


class InputViewer(Base):
    @classmethod
    def input(
            cls,
            name: Callable[[], str] | Prop[str] = '',
            value: Prop[Any] | None = None,
            on_set: Prop[Callable[[Any], Awaitable[None] | None]] | None = None,
            schema: Prop[Schema] | None = None,
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

        if schema is None:
            schema = StrSchema()

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
            on_set: Prop[Callable[[Any], Awaitable[None] | None]] | None,
            schema: Prop[Schema],
    ) -> None:
        name = to_ref(name)
        value = to_ref(value)
        on_set = to_ref(on_set)
        schema = to_ref(schema)

        node = Input()
        node.set_interactive_id(cls._generate_interactive_id())

        await node.bind_name(name)
        await node.bind_value(value)
        await node.bind_on_set(on_set)
        await node.bind_schema(schema)

        cls._attach_to_container(node)
