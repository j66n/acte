from __future__ import annotations

import inspect
from typing import Callable, Awaitable, TypeVar, Any

from acte.state.signal import Signal
from acte.context import Context

T = TypeVar('T')


class Effect:
    def __init__(self, func: Callable[[], Awaitable[None] | None], is_async: bool = False) -> None:
        if not is_async:
            raise TypeError("Cannot instantiate directly. Use 'create' classmethod.")

        self._func = func

        self._signal_list: list[Signal[Any]] = []
        self._effect_children: list[Effect] = []

        self._is_cancel = False

    @classmethod
    async def create(cls, func: Callable[[], Awaitable[None] | None]) -> Effect:
        e = Effect(func, True)
        await e.call()
        return e

    @property
    def is_cancel(self) -> bool:
        return self._is_cancel

    async def reset(self) -> None:
        if self._is_cancel is True:
            raise ValueError("Effect is canceled, cannot reset")

        self.cancel()

        self._is_cancel = False

        await self.call()

    async def call(self) -> None:
        if self._is_cancel is True:
            raise ValueError("Effect is canceled, cannot call")

        effect_stack = Context.get_effect_stack()

        # add this effect to its parent effect's children
        parent_effect = effect_stack[-1] if len(effect_stack) > 0 else None
        if parent_effect is not None:
            parent_effect._effect_children.append(self)

        # call this effect
        effect_stack.append(self)

        if inspect.iscoroutinefunction(self._func):
            await self._func()
        else:
            self._func()

        effect_stack.pop()

    def add_signal(self, signal: Signal[Any]) -> None:
        self._signal_list.append(signal)

    def remove_signal(self, signal: Signal[Any]) -> None:
        self._signal_list.remove(signal)

    def cancel(self) -> None:
        if self._is_cancel is True:
            raise ValueError("Effect is already canceled")

        # cancel effect children
        for effect in self._effect_children:
            if effect.is_cancel is False:  # parent effect change may have cancelled child effect by its own
                effect.cancel()

        self._effect_children = []

        # remove this effect from all signals
        for signal in self._signal_list:
            signal.remove_effect(self)
            self._signal_list.remove(signal)

        self._is_cancel = True
