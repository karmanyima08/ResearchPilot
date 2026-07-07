from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ParsedDocument:
    """
    Represents a parsed research paper before it is stored.
    """

    markdown: str
    metadata: Dict[str, Any]
    structure: Dict[str, Any] = field(default_factory=dict)