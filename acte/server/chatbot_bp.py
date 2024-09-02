import os
from json import JSONDecodeError

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, StreamingResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from acte.chatbot import Chatbot


class _CustomStaticFiles(StaticFiles):
    def file_response(self, full_path, stat_result, scope, status_code=200):
        response = super().file_response(full_path, stat_result, scope, status_code)
        if full_path.endswith('.js'):
            response.headers['Content-Type'] = 'application/javascript'
        return response


class ChatbotBp:
    def __init__(self, chatbot: Chatbot, load_static: bool = True) -> None:
        self._chatbot = chatbot
        self._load_static = load_static

    def as_app(self) -> Starlette:
        routes = [Route('/completions', self._completions_route, methods=['POST'])]

        if self._load_static:
            this_file_dir = os.path.dirname(os.path.abspath(__file__))
            static_dir = os.path.join(this_file_dir, "static")

            static_route = Mount('/', app=_CustomStaticFiles(directory=static_dir, html=True), name="static")
            routes.append(static_route)

        return Starlette(routes=routes)

    async def _completions_route(self, request: Request) -> JSONResponse | StreamingResponse:
        try:
            request_dict = await request.json()
        except JSONDecodeError:
            return JSONResponse({"error_info": {"validation_error": "fail to decode json"}}, 400)

        try:
            messages = request_dict["messages"]
        except KeyError:
            return JSONResponse({"err_info": {"validation_error": "messages key not found"}}, 400)

        try:
            first_result = await anext(self._chatbot.completion(messages))
        except Exception as e:
            return JSONResponse({"error_info": {"validation_error": str(e)}}, 400)

        async def generate():
            yield f"data: {first_result}\n\n"

            async for choice in self._chatbot.completion(messages):
                yield f"data: {choice}\n\n"

            yield f"data: [DONE]"

        return StreamingResponse(generate(), media_type="text/event-stream")
