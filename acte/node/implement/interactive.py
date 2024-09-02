class Interactive:
    def __init__(self) -> None:
        self._interactive_id: str = ""

    @property
    def interactive_id(self) -> str:
        return self._interactive_id

    def set_interactive_id(self, interactive_id: str) -> None:
        self._interactive_id = interactive_id
