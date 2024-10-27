from typing import Dict, Any
import json

class Config:
    def __init__(self):
        self.mode: str = "normal"
        self.clothes: list = ["pencil dress"]
        self.stable_diffusion_prompt: str = "woman secretary"
        self.pictures: bool = True
        self.base_url: str = "http://localhost:1234/v1"
        self.api_key: str = "lm-studio"
        self.telegram_token: str = "YOUR_TOKEN_HERE"
        self.webui_host: str = "127.0.0.1"
        self.webui_port: int = 7860

    @classmethod
    def load_messages(cls, filename: str) -> list:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def save_messages(messages: list, filename: str) -> None:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(messages, file, ensure_ascii=False, indent=4)