from abc import ABC, abstractmethod
from pathlib import Path

from .models import ParsedDocument


class DocumentParser(ABC):

    @abstractmethod
    def parse(self, pdf_path: Path) -> ParsedDocument:
        pass