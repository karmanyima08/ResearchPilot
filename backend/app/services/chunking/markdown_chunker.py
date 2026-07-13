import re
from typing import List

from .chunker import Chunker
from .models import Chunk


class MarkdownChunker(Chunker):

    MAX_CHARS = 1000
    OVERLAP = 150

    def chunk(self, markdown: str) -> List[Chunk]:

        sections = self._extract_sections(markdown)

        chunks = []

        chunk_id = 1

        for heading, text in sections:

            text = text.strip()

            if len(text) <= self.MAX_CHARS:

                chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        section=heading,
                        content=text,
                        metadata={
                            "heading": heading,
                            "part": 1
                        }
                    )
                )

                chunk_id += 1

            else:

                start = 0
                part = 1

                while start < len(text):

                    end = start + self.MAX_CHARS

                    chunk_text = text[start:end]

                    chunks.append(
                        Chunk(
                            chunk_id=chunk_id,
                            section=heading,
                            content=chunk_text,
                            metadata={
                                "heading": heading,
                                "part": part
                            }
                        )
                    )

                    chunk_id += 1
                    part += 1

                    start += self.MAX_CHARS - self.OVERLAP

        return chunks

    def _extract_sections(self, markdown: str):

        sections = []

        current_heading = "Document"
        current_lines = []

        for line in markdown.splitlines():

            if re.match(r"^#{1,6}\s+", line):

                sections.append(
                    (
                        current_heading,
                        "\n".join(current_lines)
                    )
                )

                current_heading = line.lstrip("#").strip()

                current_lines = []

            else:

                current_lines.append(line)

        sections.append(
            (
                current_heading,
                "\n".join(current_lines)
            )
        )

        return sections