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

        print("\n" + "=" * 80)
        print("DOCILING MARKDOWN OUTPUT")
        print("=" * 80)
        print(parsed_document.markdown[:1000])
        print("=" * 80)

        return result