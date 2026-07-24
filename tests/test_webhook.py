"""Level 3 验收测试：Webhook 接收 + 消息解析"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health")
        assert resp.status_code == 200


@pytest.mark.asyncio
async def test_challenge_verification():
    """飞书 URL 验证"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/webhook", json={"challenge": "test123"})
        assert resp.json()["challenge"] == "test123"


@pytest.mark.asyncio
async def test_parse_assessment_command():
    """解析评估指令"""
    from app.utils.text_parser import parse_teacher_message
    cmd = parse_teacher_message("评估 学生:小明 年级:3 主题:动物穿衣服 发言:我觉得应该给动物穿衣服")
    assert cmd.action == "assess"
    assert cmd.student_name == "小明"
    assert cmd.grade == 3
    assert cmd.topic == "动物穿衣服"
    assert "应该给动物穿衣服" in cmd.text


@pytest.mark.asyncio
async def test_parse_help():
    from app.utils.text_parser import parse_teacher_message
    cmd = parse_teacher_message("帮助")
    assert cmd.action == "help"


@pytest.mark.asyncio
async def test_parse_query():
    from app.utils.text_parser import parse_teacher_message
    cmd = parse_teacher_message("查询 小明")
    assert cmd.action == "query"
    assert cmd.student_name == "小明"


@pytest.mark.asyncio
async def test_webhook_ignores_non_mention_message():
    """非 @机器人 的群消息应被忽略（不返回解析结果）"""
    event_body = {
        "header": {"token": "", "event_type": "im.message.receive_v1"},
        "event": {
            "sender": {"sender_id": {"open_id": "ou_teacher"}},
            "message": {
                "message_type": "text",
                "chat_id": "oc_test",
                "message_id": "om_test",
                "content": '{"text": "今天天气不错"}',
            },
        },
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/webhook", json=event_body)
        assert resp.status_code == 200
        assert resp.json() == {"code": 0}
