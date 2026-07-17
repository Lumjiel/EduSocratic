import json
import logging
from typing import Optional
from lark_oapi import Client
from lark_oapi.api.im.v1 import (
    CreateMessageReq, CreateMessageReqBody,
    ReplyMessageReq, ReplyMessageReqBody
)
from app.config import settings


logger = logging.getLogger(__name__)


class FeishuClient:
    """飞书API封装"""

    def __init__(self):
        self.client = Client.builder() \
            .app_id(settings.FEISHU_APP_ID) \
            .app_secret(settings.FEISHU_APP_SECRET) \
            .build()

    async def send_message(self, receive_id: str, content: str, msg_type: str = "interactive") -> dict:
        """发送消息"""
        try:
            body = CreateMessageReqBody.builder() \
                .content(content) \
                .msg_type(msg_type) \
                .build()

            req = CreateMessageReq.builder() \
                .receive_id_type("open_id") \
                .receive_id(receive_id) \
                .body(body) \
                .build()

            resp = self.client.im.v1.message.create(req)
            if not resp.success():
                logger.error(f"Failed to send message: {resp.code} {resp.msg}")
            return {"success": resp.success(), "code": resp.code, "msg": resp.msg}
        except Exception as e:
            logger.error(f"Send message error: {e}")
            return {"success": False, "error": str(e)}

    async def download_file(self, message_id: str, file_key: str, file_type: str = "opus") -> bytes:
        """下载飞书文件"""
        try:
            from lark_oapi.api.im.v1 import GetMessageResourceReq
            req = GetMessageResourceReq.builder() \
                .message_id(message_id) \
                .file_key(file_key) \
                .type(file_type) \
                .build()
            resp = self.client.im.v1.message_resource.get(req)
            return resp.file.read() if resp.file else b""
        except Exception as e:
            logger.error(f"Download file error: {e}")
            return b""

    async def reply_message(self, message_id: str, content: str, msg_type: str = "interactive") -> dict:
        """回复消息"""
        try:
            body = ReplyMessageReqBody.builder() \
                .content(content) \
                .msg_type(msg_type) \
                .build()

            req = ReplyMessageReq.builder() \
                .message_id(message_id) \
                .body(body) \
                .build()

            resp = self.client.im.v1.message.reply(req)
            return {"success": resp.success(), "code": resp.code, "msg": resp.msg}
        except Exception as e:
            logger.error(f"Reply message error: {e}")
            return {"success": False, "error": str(e)}
