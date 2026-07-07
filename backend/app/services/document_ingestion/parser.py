from abc import ABC, abstractmethod
from pathlib import Path

from .models import ParsedDocument


class DocumentParser(ABC):
    """
    Base class for all document parsers.
    """

    @abstractmethod
    def parse(self, pdf_path: Path) -> ParsedDocument:
        """
        Convert a document into a ParsedDocument.
        """
        pass