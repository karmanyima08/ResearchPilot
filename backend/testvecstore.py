from pathlib import Path

from app.services.chunking.service import ChunkingService
from app.services.embeddings.service import EmbeddingService
from app.services.vector_store.service import VectorStoreService


markdown = Path(
    "storage/papers/e0d48c4b-bf97-4960-9091-2e33ae68f031/parsed.md"
).read_text(encoding="utf-8")


chunks = ChunkingService().chunk_markdown(markdown)

embeddings = EmbeddingService().embed_chunks(chunks)

VectorStoreService().store(chunks, embeddings)

print("Stored", len(chunks), "chunks successfully!")