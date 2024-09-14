from __future__ import annotations

from typing import TypeVar, TYPE_CHECKING

from acte.context import Context
from acte.state.ref import Ref

if TYPE_CHECKING:
    from acte.state.effect import Effect

T = TypeVar('T')


class Signal(Ref[T]):
    def __init__(self, value: T | None) -> None:
        super().__init__(value)

        self._effect_list: list[Effect] = []

    @property
    def value(self) -> T | None:
        effect_stack = Context.get_effect_stack()

        # if no effect is running, return the value directly
        if len(effect_stack) == 0:
            return self._value

        # add this signal to the current effect
        current_effect = effect_stack[-1]
        if current_effect not in self._effect_list:
            # signal and effect add each other
            self.add_effect(current_effect)
            current_effect.add_signal(self)

        return self._value

    async def set(self, value: T | None) -> None:
        if self._value == value:
            return

        self._value = value

        prev_effect_list = self._effect_list

        # remove all effects and related signal
        self._effect_list = []
        for effect in prev_effect_list:
            effect.remove_signal(self)

        for effect in prev_effect_list:
            if effect.is_cancel is False:  # parent effect change may have cancelled child effect by its own
                await effect.call()

    def add_effect(self, effect: Effect) -> None:
        self._effect_list.append(effect)

    def remove_effect(self, effect: Effect) -> None:
        self._effect_list.remove(effect)
