from fastapi import FastAPI
from app.api.papers import router as papers_router

app = FastAPI(
    title="ResearchPilot API",
    description="Backend API for the AI-powered Research Assistant",
    version="0.1.0"
)

app.include_router(papers_router)


@app.get("/")
async def root():
    return {
        "message": "ResearchPilot API is running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }