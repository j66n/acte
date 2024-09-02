from typing import Any

from acte.session import Session


class Validator:
    @classmethod
    def validate_execute_request(
            cls,
            data: dict[str, Any],
            session_dict: dict[str, Session],
    ) -> dict[str, Any] | None:
        err_dict: dict[str, Any] = {}

        sid_err = cls._validate_session_id(data, session_dict)
        if sid_err is not None:
            err_dict.update(sid_err)

        actions = data.get('actions', None)
        if actions is None:
            err_dict['actions'] = 'Missing field.'
        else:
            if not isinstance(actions, list):
                err_dict['actions'] = 'Invalid value. Must be a list.'
            else:
                action_err_info_list: list[Any] = []
                for i, action in enumerate(actions):
                    action_err_info = cls._validate_action(action)
                    if action_err_info is not None:
                        item = {"index": i, **action_err_info}
                        action_err_info_list.append(item)

                if len(action_err_info_list) != 0:
                    err_dict['actions'] = action_err_info_list

        if len(err_dict) != 0:
            return err_dict

        return None

    @classmethod
    def _validate_action(cls, action_data: dict[str, Any]) -> dict[str, Any] | None:
        err_info_dict: dict[str, Any] = {}

        if 'target_id' not in action_data:
            err_info_dict['target_id'] = 'Missing field.'
        else:
            if not isinstance(action_data['target_id'], str):
                err_info_dict['target_id'] = 'Invalid value. Must be a string.'

        if 'action_type' not in action_data:
            err_info_dict['action_type'] = 'Missing field.'
        else:
            if action_data['action_type'] not in ['press', 'fill']:
                err_info_dict['action_type'] = 'Invalid value. Must be one of "press" and "fill". '

            if action_data['action_type'] == 'fill':
                if 'value' not in action_data:
                    err_info_dict['value'] = 'Missing field.'
                else:
                    if not isinstance(action_data['value'], str):
                        err_info_dict['value'] = 'Invalid value. Must be a string.'
            else:
                if 'value' in action_data:
                    err_info_dict['value'] = 'Invalid field. Must not be present.'

        if len(err_info_dict) != 0:
            return err_info_dict

        return None

    @classmethod
    def _validate_session_id(cls, data: dict[str, Any], session_dict: dict[str, Session]) -> dict[str, Any] | None:
        err_dict: dict[str, Any] = {}

        sid = data.get('session_id', None)
        if sid is None:
            err_dict['session_id'] = 'Missing field.'
        else:
            if not isinstance(sid, str):
                err_dict['session_id'] = 'Invalid value. Must be a string.'
            else:
                if sid not in session_dict:
                    err_dict['session_id'] = 'Invalid value. Session not found.'

        if len(err_dict) != 0:
            return err_dict

        return None
