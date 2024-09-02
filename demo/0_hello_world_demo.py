from acte import Component, v
from acte.chatbot import OpenaiChatbot
from acte.server import Server
from acte.session import SessionManager


class HelloWorld(Component):
    def view(self) -> None:
        v.text("Hello World")


server = Server(
    session_manager=SessionManager(HelloWorld, debug=True),
    chatbot=OpenaiChatbot(                # default model is gpt-4o
        api_key="YOUR OPENAI API KEY",
    )
)

if __name__ == '__main__':
    server.run()
