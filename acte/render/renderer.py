import abc

from acte.node import Node


class Renderer(abc.ABC):
    @abc.abstractmethod
    def render(self, node: Node) -> str:
        pass
