from abc import ABC, abstractmethod

from typing import AsyncGenerator, Any


class Chatbot(ABC):
    @abstractmethod
    def completion(self, messages: list[dict[str, Any]]) -> AsyncGenerator[bytes, None]:
        pass
