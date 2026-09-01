from fastapi import UploadFile

from .validator import Validator
from .storage import StorageService
from .docling_parser import DoclingParser
from app.services.chunking.service import ChunkingService

class DocumentIngestionService:

    def __init__(self):
        self.storage = StorageService()
        self.parser = DoclingParser()
        self.chunking = ChunkingService()

    def ingest(self, file: UploadFile):
        print("########## INGEST STARTED ##########")

        Validator.validate_pdf(file)

        result = self.storage.save_pdf(file)

        print("=" * 60)
        print("UPLOADED FILE:", file.filename)
        print("SAVED PDF PATH:", result["pdf_path"])
        print("=" * 60)


        parsed_document = self.parser.parse(result["pdf_path"])

        chunks = self.chunking.chunk_markdown(parsed_document.markdown)

        print("\n" + "=" * 80)
        print("CHUNKING REPORT")
        print("=" * 80)
        print(f"Total Chunks: {len(chunks)}")

        for chunk in chunks:
            print(
                f"[{chunk.chunk_id}] {chunk.section} "
                f"({len(chunk.content)} chars)"
            )
        print("Markdown length before saving:", len(parsed_document.markdown))
        markdown_path = self.storage.save_markdown(
            result["paper_folder"],
            parsed_document.markdown
        )



        parsed_path = self.storage.save_parsed_document(
            result["paper_folder"],
            parsed_document
        )

        print("Returned:", parsed_path)

        return {
            **result,
            "markdown_path": markdown_path,
            "parsed_path": parsed_path
        }