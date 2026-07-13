from dataclasses import dataclass
from typing import Dict


@dataclass
class SearchResult:
    content: str
    score: float
    metadata: Dict