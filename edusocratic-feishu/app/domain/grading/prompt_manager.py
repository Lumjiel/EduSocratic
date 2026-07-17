from pathlib import Path
from typing import Optional
import re


PROMPTS_DIR = Path(__file__).parent.parent.parent / "prompts"


class PromptManager:
    """Prompt模板管理 — 支持版本化和A/B测试"""

    def __init__(self, version: str = "v1.0"):
        self.version = version
        self._cache: dict[str, str] = {}

    def get_assessment_prompt(self, grade: int) -> str:
        """获取对应年级的评估Prompt"""
        if 1 <= grade <= 2:
            return self._load("assessment_1_2.md")
        elif 3 <= grade <= 4:
            return self._load("assessment_3_4.md")
        elif 5 <= grade <= 7:
            return self._load("assessment_5_7.md")
        return self._load("assessment_3_4.md")

    def get_format_repair_prompt(self) -> str:
        return self._load("format_repair.md")

    def render_assessment_prompt(self, grade: int, topic: str, response: str) -> str:
        """渲染评估Prompt模板"""
        template = self.get_assessment_prompt(grade)
        return template.replace("{{grade}}", str(grade)).replace("{{topic}}", topic).replace("{{response}}", response)

    def _load(self, filename: str) -> str:
        if filename in self._cache:
            return self._cache[filename]
        path = PROMPTS_DIR / self.version / filename
        if not path.exists():
            path = PROMPTS_DIR / "v1.0" / filename
        content = path.read_text(encoding="utf-8")
        self._cache[filename] = content
        return content

    def clear_cache(self):
        self._cache.clear()
