from json import JSONDecodeError

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from acte.chatbot import Chatbot
from acte.server.chatbot_bp import ChatbotBp
from acte.session.session_manager import SessionManager


class Server:
    def __init__(
            self,
            session_manager: SessionManager,
            chatbot: Chatbot | None = None,
    ):
        self._session_manager = session_manager

        self._app = Starlette(routes=[
            Route('/session', self._new_session, methods=['POST']),
            Route('/execute', self._execute, methods=['POST']),
            Route('/display', self._display, methods=['POST']),
        ])

        if chatbot is not None:
            chatbot_bp = ChatbotBp(chatbot)
            self._app.mount("/", chatbot_bp.as_app())

    @property
    def app(self) -> Starlette:
        return self._app

    def run(self, *args, **kwargs) -> None:
        uvicorn.run(self._app, *args, **kwargs)

    async def _new_session(self, request: Request) -> JSONResponse:
        resp_dict = await self._session_manager.new_session()
        return JSONResponse(resp_dict)

    async def _execute(self, request: Request) -> JSONResponse:
        try:
            data = await request.json()
        except JSONDecodeError as e:
            return JSONResponse({"error_info": {"validation_error": str(e)}})

        resp_dict = await self._session_manager.execute(data)
        return JSONResponse(resp_dict)

    async def _display(self, request: Request) -> JSONResponse:
        try:
            data = await request.json()
        except JSONDecodeError as e:
            return JSONResponse({"error_info": {"validation_error": str(e)}})

        resp_dict = await self._session_manager.display(data)
        return JSONResponse(resp_dict)
