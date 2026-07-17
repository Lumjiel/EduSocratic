from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    import redis.asyncio as redis
    from app.infrastructure.llm.base import LLMClientFactory
    from app.infrastructure.llm.circuit_breaker import CostCircuitBreaker
    from app.infrastructure.cache.similarity import SimilarityCache
    from app.infrastructure.feishu.client import FeishuClient
    from app.infrastructure.feishu.card_builder import CardBuilder
    from app.infrastructure.feishu.event_handler import FeishuEventHandler
    from app.domain.grading.engine import GradingEngine
    from app.domain.grading.validator import OutputValidator
    from app.domain.grading.prompt_manager import PromptManager

    app.state.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    app.state.llm = LLMClientFactory.create()
    app.state.validator = OutputValidator(app.state.llm)
    app.state.prompts = PromptManager()
    app.state.breaker = CostCircuitBreaker(app.state.redis)
    app.state.cache = SimilarityCache(app.state.redis)
    app.state.feishu = FeishuClient()
    app.state.cards = CardBuilder()
    app.state.engine = GradingEngine(
        llm=app.state.llm,
        validator=app.state.validator,
        prompt_manager=app.state.prompts,
        circuit_breaker=app.state.breaker,
        similarity_cache=app.state.cache,
    )
    app.state.event_handler = FeishuEventHandler(
        feishu_client=app.state.feishu,
        grading_engine=app.state.engine,
        card_builder=app.state.cards,
    )

    yield

    # Shutdown
    await app.state.redis.close()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1 import router as api_router
app.include_router(api_router, prefix="/api")


@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME}
