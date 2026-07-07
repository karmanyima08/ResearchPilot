from pathlib import Path

from .parser import DocumentParser
from .models import ParsedDocument


class DoclingParser(DocumentParser):

    def parse(self, pdf_path: Path) -> ParsedDocument:
        raise NotImplementedError("Docling parser not implemented yet.")