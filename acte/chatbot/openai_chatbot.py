import json

from openai import AsyncOpenAI
from typing import Any, AsyncGenerator

from acte.chatbot.chatbot import Chatbot
from acte.chatbot.tools import tools


class OpenaiChatbot(Chatbot):
    def __init__(
            self,
            api_key: str,
            system_message: str = '',
            model: str = "gpt-4o",
            temperature: float = 0.3,
            max_tokens: int = 2000,
            base_url: str = "https://api.openai.com/v1",
    ) -> None:
        self._api_key = api_key
        self._system_message = system_message
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._base_url = base_url

        self.client: AsyncOpenAI = AsyncOpenAI(
            api_key=self._api_key,
            base_url=self._base_url,
        )

    async def completion(self, messages: list[dict[str, Any]]) -> AsyncGenerator[str, None]:
        # Openai doesn't support user tool call and response, so we need to escape them
        if self._system_message != '':
            messages = [
                {'role': 'system', 'content': self._system_message},
                *self._escape_user_tool_calls_and_responses(messages),
            ]

        async for chunk in await self.client.chat.completions.create(
                model=self._model,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
                messages=messages,
                tools=tools,
                stream=True
        ):
            choices = chunk.model_dump_json()
            yield choices

    @staticmethod
    def _escape_user_tool_calls_and_responses(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        prev_user_call = False

        new_messages = []

        for message in messages:
            new_message = message

            if 'tool_calls' in message:
                new_message = {
                    "role": "user",
                    "content": json.dumps(message['tool_calls'])
                }
                prev_user_call = True
            elif prev_user_call is True:
                prev_user_call = False
                new_message = {
                    "role": "user",
                    "content": message['content']
                }

            new_messages.append(new_message)

        return new_messages
