import aiohttp
import aiofiles
from pathlib import Path
from typing import Optional


class OSSProvider:
    """文件存储（本地/云OSS）"""

    def __init__(self, base_path: str = "./data/files"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def save_file(self, filename: str, data: bytes) -> str:
        file_path = self.base_path / filename
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(data)
        return str(file_path)

    async def read_file(self, filepath: str) -> bytes:
        async with aiofiles.open(filepath, "rb") as f:
            return await f.read()
