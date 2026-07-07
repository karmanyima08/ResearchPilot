from fastapi import UploadFile

from .validator import Validator
from .storage import StorageService


class DocumentIngestionService:

    def __init__(self):
        self.storage = StorageService()

    def ingest(self, file: UploadFile):

        Validator.validate_pdf(file)

        result = self.storage.save_pdf(file)

        return result