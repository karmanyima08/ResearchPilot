from fastapi import APIRouter, UploadFile, File

from app.services.document_ingestion.service import DocumentIngestionService

router = APIRouter(
    prefix="/api/v1/papers",
    tags=["Papers"]
)

from app.services.indexing.service import IndexingService

service = IndexingService()


@router.post("/upload")
async def upload_paper(file: UploadFile = File(...)):

    result = service.index(file)

    return {
        "success": True,
        **result
    }