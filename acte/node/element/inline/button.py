from typing import Callable, Awaitable

from acte.node.element.inline.inline import Inline
from acte.node.implement.interactive import Interactive
from acte.schema.schema import Schema
from acte.state import Effect, Ref


class Button(Inline, Interactive):
    def __init__(self) -> None:
        Inline.__init__(self)
        Interactive.__init__(self)

        self._content: str = ''
        self._schema: Schema | None = None
        self._on_press: Callable[[], Awaitable[None] | None] | None = None

    @property
    def content(self) -> str:
        return self._content

    @property
    def schema(self) -> Schema | None:
        return self._schema

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

    async def bind_schema(self, schema: Ref[Schema]) -> None:
        async def _func() -> None:
            self._schema = schema.value

        effect = await Effect.create(_func)

        self._effect_list.append(effect)

    async def bind_on_press(self, on_press: Ref[Callable[[], Awaitable[None] | None]]) -> None:
        async def _func() -> None:
            self._on_press = on_press.value

        effect = await Effect.create(_func)

        self._effect_list.append(effect)
