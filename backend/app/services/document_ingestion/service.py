from fastapi import UploadFile

from .validator import Validator
from .storage import StorageService
from .docling_parser import DoclingParser


class DocumentIngestionService:

    def __init__(self):
        self.storage = StorageService()
        self.parser = DoclingParser()

    def ingest(self, file: UploadFile):

        Validator.validate_pdf(file)

        result = self.storage.save_pdf(file)

        parsed_document = self.parser.parse(result["pdf_path"])

        markdown_path = self.storage.save_markdown(
            result["paper_folder"],
            parsed_document.markdown
        )

        return {
            **result,
            "markdown_path": markdown_path
        }