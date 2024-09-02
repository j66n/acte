from __future__ import annotations

import inspect
from typing import TypeVar
from abc import abstractmethod

T = TypeVar('T')


async def call_on_mount(c: Component) -> None:
    on_mount_func = getattr(c, 'on_mount', None)
    if on_mount_func is None:
        return

    if inspect.iscoroutinefunction(on_mount_func):
        await on_mount_func()
    else:
        on_mount_func()


async def call_on_display(c: Component) -> None:
    on_display_func = getattr(c, 'on_display', None)
    if on_display_func is None:
        return

    if inspect.iscoroutinefunction(on_display_func):
        await on_display_func()
    else:
        on_display_func()


class Component:
    @abstractmethod
    def view(self) -> None:
        pass
