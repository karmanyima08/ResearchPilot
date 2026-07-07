from fastapi import APIRouter, UploadFile, File

from app.services.document_ingestion.service import DocumentIngestionService

router = APIRouter(
    prefix="/api/v1/papers",
    tags=["Papers"]
)

service = DocumentIngestionService()


@router.post("/upload")
async def upload_paper(file: UploadFile = File(...)):

    result = service.ingest(file)

    return {
        "success": True,
        "paper_id": result["paper_id"],
        "filename": file.filename
    }