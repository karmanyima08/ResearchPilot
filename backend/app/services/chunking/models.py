from dataclasses import dataclass
from typing import Dict


@dataclass
class Chunk:
    chunk_id: int
    section: str
    content: str
    metadata: Dict

    @property
    def length(self):
        return len(self.content)