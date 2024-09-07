from acte.build import call_on_display
from acte.common.util import call_mix
from acte.executor.action_type import ActionType
from acte.node import Root, Node, Button, Input, ComponentNode, InputType
from acte.node.implement import Interactive, Container


class Executor:
    @classmethod
    async def execute(cls, root: Root, target_id: str, action_type: ActionType, value: str | None) -> None:
        target = cls._find_node(root, target_id)
        if target is None:
            raise ValueError(f"Target not found: {target_id}")

        await cls._execute(target, action_type, value)

    @classmethod
    async def display(cls, node: Node) -> None:
        if isinstance(node, ComponentNode):
            c = node.component
            if c is not None:
                await call_on_display(c)

        if isinstance(node, Container):
            for child in node.children:
                await cls.display(child)

    @classmethod
    def _find_node(cls, node: Node, interactive_id: str) -> Interactive | None:
        if isinstance(node, Interactive) and node.interactive_id == interactive_id:
            return node

        if not isinstance(node, Container):
            return None

        for child in node.children:
            target = cls._find_node(child, interactive_id)
            if target is not None:
                return target

        return None

    @classmethod
    async def _execute(cls, interactive: Interactive, action_type: ActionType, value: str | None) -> None:
        if isinstance(interactive, Button):
            await cls._button_execute(interactive, action_type)
        elif isinstance(interactive, Input):
            await cls._input_execute(interactive, action_type, value)
        else:
            raise ValueError(f"Unknown interactive type: {interactive}")

    @classmethod
    async def _button_execute(cls, button: Button, action_type: ActionType) -> None:
        if action_type == ActionType.PRESS:
            await call_mix(button.on_press)
        else:
            raise ValueError(f"Button doesn't support action type: {action_type.value}")

    @classmethod
    async def _input_execute(cls, node: Input, action_type: ActionType, value: str | None) -> None:
        if action_type == ActionType.FILL:
            if value is None:
                raise ValueError("Input value is None")

            try:
                if value != '':
                    node.type(value)
            except ValueError:
                raise ValueError(f"Input value is not a {node.type}: {value}")

            await call_mix(node.on_fill, value)

        else:
            raise ValueError(f"Input doesn't support action type: {action_type.value}")
