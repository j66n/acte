import inspect
from typing import Callable, TypeVar, cast, Awaitable

from acte.state.effect import Effect
from acte.state.signal import Signal
from acte.state.ref import Ref

T = TypeVar('T')


class Memo(Ref[T]):
    # noinspection PyMissingConstructor
    def __init__(self, func: Callable[[], Awaitable[T] | T]) -> None:
        self._func = func
        self._signal: Signal[T] | None = None

        async def _effect_func() -> None:
            if inspect.iscoroutinefunction(self._func):
                value = await self._func()
            else:
                value = self._func()

            if self._signal is None:
                self._signal = Signal(value)
            else:
                await self._signal.set(value)

        self._effect = Effect(_effect_func)

    @property
    def effect(self) -> Effect:
        return self._effect

    @property
    def value(self) -> T | None:
        signal = cast(Signal[T], self._signal)

        return signal.value

    def cancel(self) -> None:
        if self._effect.is_cancel is True:
            raise ValueError("Memo is already canceled")

        self._effect.cancel()
