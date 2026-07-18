from fastapi import FastAPI
from app.api.papers import router as papers_router
from app.api.chat import router as chat_router
from app.api.papers_manager import router as papers_manager_router
from fastapi.middleware.cors import CORSMiddleware
from app.api import export

app = FastAPI(
    title="ResearchPilot API",
    description="Backend API for the AI-powered Research Assistant",
    version="0.1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(export.router)
app.include_router(papers_router)
app.include_router(chat_router)
app.include_router(papers_manager_router)

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