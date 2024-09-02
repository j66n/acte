from typing import Any


class RetVal:
    def __init__(self) -> None:
        self.session_id: str | None = None
        self.screen: str | None = None

        self.validate_error: dict[str, Any] | None = None
        self.build_error: str | None = None
        self.execute_error: dict[str, Any] | None = None
        self.display_error: str | None = None
        self.executed_actions: list[dict[str, Any]] | None = None

        self.ret_dict: dict[str, Any] = {}

    def to_dict(self) -> dict[str, Any]:
        self.ret_dict = {}

        self._add_dict_field('session_id')
        self._add_dict_field('screen')

        self._add_dict_error_field('build_error')
        self._add_dict_error_field('validate_error')
        self._add_dict_error_field('execute_error')
        self._add_dict_error_field('display_error')
        self._add_dict_error_field('executed_actions')

        return self.ret_dict

    def _add_dict_field(self, field_name: str) -> None:
        value = getattr(self, field_name)
        if value is not None:
            self.ret_dict[field_name] = value

    def _add_dict_error_field(self, field_name: str) -> None:
        value = getattr(self, field_name)
        if value is not None:
            if 'error_info' not in self.ret_dict:
                self.ret_dict['error_info'] = {}

            self.ret_dict['error_info'][field_name] = value
