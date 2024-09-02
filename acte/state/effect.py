from __future__ import annotations

import inspect
from typing import Callable, Awaitable, TypeVar, Any

from acte.state.signal import Signal
from acte.context.context import Context

T = TypeVar('T')


class Effect:
    def __init__(self, func: Callable[[], Awaitable[None] | None]) -> None:
        self._func = func

        self._signal_list: list[Signal[Any]] = []
        self._effect_children: list[Effect] = []

        self._is_pending = True
        self._is_cancel = False

        pending_effect_list = Context.get_pending_effect_list()
        pending_effect_list.append(self)

    @classmethod
    async def create(cls, func: Callable[[], Awaitable[None] | None]) -> Effect:
        e = Effect(func)
        await e.async_init()
        return e

    @property
    def is_pending(self) -> bool:
        return self._is_pending

    @property
    def is_cancel(self) -> bool:
        return self._is_cancel

    async def async_init(self) -> None:
        if self._is_pending is False:
            raise ValueError("Effect is not pending")

        async_init_list = Context.get_pending_effect_list()
        async_init_list.remove(self)

        await self.call()

        self._is_pending = False

    async def reset(self) -> None:
        if self._is_cancel is True:
            raise ValueError("Effect is canceled, cannot reset")

        if self._is_pending is True:
            raise ValueError("Effect is pending, cannot reset")

        self.cancel()

        self._is_cancel = False
        self._is_pending = True

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

        self._is_pending = False
        self._is_cancel = True
