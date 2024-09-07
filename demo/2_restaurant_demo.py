from typing import Callable, Awaitable

from acte.chatbot import OpenaiChatbot
from acte.server import Server
from acte.session import SessionManager

from acte import Component, v, Prop, as_prop
from acte.state.signal import Signal


class MenuItem(Component):
    def __init__(
            self,
            name: Prop[str],  # Prop = Ref[T] | T
            price: Prop[float],
            quantity: Prop[int],
            on_quantity_change: Callable[[str, float, int], Awaitable[None]]
    ) -> None:
        self._name = as_prop(name)  # as_prop is to convert T to Ref[T]
        self._price = as_prop(price)
        self._quantity = as_prop(quantity)

        self._on_quantity_change = on_quantity_change

    def view(self) -> None:
        with v.div():
            v.text(lambda: f"{self._name.value}: ${self._price.value}")
            v.input_int("quantity", self._quantity, self._on_fill)

    async def _on_fill(self, value: str) -> None:
        await self._on_quantity_change(
            self._name.value,
            self._price.value,
            0 if value == '' else int(value)
        )


class Menu(Component):
    def __init__(self) -> None:
        self._menu = {
            "Pizza": {"price": 10.0, "quantity": Signal(0)},  # Signal is a kind of Ref, but can be set
            "Coke": {"price": 2.0, "quantity": Signal(0)},
        }

    def view(self) -> None:
        v.text("Super Restaurant Menu")

        for key, value in self._menu.items():
            v.component(
                MenuItem(
                    name=key,
                    price=value['price'],
                    quantity=value['quantity'],
                    on_quantity_change=self._on_quantity_change,
                )
            )

        v.text(self.total)

        v.button("checkout", on_press=self._checkout, hint="This is a test Hint")

    def total(self) -> str:
        total = 0

        for key, value in self._menu.items():
            total += value['price'] * value['quantity'].value

        return f"Total: ${total}"

    async def _on_quantity_change(self, name: str, price: float, quantity: int) -> None:
        await self._menu[name]['quantity'].set(quantity)

    async def _checkout(self) -> None:
        total = self.total()

        for value in self._menu.values():
            await value['quantity'].set(0)

        print(f"Checkout: {total}")


server = Server(
    session_manager=SessionManager(Menu, debug=True),
    chatbot=OpenaiChatbot(
        api_key="YOUR OPENAI API KEY",
    )
)

if __name__ == '__main__':
    server.run()
