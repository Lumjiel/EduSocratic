import logging
from fastapi import APIRouter, Request, HTTPException


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/feishu/events")
async def handle_feishu_event(request: Request):
    """飞书事件回调"""
    body = await request.json()

    if body.get("type") == "url_verification":
        return {"challenge": body.get("challenge")}

    event = body.get("event", {})
    event_type = body.get("header", {}).get("event_type", "")

    if event_type == "im.message.receive_v1":
        handler = request.app.state.event_handler
        try:
            from lark_oapi.api.im.v1 import P2ImMessageReceiveV1
            event_data = P2ImMessageReceiveV1()
            await handler.handle_message(event_data)
        except Exception as e:
            logger.error(f"Handle message event error: {e}", exc_info=True)

    return {"code": 0, "msg": "ok"}


@router.post("/feishu/card/callback")
async def handle_card_callback(request: Request):
    """飞书卡片回调"""
    body = await request.json()
    action = body.get("action", {})
    action_value = action.get("value", {})

    action_type = action_value.get("action")
    assessment_id = action_value.get("id")

    if action_type == "disagree":
        # 记录教师反馈
        pass

    return {"code": 0, "msg": "ok"}
