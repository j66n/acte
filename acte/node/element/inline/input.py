from typing import Callable, Awaitable, TypeVar, Generic, Type, TypeAlias, Any

from acte.node.element.inline.inline import Inline
from acte.node.implement.interactive import Interactive
from acte.schema.schema import Schema
from acte.state import Ref, Effect, Signal


class Input(Inline, Interactive):
    def __init__(self) -> None:
        Inline.__init__(self)
        Interactive.__init__(self)

        self._name: str = ''
        self._schema: Schema | None = None
        self._value: Any = None
        self._on_set: Callable[[str], Awaitable[None] | None] | None = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def schema(self) -> Schema | None:
        return self._schema

    @property
    def value(self) -> Any:
        return self._value

    @property
    def on_set(self) -> Callable[[str], Awaitable[None] | None] | None:
        return self._on_set

    async def bind_name(self, name: Ref[str]) -> None:
        async def _func() -> None:
            v = name.value
            if v is None:
                v = ""

            self._name = v

        effect = await Effect.create(_func)

        self._effect_list.append(effect)

    def set_schema(self, schema: Schema) -> None:
        self._schema = schema

    async def bind_value(self, value: Ref[Any]) -> None:
        async def _func() -> None:
            self._value = value.value

        effect = await Effect.create(_func)

        self._effect_list.append(effect)

    async def bind_on_set(self, on_set: Ref[Callable[[str], Awaitable[None] | None]]) -> None:
        async def _func() -> None:
            self._on_set = on_set.value

        effect = await Effect.create(_func)

        self._effect_list.append(effect)
