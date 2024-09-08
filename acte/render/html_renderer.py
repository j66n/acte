import xml.etree.ElementTree as Et
from typing import cast

from acte.node import Node, Block, Virtual, Inline, Div, Text, ComponentNode, Root, Button, Dyna, Cache, Input, \
    InputType
from acte.node.implement import Container
from acte.render.renderer import Renderer


class HtmlRenderer(Renderer):
    def __init__(self) -> None:
        self._output = ""

    def render(self, node: Node) -> str:
        self._render(node)

        output = self._output

        self._output = ""

        return output

    def _render(self, node: Node) -> None:
        if isinstance(node, Virtual):
            self._render_virtual(node)
        elif isinstance(node, Block):
            self._render_block(node)
        elif isinstance(node, Inline):
            self._render_inline(node)
        else:
            raise ValueError(f"Unknown node type: {type(node)}")

    def _render_virtual(self, virtual: Virtual) -> None:
        if type(virtual) is ComponentNode:
            pass
        elif type(virtual) is Dyna:
            pass
        elif type(virtual) is Cache:
            pass
        else:
            raise ValueError(f"Unknown virtual type: {type(virtual)}")

        if isinstance(virtual, Container):
            for child in virtual.children:
                self._render(child)

        if type(virtual) is ComponentNode:
            pass
        elif type(virtual) is Dyna:
            pass
        elif type(virtual) is Cache:
            pass
        else:
            raise ValueError(f"Unknown virtual type: {type(virtual)}")

    def _render_block(self, block: Block) -> None:
        if type(block) is Root:
            self._output += "<body>"
        elif type(block) is Div:
            self._output += "<div>"
        else:
            raise ValueError(f"Unknown block type: {type(block)}")

        for child in block.children:
            self._render(child)

        if type(block) is Root:
            self._output += "</body>"
        elif type(block) is Div:
            self._output += "</div>"
        else:
            raise ValueError(f"Unknown block type: {type(block)}")

    def _render_inline(self, inline: Node) -> None:
        if isinstance(inline, Text):
            el = Et.Element("span")
            el.text = inline.content

            self._output += Et.tostring(el, method='html', encoding="unicode")
        elif isinstance(inline, Button):
            el = Et.Element(
                "button",
                id=inline.interactive_id,
            )

            if inline.hint != '':
                el.set("title", inline.hint)

            el.text = inline.content

            self._output += Et.tostring(el, method='html', encoding="unicode")
        elif isinstance(inline, Input):
            el = Et.Element("input")

            el.set("id", inline.interactive_id)

            if inline.name != '':
                el.set("name", inline.name)

            if inline.type is str:
                el.set("type", "text")
            elif inline.type is int:
                el.set("type", "number")
                el.set("step", "1")
            elif inline.type is float:
                el.set("type", "number")
                el.set("step", "any")
            else:
                raise ValueError(f"Unknown input type: {inline.type}")

            if inline.value is None:
                el.set("value", "")
            else:
                el.set("value", str(inline.value))

            if inline.hint != '':
                el.set("title", inline.hint)

            if inline.enum is not None:
                el.set("enum", str(inline.enum))

            self._output += Et.tostring(el, method='html', encoding="unicode")
        else:
            raise ValueError(f"Unknown inline type: {type(inline)}")
