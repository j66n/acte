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
            title: Callable[[], str] | Prop[str] | None = None,
            enum: Prop[list[str]] | None = None,
    ) -> None:
        if callable(title):
            title = Compute(title)

        if title is not None:
            title = to_ref(title)

        if enum is not None:
            enum = to_ref(enum)

        schema = StrSchema()

        schema_attrs = {
            'title': title,
            'enum': enum,
        }

        cls._input(
            name,
            schema,
            schema_attrs,
            value,
            on_set,
        )

    @classmethod
    def input_int(
            cls,
            name: Callable[[], str] | Prop[str] = '',
            value: Prop[int] | None = None,
            on_set: Prop[Callable[[str], Awaitable[None] | None]] | None = None,
            title: Callable[[], str] | Prop[str] | None = None,
            enum: Prop[list[int]] | None = None,
    ) -> None:
        if callable(title):
            title = Compute(title)

        if title is not None:
            title = to_ref(title)

        if enum is not None:
            enum = to_ref(enum)

        schema = IntSchema()

        schema_attrs = {
            'title': title,
            'enum': enum,
        }

        cls._input(
            name,
            schema,
            schema_attrs,
            value,
            on_set,
        )

    @classmethod
    def input_float(
            cls,
            name: Callable[[], str] | Prop[str] = '',
            value: Signal[float] | None = None,
            on_set: Prop[Callable[[str], Awaitable[None] | None]] | None = None,
            title: Callable[[], str] | Prop[str] | None = None,
            enum: Prop[list[float]] | None = None,
    ) -> None:
        if callable(title):
            title = Compute(title)

        if title is not None:
            title = to_ref(title)

        if enum is not None:
            enum = to_ref(enum)

        schema = NumSchema()

        schema_attrs = {
            'title': title,
            'enum': enum,
        }

        cls._input(
            name,
            schema,
            schema_attrs,
            value,
            on_set,
        )

    @classmethod
    def input_bool(
            cls,
            name: Callable[[], str] | Prop[str] = '',
            value: Signal[bool] | None = None,
            on_set: Prop[Callable[[str], Awaitable[None] | None]] | None = None,
            title: Callable[[], str] | Prop[str] | None = None,
            enum: Prop[list[bool]] | None = None,
    ) -> None:
        if callable(title):
            title = Compute(title)

        if title is not None:
            title = to_ref(title)

        if enum is not None:
            enum = to_ref(enum)

        schema = BoolSchema()

        schema_attrs = {
            'title': title,
            'enum': enum,
        }

        cls._input(
            name,
            schema,
            schema_attrs,
            value,
            on_set,
        )

    @classmethod
    def _input(
            cls,
            name: Callable[[], str] | Prop[str],
            schema: Schema,
            schema_attrs: dict[str, Any],
            value: Prop[Any] | None,
            on_set: Prop[Callable[[str], Awaitable[None] | None]] | None,
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
                schema,
                schema_attrs,
                value,
                on_set,
            )
        )

    @classmethod
    async def _input_constructor(
            cls,
            name: Prop[str],
            schema: Schema,
            schema_attrs: dict[str, Any],
            value: Prop[Any],
            on_set: Prop[Callable[[str], Awaitable[None] | None]] | None,
    ) -> None:
        name = to_ref(name)
        value = to_ref(value)
        if on_set is not None:
            on_set = to_ref(on_set)

        node = Input()
        node.set_interactive_id(cls._generate_interactive_id())
        node.set_schema(schema)

        for k, v in schema_attrs.items():
            if v is None:
                continue

            async def _(_k=k, _v=v):
                async def __() -> None:
                    setter = getattr(schema, f'set_{_k}')
                    setter(_v.value)

                e = await Effect.create(__)
                node.add_effect(e)

            await _()

        await node.bind_name(name)
        await node.bind_value(value)
        if on_set is not None:
            await node.bind_on_set(on_set)

        cls._attach_to_container(node)
