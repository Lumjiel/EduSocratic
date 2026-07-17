import os
import aiohttp
from typing import Optional
from app.config import settings


class LLMProvider:
    """LLM Provider 接口"""

    async def chat(
        self,
        messages: list[dict],
        temperature: float = 0,
        response_format: Optional[dict] = None,
        max_tokens: int = 1000
    ) -> str:
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """OpenAI GPT-4 Turbo 适配"""

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.base_url = "https://api.openai.com/v1"

    async def chat(
        self,
        messages: list[dict],
        temperature: float = 0,
        response_format: Optional[dict] = None,
        max_tokens: int = 1000
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if response_format:
            payload["response_format"] = response_format

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data["choices"][0]["message"]["content"]


class ZhipuProvider(LLMProvider):
    """智谱 GLM-4 适配"""

    def __init__(self):
        self.api_key = settings.ZHIPU_API_KEY
        self.model = settings.ZHIPU_MODEL
        self.base_url = "https://open.bigmodel.cn/api/paas/v4"

    async def chat(
        self,
        messages: list[dict],
        temperature: float = 0,
        response_format: Optional[dict] = None,
        max_tokens: int = 1000
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data["choices"][0]["message"]["content"]


class LLMClientFactory:
    """LLM Provider 工厂"""

    _providers = {
        "openai": OpenAIProvider,
        "zhipu": ZhipuProvider,
    }

    @classmethod
    def create(cls, provider: Optional[str] = None) -> LLMProvider:
        name = provider or settings.LLM_PROVIDER
        provider_cls = cls._providers.get(name)
        if not provider_cls:
            raise ValueError(f"Unknown LLM provider: {name}")
        return provider_cls()
