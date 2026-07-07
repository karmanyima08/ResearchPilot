from pathlib import Path

from docling.document_converter import DocumentConverter

from .parser import DocumentParser
from .models import ParsedDocument


class DoclingParser(DocumentParser):

    def __init__(self):
        self.converter = DocumentConverter()

    def parse(self, pdf_path: Path) -> ParsedDocument:
        result = self.converter.convert(str(pdf_path))

        markdown = result.document.export_to_markdown()

        return ParsedDocument(markdown=markdown)