from acte.node.element.element import Element
from acte.node.implement.container import Container


class Block(Element, Container):
    def __init__(self) -> None:
        Element.__init__(self)
        Container.__init__(self)
