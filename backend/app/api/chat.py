from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chat.service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

chat_service = ChatService()


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    question: str
    paper_ids: list[str] = []
    history: list[ChatMessage] = []


class LiteratureReviewRequest(BaseModel):
    paper_ids: list[str]

class CompareRequest(BaseModel):
    paper_ids: list[str]

class ResearchGapRequest(BaseModel):
    paper_ids: list[str]

@router.post("/")
async def chat(request: ChatRequest):
    answer, results, suggestions = chat_service.ask(
        request.question,
        request.paper_ids,
        request.history,
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": [r.metadata for r in results],
        "suggestions": suggestions
    }


@router.post("/literature-review")
async def literature_review(request: LiteratureReviewRequest):

    answer, results = chat_service.generate_literature_review(
        request.paper_ids
    )

    return {
        "answer": answer,
        "sources": [r.metadata for r in results]
    }

@router.post("/compare")
async def compare(request: CompareRequest):

    answer, results = chat_service.compare_papers(
        request.paper_ids
    )

    return {
        "answer": answer,
        "sources": [r.metadata for r in results]
    }
@router.post("/research-gaps")
async def research_gaps(request: ResearchGapRequest):
        answer, results = chat_service.research_gaps(
            request.paper_ids
        )

        return {
            "answer": answer,
            "sources": [r.metadata for r in results]
        }