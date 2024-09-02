from acte import Component, v
from acte.chatbot import OpenaiChatbot
from acte.server import Server
from acte.session import SessionManager
from acte.state.signal import Signal


class Counter(Component):
    def __init__(self) -> None:
        self._n = Signal(0)

    def view(self) -> None:
        v.text("This is a counter.")

        with v.div():
            v.text(lambda: f"Current Value: {self._n.value}")
            # _n is Signal, so you need to use self._n.value in lambda

        v.button("add", on_press=self._add)

    async def _add(self) -> None:
        await self._n.set(self._n.value + 1)


server = Server(
    session_manager=SessionManager(Counter, debug=True),
    chatbot=OpenaiChatbot(
        api_key="YOUR OPENAI API KEY",
    )
)

if __name__ == '__main__':
    server.run()
