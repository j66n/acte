import traceback
import uuid
from typing import Type, Any, cast

from acte.build import Builder, Component
from acte.executor import Executor, ActionType
from acte.render import Renderer, HtmlRenderer
from acte.session.exception import SessionBuildException, SessionDisplayException, SessionValidateException, \
    SessionExecuteException

from acte.session.session import Session
from acte.session.ret_val import RetVal
from acte.session.validator import Validator


class SessionManager(Validator):
    def __init__(
            self,
            entry_class: Type[Component],
            builder: Builder | None = None,
            executor: Executor | None = None,
            renderer: Renderer | None = None,
            debug: bool = False,
    ) -> None:
        self._entry_class = entry_class
        self._builder = builder if builder is not None else Builder()
        self._executor = executor if executor is not None else Executor()
        self._renderer = renderer if renderer is not None else HtmlRenderer()
        self._debug = debug

        self._session_dict: dict[str, Session] = {}

    async def new_session(self) -> dict[str, Any]:
        ret_val = RetVal()

        session = Session(self._entry_class, self._builder, self._executor, self._renderer)

        session_id = str(uuid.uuid4())
        self._session_dict[session_id] = session

        ret_val.session_id = session_id

        try:
            await session.start()
        except Exception as e:
            if self._debug:
                traceback.print_exc()

            ret_val.build_error = str(e)
            return ret_val.to_dict()

        screen, display_error = await self._display(session)
        if screen is not None:
            ret_val.screen = screen

        if display_error is not None:
            if self._debug:
                traceback.print_exc()

            ret_val.display_error = display_error

        return ret_val.to_dict()

    async def execute(self, request: dict[str, Any]) -> dict[str, Any]:
        """
        :param request:
        {
            "session_id": str,
            "actions": [
                {
                    "target_id": str,
                    "type": str,
                    "value": str | None
                }
            ]
        }
        """
        ret = RetVal()

        ret.validate_error = self.validate_execute_request(request, self._session_dict)
        if ret.validate_error is not None:
            if self._debug:
                traceback.print_exc()

            sid = request.get('session_id')
            if (sid is not None) and (sid in self._session_dict):
                ret.session_id = sid

            ret.executed_actions = []

            return ret.to_dict()

        ret.session_id = request['session_id']
        actions = request['actions']

        session = self._session_dict[cast(str, ret.session_id)]

        executed_actions = []
        for action in actions:
            target_id = action['target_id']
            action_type = ActionType(action['action_type'])
            value = action.get('value')

            try:
                await session.execute(target_id, action_type, value)
                executed_actions.append(action)
            except Exception as e:
                if self._debug:
                    traceback.print_exc()

                ret.execute_error = {
                    "action": action,
                    "message": str(e)
                }

                ret.executed_actions = executed_actions
                break

        ret.screen, ret.display_error = await self._display(session)

        return ret.to_dict()

    async def display(self, request: dict[str, Any]) -> dict[str, Any]:
        ret = RetVal()

        ret.validate_error = self._validate_session_id(request, self._session_dict)
        if ret.validate_error is not None:
            if self._debug:
                traceback.print_exc()

            sid = request.get('session_id')
            if (sid is not None) and (sid in self._session_dict):
                ret.session_id = sid

            return ret.to_dict()

        sid = request['session_id']
        ret.session_id = sid
        session = self._session_dict[cast(str, sid)]

        ret.screen, ret.display_error = await self._display(session)
        if ret.display_error is not None:
            if self._debug:
                traceback.print_exc()

        return ret.to_dict()

    @staticmethod
    async def _display(session: Session) -> tuple[str | None, str | None]:
        try:
            await session.display()
            screen = session.render()
            return screen, None
        except Exception as e:
            return None, str(e)
