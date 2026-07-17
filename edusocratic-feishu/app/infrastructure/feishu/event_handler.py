import json
import logging
from typing import Optional
from lark_oapi.api.im.v1 import P2ImMessageReceiveV1
from app.config import settings


logger = logging.getLogger(__name__)


class FeishuEventHandler:
    """飞书事件处理器"""

    def __init__(self, feishu_client, grading_engine, card_builder, asr_provider=None):
        self.feishu = feishu_client
        self.engine = grading_engine
        self.cards = card_builder
        self.asr = asr_provider

    async def handle_message(self, event: P2ImMessageReceiveV1) -> None:
        """处理飞书消息接收事件"""
        message = event.event.message
        message_id = message.message_id
        sender_id = event.event.sender.sender_id.open_id

        # 解析消息内容
        try:
            content = json.loads(message.content)
        except (json.JSONDecodeError, TypeError):
            logger.warning(f"Invalid message content from {sender_id}")
            return

        msg_type = message.msg_type

        if msg_type == "text":
            text = content.get("text", "").strip()
            if text:
                await self._handle_text_message(sender_id, message_id, text)

        elif msg_type == "audio":
            file_key = content.get("file_key")
            if file_key:
                await self._handle_audio_message(sender_id, message_id, message_id, file_key)

        elif msg_type == "file":
            file_key = content.get("file_key")
            if file_key:
                await self._handle_file_message(sender_id, message_id, message_id, file_key)

    async def _handle_text_message(self, sender_id: str, reply_id: str, text: str) -> None:
        """处理文字消息"""
        # TODO: 从数据库获取学生信息和当前课堂主题
        # 这里使用示例数据演示
        student_id = sender_id
        class_id = "demo_class"
        grade = 3
        topic = "应不应该给动物穿衣服？"

        result = await self.engine.assess(
            student_id=student_id,
            class_id=class_id,
            grade=grade,
            topic=topic,
            response=text
        )

        if result.get("error"):
            await self.feishu.reply_message(
                reply_id,
                json.dumps({"text": "系统暂时无法评估，请稍后再试或联系老师手动评估"}),
                "text"
            )
            return

        card_content = self.cards.build_assessment_card(
            student_name="学生",
            grade=grade,
            topic=topic,
            scores=result.get("scores", {}),
            weighted_score=result.get("weighted_score", 0),
            highlights=result.get("highlights", ""),
            suggestions=result.get("suggestions", ""),
            overall_comment=result.get("overall_comment", ""),
            assessment_id=reply_id
        )

        await self.feishu.send_message(
            receive_id=sender_id,
            content=card_content,
            msg_type="interactive"
        )

    async def _handle_audio_message(self, sender_id: str, reply_id: str, message_id: str, file_key: str) -> None:
        """处理语音消息"""
        if not self.asr:
            await self.feishu.reply_message(
                reply_id,
                json.dumps({"text": "语音识别功能暂未开启，请输入文字"}),
                "text"
            )
            return

        # 下载音频
        audio_bytes = await self.feishu.download_file(message_id, file_key)
        if not audio_bytes:
            await self.feishu.reply_message(
                reply_id,
                json.dumps({"text": "音频下载失败，请重试"}),
                "text"
            )
            return

        # ASR转写
        asr_result = await self.asr.transcribe(audio_bytes)
        text = asr_result.get("text", "")
        confidence = asr_result.get("confidence", 0)

        if confidence < settings.ASR_MIN_CONFIDENCE:
            await self.feishu.reply_message(
                reply_id,
                json.dumps({"text": "我没听清，请再说一次，或者输入文字回答"}),
                "text"
            )
            return

        # 转写成功后当作文字处理
        await self._handle_text_message(sender_id, reply_id, text)

    async def _handle_file_message(self, sender_id: str, reply_id: str, message_id: str, file_key: str) -> None:
        """处理文件消息（习作文档）"""
        # TODO: 实现OCR/文本提取后评估
        await self.feishu.reply_message(
            reply_id,
            json.dumps({"text": "习作评估功能开发中，敬请期待"}),
            "text"
        )
