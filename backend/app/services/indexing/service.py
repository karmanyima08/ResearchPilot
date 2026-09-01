from fastapi import UploadFile

from app.services.document_ingestion.storage import StorageService
from app.services.document_ingestion.validator import Validator
from app.services.document_ingestion.docling_parser import DoclingParser

from app.services.chunking.service import ChunkingService
from app.services.embeddings.service import EmbeddingService
from app.services.vector_store.service import VectorStoreService


class IndexingService:

    def __init__(self):

        self.storage = StorageService()
        self.parser = DoclingParser()

        self.chunker = ChunkingService()

        self.embedder = EmbeddingService()

        self.vector_store = VectorStoreService()

    def index(self, file: UploadFile):

        Validator.validate_pdf(file)

        storage_result = self.storage.save_pdf(file)

        parsed_document = self.parser.parse(
            storage_result["pdf_path"]
        )

        markdown_path = self.storage.save_markdown(
            storage_result["paper_folder"],
            parsed_document.markdown
        )

        parsed_path = self.storage.save_parsed_document(
            storage_result["paper_folder"],
            parsed_document
        )

        chunks = self.chunker.chunk_markdown(
            parsed_document.markdown
        )

        # Enrich metadata with paper information
        for chunk in chunks:
            chunk.metadata["paper_id"] = storage_result["paper_id"]
            chunk.metadata["paper_name"] = file.filename

        embeddings = self.embedder.embed_chunks(chunks)

        self.vector_store.store(
            chunks,
            embeddings
        )

        return {
            "paper_id": storage_result["paper_id"],
            "chunks": len(chunks),
            "markdown_path": str(markdown_path),
            "parsed_path": str(parsed_path)
        }