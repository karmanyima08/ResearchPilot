from pathlib import Path

from app.services.chunking.service import ChunkingService
from app.services.embeddings.service import EmbeddingService

markdown = Path(
    "storage/papers/e0d48c4b-bf97-4960-9091-2e33ae68f031/parsed.md"
).read_text(encoding="utf-8")

chunk_service = ChunkingService()

chunks = chunk_service.chunk_markdown(markdown)

embedding_service = EmbeddingService()

vectors = embedding_service.embed_chunks(chunks)

print("=" * 80)
print("Chunks:", len(chunks))
print("Vectors:", len(vectors))
print("Embedding Dimension:", len(vectors[0]))
print("=" * 80)