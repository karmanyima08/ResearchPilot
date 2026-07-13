from abc import ABC, abstractmethod
from typing import List

from .models import Chunk


class Chunker(ABC):

    @abstractmethod
    def chunk(self, markdown: str) -> List[Chunk]:
        pass