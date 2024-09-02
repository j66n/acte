from typing import Callable, TypeVar

from acte.state.ref import Ref

T = TypeVar('T')


class Compute(Ref[T]):
    # noinspection PyMissingConstructor
    def __init__(self, func: Callable[[], T]) -> None:
        self._func = func

    @property
    def value(self) -> T:
        return self._func()
