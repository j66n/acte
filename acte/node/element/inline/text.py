from acte.node.element.inline.inline import Inline
from acte.state import Ref, Effect


class Text(Inline):
    def __init__(self) -> None:
        super().__init__()

        self._content = ""

    @property
    def content(self) -> str:
        return self._content

    async def bind_content(self, content: Ref[str]) -> None:
        async def _func() -> None:
            self._content = content.value

        effect = await Effect.create(_func)

        self._effect_list.append(effect)
