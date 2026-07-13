from app.services.retrieval.service import RetrievalService

service = RetrievalService()

results = service.search(
    "What is Retrieval-Augmented Generation?"
)

print("=" * 80)

for i, result in enumerate(results, start=1):

    print(f"Result {i}")
    print("Score:", result.score)
    print("Heading:", result.metadata.get("heading"))
    print()
    print(result.content[:300])
    print("-" * 80)