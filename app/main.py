from fastapi import FastAPI
from app.api.webhook import router as webhook_router

app = FastAPI(title="EduSocratic", version="0.1.0")
app.include_router(webhook_router)


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
