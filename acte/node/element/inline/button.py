from typing import Callable, Awaitable

from acte.node.element.inline.inline import Inline
from acte.node.implement.interactive import Interactive
from acte.state import Effect, Ref


class Button(Inline, Interactive):
    def __init__(self) -> None:
        Inline.__init__(self)
        Interactive.__init__(self)

        self._content: str = ''
        self._hint: str = ''
        self._on_press: Callable[[], Awaitable[None] | None] | None = None

    @property
    def content(self) -> str:
        return self._content

    @property
    def hint(self) -> str:
        return self._hint

    @property
    def on_press(self) -> Callable[[], Awaitable[None] | None] | None:
        return self._on_press

    async def bind_content(self, content: Ref[str]) -> None:
        async def _func() -> None:
            v = content.value
            if v is None:
                v = ''

            self._content = v

        effect = await Effect.create(_func)

        self._effect_list.append(effect)

    async def bind_hint(self, hint: Ref[str]) -> None:
        async def _func() -> None:
            v = hint.value
            if v is None:
                v = ''

            self._hint = v

        effect = await Effect.create(_func)

        self._effect_list.append(effect)

    async def bind_on_press(self, on_press: Ref[Callable[[], Awaitable[None] | None]]) -> None:
        async def _func() -> None:
            self._on_press = on_press.value

        effect = await Effect.create(_func)

        self._effect_list.append(effect)
