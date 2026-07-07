from dataclasses import dataclass

@dataclass
class ParsedDocument:
    """
    Standard representation of a parsed document.
    """

    markdown: str