from pathlib import Path

from app.services.chunking.service import ChunkingService


markdown = Path(
    "storage/papers/e0d48c4b-bf97-4960-9091-2e33ae68f031/parsed.md"
).read_text(encoding="utf-8")

service = ChunkingService()

chunks = service.chunk_markdown(markdown)

print("=" * 80)
print("TOTAL CHUNKS:", len(chunks))
print("=" * 80)

for chunk in chunks:

    print("=" * 60)

    print("Chunk ID:", chunk.chunk_id)

    print("Section:", chunk.section)

    print("Part:", chunk.metadata["part"])

    print("Length:", chunk.length)

    print(chunk.content[:120])

    print()