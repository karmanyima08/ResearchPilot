from fastapi import APIRouter, UploadFile, File
from fastapi import HTTPException
from app.services.papers.service import PaperService
from app.services.document_ingestion.service import DocumentIngestionService

router = APIRouter(
    prefix="/api/v1/papers",
    tags=["Papers"]
)

from app.services.indexing.service import IndexingService

service = IndexingService()
paper_service = PaperService()

@router.post("/upload")
async def upload_paper(file: UploadFile = File(...)):

    if paper_service.exists(file.filename):
        raise HTTPException(
            status_code=409,
            detail="A paper with this filename already exists."
        )
    result = service.index(file)

    return {
        "success": True,
        **result
    }