from typing import Callable, Awaitable, TypeVar, Generic, Type, TypeAlias

from acte.node.element.inline.inline import Inline
from acte.node.implement.interactive import Interactive
from acte.state import Ref, Effect, Signal

T = TypeVar('T', str, int, float)

InputType: TypeAlias = Type[T]


class Input(Generic[T], Inline, Interactive):
    def __init__(self, input_type: InputType) -> None:
        Inline.__init__(self)
        Interactive.__init__(self)

        self._type: InputType = input_type

        self._name: str = ''
        self._value: T | None = None
        self._on_fill: Callable[[str], Awaitable[None] | None] = lambda a: None

    @property
    def type(self) -> InputType:
        return self._type

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> T | None:
        return self._value

    @property
    def on_fill(self) -> Callable[[str], Awaitable[None] | None]:
        return self._on_fill

    async def bind_name(self, name: Ref[str]) -> None:
        async def _func() -> None:
            self._name = name.value

        effect = await Effect.create(_func)

        self._effect_list.append(effect)

    async def bind_value(self, value: Signal[T]) -> None:
        async def _func() -> None:
            self._value = value.value

        effect = await Effect.create(_func)

        self._effect_list.append(effect)

    async def bind_on_fill(self, on_fill: Ref[Callable[[str], Awaitable[None] | None]]) -> None:
        async def _func() -> None:
            self._on_fill = on_fill.value

        effect = await Effect.create(_func)

        self._effect_list.append(effect)
