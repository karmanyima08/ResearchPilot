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

@router.delete("/{paper_id}")
async def delete_paper(paper_id: str):
    return paper_service.delete_paper(paper_id)