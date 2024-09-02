from typing import TypeVar, TypeAlias

from acte.state import Ref

T = TypeVar('T')

Prop: TypeAlias = Ref[T] | T


def to_ref(value: Prop[T]) -> Ref[T]:
    if isinstance(value, Ref):
        return value

    return Ref(value)


as_prop = to_ref
