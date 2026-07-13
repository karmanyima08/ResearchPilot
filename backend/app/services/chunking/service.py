from .markdown_chunker import MarkdownChunker


class ChunkingService:

    def __init__(self):

        self.chunker = MarkdownChunker()

    def chunk_markdown(self, markdown: str):

        return self.chunker.chunk(markdown)