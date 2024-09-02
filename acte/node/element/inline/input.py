from enum import Enum
from typing import Callable, Awaitable, Any

from acte.node.element.inline.inline import Inline
from acte.node.implement.interactive import Interactive
from acte.state import Ref, Effect, Signal


class InputType(Enum):
    TEXT = "text"
    INT = "int"
    FLOAT = "float"


class Input(Inline, Interactive):
    def __init__(self, input_type: InputType) -> None:
        Inline.__init__(self)
        Interactive.__init__(self)

        self._type: InputType = input_type

        self._name: str = ''
        self._value: str = ''
        self._on_fill: Callable[[str, str], Awaitable[None] | None] = lambda a, b: None

    @property
    def type(self) -> InputType:
        return self._type

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> str:
        return self._value

    @property
    def on_fill(self) -> Callable[[str, str], Awaitable[None] | None]:
        return self._on_fill

    async def bind_name(self, name: Ref[str]) -> None:
        async def _func() -> None:
            self._name = name.value

        effect = await Effect.create(_func)

        self._effect_list.append(effect)

    async def bind_value(self, value: Signal[Any]) -> None:
        async def _func() -> None:
            if value.value is None:
                self._value = ''
            else:
                self._value = str(value.value)

        effect = await Effect.create(_func)

        self._effect_list.append(effect)

    async def bind_on_fill(self, on_fill: Ref[Callable[[str], Awaitable[None] | None]]) -> None:
        async def _func() -> None:
            self._on_fill = on_fill.value

        effect = await Effect.create(_func)

        self._effect_list.append(effect)
