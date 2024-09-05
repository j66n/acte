import json

import aiohttp
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

        url = f"{self._base_url}/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}"
        }

        payload = {
            "model": self._model,
            "temperature": self._temperature,
            "max_tokens": self._max_tokens,
            "messages": messages,
            "tools": tools,
            "stream": True,
        }

        # use aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.content_type == "text/event-stream":
                    async for line in response.content:
                        yield line
                else:
                    response = await response.text()
                    raise Exception(response)

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
