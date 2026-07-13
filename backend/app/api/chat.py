from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retrieval.service import RetrievalService
from app.services.llm.service import LLMService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

retriever = RetrievalService()
llm = LLMService()


class ChatRequest(BaseModel):
    question: str
    paper_id: str | None = None


@router.post("/")
async def chat(request: ChatRequest):
    results = retriever.search(
        request.question,
        paper_id=request.paper_id
    )

    answer = llm.answer(
        request.question,
        results
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": [r.metadata for r in results]
    }