"""飞书事件回调端点"""

import json
import logging
from fastapi import APIRouter, Request, HTTPException
from app.config import settings
from app.utils.text_parser import parse_teacher_message

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/webhook")
async def feishu_webhook(request: Request):
    """接收飞书事件推送"""
    body = await request.json()

    # 1. URL 验证（飞书首次配置时发送）
    if "challenge" in body:
        return {"challenge": body["challenge"]}

    # 2. 验证 token
    token = body.get("header", {}).get("token", "")
    if token != settings.feishu_verification_token:
        raise HTTPException(status_code=403, detail="Invalid token")

    # 3. 提取事件
    event = body.get("event", {})
    event_type = body.get("header", {}).get("event_type", "")

    if event_type != "im.message.receive_v1":
        return {"code": 0}  # 忽略非消息事件

    # 4. 提取消息信息
    message = event.get("message", {})
    msg_type = message.get("message_type", "")
    chat_id = message.get("chat_id", "")
    message_id = message.get("message_id", "")
    content_str = message.get("content", "{}")
    sender = event.get("sender", {}).get("sender_id", {}).get("open_id", "")

    # 5. 检查是否 @了机器人
    mentions = message.get("mentions", [])
    is_mentioned = any(
        m.get("key") == "@_all" or m.get("id", {}).get("open_id") == settings.feishu_app_id
        for m in mentions
    ) if mentions else False

    content = json.loads(content_str) if isinstance(content_str, str) else content_str

    if msg_type == "text":
        text_content = content.get("text", "")
        # 简单判断：如果消息以 @ 开头或包含 @机器人
        if not is_mentioned and "@" not in text_content:
            return {"code": 0}  # 不是 @机器人的消息，忽略

        # 解析指令
        parsed = parse_teacher_message(text_content)
        logger.info(f"解析结果: {parsed}")

        # TODO: Level 4 实现实际评估调用
        # 目前先返回解析结果（调试用）
        return {
            "code": 0,
            "data": {
                "parsed": parsed.model_dump(),
                "chat_id": chat_id,
                "message_id": message_id,
                "sender": sender,
            }
        }

    elif msg_type == "image":
        # TODO: Phase 2 实现 OCR
        logger.info(f"收到图片消息: {message_id}")
        return {"code": 0, "data": {"msg": "图片功能开发中"}}

    elif msg_type == "audio":
        # TODO: Phase 2 实现 ASR
        logger.info(f"收到语音消息: {message_id}")
        return {"code": 0, "data": {"msg": "语音功能开发中"}}

    return {"code": 0}
