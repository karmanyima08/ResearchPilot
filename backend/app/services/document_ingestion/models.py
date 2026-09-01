from dataclasses import dataclass, field

@dataclass
class ParsedDocument:
    """
    Standard representation of a parsed document.
    """

    markdown: str

    sections: dict[str, str] = field(default_factory=dict)

    metadata: dict = field(default_factory=dict)