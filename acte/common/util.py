import inspect
from typing import Any, Awaitable, Callable, TypeVar, Union, cast

T = TypeVar('T')


async def call_mix(
        func: Callable[..., Union[Awaitable[T], T]],
        *args: Any,
        **kwargs: Any
) -> T:
    if inspect.iscoroutinefunction(func):
        return cast(T, await func(*args, **kwargs))
    else:
        return cast(T, func(*args, **kwargs))
