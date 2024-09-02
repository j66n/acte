from typing import Generic, TypeVar

T = TypeVar('T', covariant=True)


class Ref(Generic[T]):
    def __init__(self, value: T|None) -> None:
        self._value = value

    @property
    def value(self) -> T|None:
        return self._value
