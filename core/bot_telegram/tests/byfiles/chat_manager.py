from openai import OpenAI
from typing import List, Dict

class ChatManager:
    def __init__(self, base_url: str, api_key: str):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.messages: List[Dict[str, str]] = []

    def get_response(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})
        completion = self.client.chat.completions.create(
            model="TheBloke/dolphin-2.2.1-mistral-7B-GGUF",
            messages=self.messages,
            temperature=1.1,
        )
        response = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": response})
        return response
