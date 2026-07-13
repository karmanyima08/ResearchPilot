from fastapi import APIRouter

from app.services.papers.service import PaperService

router = APIRouter(
    prefix="/papers",
    tags=["Papers"]
)

paper_service = PaperService()


@router.get("/")
async def list_papers():

    return paper_service.list_papers()