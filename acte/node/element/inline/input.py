from typing import Callable, Awaitable, Any

from acte.schema import Schema
from acte.state import Ref, Effect

from acte.node.element.inline.inline import Inline
from acte.node.implement.interactive import Interactive


class Input(Inline, Interactive):
    def __init__(self) -> None:
        Inline.__init__(self)
        Interactive.__init__(self)

        self._name: str = ''
        self._schema: Schema | None = None
        self._value: Any = None
        self._on_set: Callable[[Any], Awaitable[None] | None] | None = None

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

    async def bind_schema(self, schema: Ref[Schema]) -> None:
        async def _func() -> None:
            self._schema = schema.value

        effect = await Effect.create(_func)

        self._effect_list.append(effect)

    async def bind_value(self, value: Ref[Any]) -> None:
        async def _func() -> None:
            self._value = value.value

        effect = await Effect.create(_func)

        self._effect_list.append(effect)

    async def bind_on_set(self, on_set: Ref[Callable[[Any], Awaitable[None] | None]]) -> None:
        async def _func() -> None:
            self._on_set = on_set.value

        effect = await Effect.create(_func)

        self._effect_list.append(effect)
