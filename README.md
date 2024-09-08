![logo.png](https://github.com/j66n/acte/raw/master/images/logo.png)

## What is Acte?

Acte is a framework to build GUI-like tools for AI Agents.

### Why GUI-like?

The current tool solution, as known as Function Calling, is based on API calling, like weather API, Google API, etc. It
has two main problems in complex scenarios:

1. Multiple APIs increase the cognitive load for AI Agents, potentially leading to reasoning errors, especially when the
   APIs have a strict calling order.
2. Directly calling APIs is a way with too much freedom degrees, lacking constraints, potentially resulting in data
   errors.

The way Agents interact with APIs reminds me of how human interacts with computers in old days. A guy faces a black and
thick screen and types the keyboard, while looking up commands in a manual. Not just Agent, we also faces these two
problems.

Then a technique that surprised Steve Jobs comes up: Graphical User Interface (GUI).

Since then, most of us no longer directly interact with command lines (a kind of API). We interact with API through GUI.
GUI generally solved these two problems by constraining interaction to reduce cognitive load and degrees of freedom.

This is why Agents also need GUI-like tools. I prefer calling it Agentic User Interface (AUI).

## Quick Start

### **Installation**

```shell
pip install acte
```

### Example1: Hello World

```python
from acte import Component, v
from acte.chatbot import OpenaiChatbot
from acte.server import Server
from acte.session import SessionManager


class HelloWorld(Component):
    def view(self) -> None:
        v.text("Hello World")


server = Server(
    session_manager=SessionManager(HelloWorld, debug=True),
    chatbot=OpenaiChatbot(  # default model is gpt-4o
        api_key="YOUR OPENAI API KEY",
    )
)

if __name__ == '__main__':
    server.run()
```

1. Copy the code to a Python file, and set **OpenAI Api Key**.

2. Run the code, and visit the playground: http://127.0.0.1:8000.
   ![Example_00_00_hello_world.png](https://github.com/j66n/acte/raw/master/images/Example_00_00_hello_world.png)

3. Input "Hi, please new a session, and tell what you see."
   Then, the Agent will interact with **Screen**, and give you a response.
   ![Example_00_01_hello_world.png](https://github.com/j66n/acte/raw/master/images/Example_00_01_hello_world.png)

Note: You can also interact with **Screen** to debug your app.

---

### Example2: Counter

```python
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
```

1. Agent can **press** the button in **Screen**. The number on the right-top of the button is **Interactive ID**.
   Agent interacts with **Screen** by pointing to ID.
   ![Example_01_00_counter.png](https://github.com/j66n/acte/raw/master/images/Example_01_00_counter.png)

2. Interaction's result will show in **Screen**. You can click "View"s in **Dialog** to check the **Screen** status in
   each step.
   ![Example_01_01_counter.png](https://github.com/j66n/acte/raw/master/images/Example_01_01_counter.png)

---

### Example3: Restaurant Assistant

```python
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
         v.input_int("quantity", self._quantity, self._on_set)

   async def _on_set(self, value: str) -> None:
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

      v.button("checkout", on_press=self._checkout)

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
```

1. Agent can **fill** input fields in **Screen**.
   ![Example_02_00_restaurant_assistant.png](https://github.com/j66n/acte/raw/master/images/Example_02_00_restaurant_assistant.png)

2. Input fields also have their own **Interactive ID**. Agent can take multiple actions in one calling.
   ![Example_02_01_restaurant_assistant.png](https://github.com/j66n/acte/raw/master/images/Example_02_01_restaurant_assistant.png)

3. You can define the backend logic after Agent press the button, such as make a request.
   ![Example_02_02_restaurant_assistant.png](https://github.com/j66n/acte/raw/master/images/Example_02_02_restaurant_assistant.png)

## Tool API

Acte Tool has 3 APIs: `new_session`, `execute`, and `display`,
which can be accessed by HTTP request or `SessionManager`

### 1. New Session

Start a new App session, then display the session's latest screen.

#### HTTP request

```http request
POST /session
```

#### SessionManager

```python
from acte.session import SessionManager

sm = SessionManager(...)

sm.new_session()
```

#### Return

```
{
    "session_id": str,
    "screen": str,
}
```

---

### 2. Execute

Execute one or more action(s), then display the session's latest screen.

#### HTTP Request

```http request
POST /execute

json:
{
    "session_id": "str",
    "actions": [
        {
            "target_id": "str",
            "action_type": "str",
            "value": "str | None",
        },
    ]
}
```

#### SessionManager

```python
from acte.session import SessionManager

sm = SessionManager(...)

sm.execute(
    {
        "session_id": str,
        "actions": [
            {
                "target_id": str,  # interactive id
                "action_type": str,  # one of ["press", "fill"]
                "value": str | None,  # required when action_type is "fill"
            },
            ...
        ]
    }
)
```

#### Return

```python
{
    "session_id": str,
    "screen": str,
}
```

---

### 3. Display

Display the session's latest screen.

#### HTTP Request

```http request
POST /display

json: 
{
    "session_id": "str",
}
```

#### SessionManager

```python
from acte.session import SessionManager

sm = SessionManager(...)

sm.execute(
    {
        "session_id": str,
    }
)
```

#### Return

```python
{
    "session_id": str,
    "screen": str,
}
```

## Roadmap

- [ ] Full Document

- [ ] Test Code

Note: The project is in Alpha stage. The API may change frequently.

## LICENSE

The project is licensed under the terms of the MIT license.
