import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_assessment_request():
    return {
        "student_id": "test_student_001",
        "class_id": "test_class_001",
        "grade": 3,
        "topic": "应不应该给动物穿衣服？",
        "response": "我觉得不应该给动物穿衣服，因为动物有自己的毛，冬天不会冷。"
    }
