import aiohttp
import base64
import hashlib
import time
from typing import Optional
from app.config import settings


class ASRProvider:
    """ASR Provider 接口"""

    async def transcribe(self, audio_bytes: bytes, audio_format: str = "m4a") -> dict:
        """转写音频为文字，返回 {text, confidence}"""
        raise NotImplementedError


class XunfeiASRProvider(ASRProvider):
    """讯飞ASR适配"""

    def __init__(self):
        self.app_id = settings.XUNFEI_APP_ID
        self.api_key = settings.XUNFEI_API_KEY
        self.api_secret = settings.XUNFEI_API_SECRET
        self.base_url = "https://raasr.xfyun.cn/v2/api"

    async def transcribe(self, audio_bytes: bytes, audio_format: str = "m4a") -> dict:
        """讯飞语音转写"""
        ts = str(int(time.time()))
        sign_str = (self.api_key + ts).encode("utf-8")
        sign = base64.b64encode(
            hashlib.md5(sign_str).digest()
        ).decode("utf-8")

        headers = {
            "X-Appid": self.app_id,
            "X-CurTime": ts,
            "X-Param": base64.b64encode(
                b'{"engine_type":"sms16k"}'
            ).decode("utf-8"),
            "X-CheckSum": sign,
        }

        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field("file", audio_bytes, filename=f"audio.{audio_format}")

            async with session.post(
                f"{self.base_url}/upload",
                headers=headers,
                data=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                resp.raise_for_status()
                result = await resp.json()
                return {
                    "text": result.get("text", ""),
                    "confidence": result.get("confidence", 0.0),
                    "raw": result
                }
